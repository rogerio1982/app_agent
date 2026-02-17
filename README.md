# My_app_bot

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

# Interactive Python Agent with OpenAI

This project is an interactive Python agent that uses the OpenAI API to automatically generate and execute Python code according to user-provided tasks. The agent can automatically install dependencies if needed for task execution.

## Features
- Automatic Python code generation via OpenAI GPT-4o-mini
- Safe execution of generated code in a sandbox
- Error detection and handling
- Automatic installation of Python dependencies (via pip) when required
- Interactive loop for multiple tasks

## Prerequisites
- Python 3.8+
- OpenAI account and API key

## Installation
1. Clone this repository or download the files.
2. Create a virtual environment (optional, but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate    # Windows
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root with the following variables:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   GMAIL_LOGIN=your_email@gmail.com  # Optional, if using email features
   GMAIL_PASSWORD=your_password      # Optional
   ```

## How to Use
Run the agent with:
```bash
python app.py
```
Type the desired task when prompted. The agent will generate, install dependencies (if needed), and execute the code automatically.

To exit, type `sair`, `exit`, or `quit`.

## Project Structure
- `app.py`: Main agent code
- `requirements.txt`: Project dependencies
- `relatorios/`: Folder for output reports (example)

## Notes
- The agent executes automatically generated Python code. Use in a controlled environment.
- Extra dependencies may be installed automatically by the agent as required by the task.

## License
MIT
