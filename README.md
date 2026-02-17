# app_agent

Agente autônomo Python para execução de tarefas automatizadas, geração de código e integração com OpenAI.

## Funcionalidades
- Gera código Python automaticamente a partir de instruções em linguagem natural.
- Executa o código gerado em ambiente isolado (sandbox_agent/execucao.py).
- Suporte a execução local via venv ou em ambiente Docker.
- Integração com OpenAI para geração de código.

## Requisitos
- Python 3.8+
- Conta e chave de API OpenAI
- (Opcional) Docker

## Instalação
1. Clone o repositório:
   ```
   git clone <url-do-repositorio>
   cd app_agent
   ```
2. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   # ou
   source venv/bin/activate  # Linux/Mac
   ```
3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
4. Configure o arquivo `.env` com sua chave OpenAI e, se necessário, credenciais de e-mail:
   ```
   OPENAI_API_KEY=sk-...
   GMAIL_LOGIN=seu@email.com
   GMAIL_PASSWORD=suasenha
   ```

## Uso
Execute o agente:
```bash
python app.py
```
Digite sua tarefa em linguagem natural e o agente irá gerar e executar o código correspondente.

## Docker
Para rodar em container:
```bash
docker build -t app_agent .
docker run -it --rm --env-file .env -v ${PWD}/sandbox_agent:/sandbox_agent app_agent
```

## Observações
- O código gerado é salvo e executado em `sandbox_agent/execucao.py`.
- Para automações que exigem acesso ao sistema operacional, prefira rodar fora do Docker.
- Não compartilhe sua chave OpenAI publicamente.

## Licença
MIT
