import os
import subprocess
from openai import OpenAI
from dotenv import load_dotenv

# =========================
# CONFIGURAÇÃO
# =========================

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
login = os.getenv("GMAIL_LOGIN")
senha = os.getenv("GMAIL_PASSWORD")

if not api_key:
    raise ValueError("OPENAI_API_KEY não encontrada.")

client = OpenAI(api_key=api_key)

SANDBOX_DIR = os.path.abspath("/sandbox_agent")
MAX_ITERACOES = 5

os.makedirs(SANDBOX_DIR, exist_ok=True)

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


def executar_codigo(codigo):
    caminho = os.path.join(SANDBOX_DIR, "execucao.py")

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(codigo)

    # Executa o código Python
    resultado = subprocess.run(
        ["python", caminho],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    return resultado


def executar_agente(tarefa):
    mensagens = [
        {
            "role": "system",
            "content": """
            Gere apenas código Python executável, puro, sem nenhum comentário, explicação, instrução, texto adicional ou orientação sobre próximos passos. Não inclua comentários de código, nem linhas iniciadas com #, nem mensagens para o usuário. Apenas o código necessário para executar a tarefa solicitada.
            """
        },
        {"role": "user", "content": tarefa}
    ]

    tentativa = 1

    
    while tentativa <= MAX_ITERACOES:
        print(f"\n🔄 Tentativa {tentativa} de {MAX_ITERACOES}...")

        # Gera código
        codigo = gerar_codigo(mensagens)

        # Limpa Markdown se houver
        codigo = codigo.strip()
        if codigo.startswith("```") and codigo.endswith("```"):
            codigo = "\n".join(codigo.split("\n")[1:-1])

        print("\n💻 Código gerado pelo agente:")
        print(codigo)

        # Executa o código
        resultado = executar_codigo(codigo)

        # Verifica se houve erro (stderr ou returncode != 0)
        erro_stderr = resultado.stderr.strip()
        erro_stdout = resultado.stdout.strip()
        
        # Detecta se há mensagem de erro no stdout também
        tem_erro_stdout = any(keyword in erro_stdout.lower() for keyword in ["erro", "error", "exception", "traceback", "failed", "falha"])
        
        # Se sucesso (sem erros e returncode 0), retorna
        if resultado.returncode == 0 and not erro_stderr and not tem_erro_stdout:
            print("\n✅ Execução bem-sucedida!")
            return resultado.stdout if resultado.stdout else "Tarefa executada com sucesso."

        # Se deu erro, junta stderr e stdout para análise
        erro = f"STDERR:\n{erro_stderr}\n\nSTDOUT:\n{erro_stdout}" if erro_stderr or tem_erro_stdout else "Código executou mas não produziu resultado esperado."
        #print("\n❌ Erro detectado:", erro)

        mensagens.append({"role": "assistant", "content": codigo})
        mensagens.append({
            "role": "user",
            "content": f"O código anterior deu o seguinte erro:\n{erro}\nPor favor, gere um novo código Python que funcione."
        })

        tentativa += 1
        print(f"🔄 Tentando novamente... (tentativa {tentativa}/{MAX_ITERACOES})\n")

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
