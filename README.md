# PI DATASUS: Análise de dados do DATASUS (Febre Amarela)

Aplicação web desenvolvida em Python com Flask e Streamlit que apresenta o estudo teórico, a definição das bases de dados e painéis interativos sobre febre amarela em humanos e primatas não humanos (1994 a 2026), a partir dos dados abertos do DATASUS.

## Tecnologias

- Python;
- Flask e Jinja2 (páginas);
- Markdown (conteúdo textual das páginas);
- Streamlit, Altair e pandas (painéis interativos, embutidos via `<iframe>`);
- HTML e CSS.

## Instalação

Crie o ambiente virtual (rode apenas uma vez, dentro da pasta do projeto):

```bash
python -m venv venv
```

Ative o ambiente virtual:

```bash
.\venv\Scripts\Activate.ps1      # Windows PowerShell
venv\Scripts\activate.bat        # Windows CMD
source venv/bin/activate         # macOS ou Linux
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Executando o projeto

Com o ambiente virtual ativado, execute:

```bash
python run.py
```

O `run.py` inicia o servidor Flask e, junto com ele, os dois apps Streamlit (portas `8501` e `8502`, definidas em `config.py`), que aparecem na página **Análise de Dados**.

Acesse no navegador: `http://127.0.0.1:5000/`.

## Estrutura do projeto

```text
PI_DATASUS/
├── app/
│   ├── services/        # Regras de negócio (leitura do Markdown e controle do Streamlit)
│   ├── static/
│   │   └── css/         # Estilos separados por responsabilidade
│   ├── templates/       # Templates Jinja2
│   │   └── shared/      # Partes reutilizáveis (cabeçalho e gráficos)
│   ├── __init__.py      # Criação da aplicação Flask
│   └── routes.py        # Rotas da aplicação
├── content/             # Textos das páginas em Markdown
├── data/                # Bases de dados (JSON) usadas nos painéis
├── streamlit_apps/      # Painéis Streamlit (app_anos, app_estado) e código comum
├── config.py            # Configurações (pastas e portas do Streamlit)
├── requirements.txt     # Dependências Python
└── run.py               # Ponto de entrada da aplicação
```

### Estilos (`app/static/css/`)

| Arquivo | Conteúdo |
|---|---|
| `base.css` | Variáveis de cor/fonte, reset e estilos globais |
| `header.css` | Cabeçalho, abas de navegação e menu suspenso |
| `content.css` | Cartão de conteúdo (texto vindo do Markdown) |
| `graficos.css` | Seção de gráficos e iframes do Streamlit |
| `index.css` | Página inicial |

A ordem dos `<link>` em `templates/base.html` importa (`base.css` primeiro).

## Observações

- O servidor de desenvolvimento do Flask é adequado para desenvolvimento local, não para produção.
- Os textos das páginas ficam em `content/*.md`; para alterar o conteúdo, edite esses arquivos.
