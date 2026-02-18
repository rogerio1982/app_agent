import os
import sys
import json
import subprocess
from openai import OpenAI
from dotenv import load_dotenv

# =========================
# CONFIGURAÇÃO
# =========================

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY não encontrada.")

client = OpenAI(api_key=api_key)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SANDBOX_DIR = os.path.join(BASE_DIR, "sandbox")
MEMORY_PATH = os.path.join(BASE_DIR, "memory_store.json")

MAX_ITERACOES = 5

os.makedirs(SANDBOX_DIR, exist_ok=True)

# =========================
# CARREGAR MEMORY_STORE
# =========================

if os.path.exists(MEMORY_PATH):
    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        memory_store = json.load(f)
else:
    memory_store = []

# =========================
# FUNÇÕES DO AGENTE
# =========================

def gerar_codigo(mensagens):
    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=mensagens,
        temperature=0
    )
    return resposta.choices[0].message.content


def salvar_memoria():
    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(memory_store, f, indent=2, ensure_ascii=False)


def executar_codigo(codigo):
    caminho_script = os.path.join(BASE_DIR, "execucao.py")

    with open(caminho_script, "w", encoding="utf-8") as f:
        f.write(codigo)

    resultado = subprocess.run(
        [sys.executable, caminho_script],
        capture_output=True,
        text=True,
        cwd=SANDBOX_DIR
    )

    return resultado


def executar_agente(tarefa):
    global memory_store

    # Garante que existe system prompt
    if not memory_store:
        memory_store.append({
            "role": "system",
            "content": """
            Gere apenas código Python executável, puro, sem comentários ou explicações.
            Trabalhe apenas dentro da pasta sandbox.
            Não utilize caminhos absolutos.
            """
        })

    # Adiciona nova tarefa
    memory_store.append({"role": "user", "content": tarefa})

    tentativa = 1

    while tentativa <= MAX_ITERACOES:
        print(f"\n🔄 Tentativa {tentativa} de {MAX_ITERACOES}...")

        codigo = gerar_codigo(memory_store)

        codigo = codigo.strip()
        if codigo.startswith("```") and codigo.endswith("```"):
            codigo = "\n".join(codigo.split("\n")[1:-1])

        print("\n💻 Código gerado pelo agente:")
        print(codigo)

        resultado = executar_codigo(codigo)

        erro_stderr = resultado.stderr.strip()
        erro_stdout = resultado.stdout.strip()

        tem_erro_stdout = any(
            keyword in erro_stdout.lower()
            for keyword in ["erro", "error", "exception", "traceback", "failed", "falha"]
        )

        # Sucesso
        if resultado.returncode == 0 and not erro_stderr and not tem_erro_stdout:
            print("\n✅ Execução bem-sucedida!")

            memory_store.append({"role": "assistant", "content": codigo})

            if erro_stdout:
                memory_store.append({
                    "role": "system",
                    "content": f"Resultado da execução:\n{erro_stdout}"
                })

            salvar_memoria()

            return erro_stdout if erro_stdout else "Tarefa executada com sucesso."

        # Erro detectado
        erro = f"STDERR:\n{erro_stderr}\n\nSTDOUT:\n{erro_stdout}"
        print("\n❌ Erro detectado:", erro)

        memory_store.append({"role": "assistant", "content": codigo})
        memory_store.append({
            "role": "user",
            "content": f"O código anterior deu o seguinte erro:\n{erro}\nPor favor, gere um novo código Python que funcione."
        })

        salvar_memoria()

        tentativa += 1
        print(f"🔄 Tentando novamente... (tentativa {tentativa}/{MAX_ITERACOES})\n")

    salvar_memoria()
    return "⚠️ Falha após várias tentativas."


# =========================
# LOOP INTERATIVO
# =========================

if __name__ == "__main__":
    print("🤖 Agente interativo iniciado.")
    print("Digite sua tarefa. (Digite 'sair' para encerrar)\n")

    while True:
        try:
            tarefa = input("📝 O que deseja fazer agora?\n>>> ")

            if tarefa.lower() in ["sair", "exit", "quit"]:
                print("👋 Encerrando agente...")
                break

            if not tarefa.strip():
                print("⚠️ Digite uma tarefa válida.")
                continue

            resultado = executar_agente(tarefa)

            print("\n📌 Resultado:")
            print(resultado)
            print("-" * 50)

        except KeyboardInterrupt:
            print("\n👋 Encerrado manualmente.")
            break

        except Exception as e:
            print(f"\n❌ Erro: {e}")
