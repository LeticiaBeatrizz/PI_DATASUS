import os


class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CONTENT_DIR = os.path.join(BASE_DIR, "content")
    STREAMLIT_APPS_DIR = os.path.join(BASE_DIR, "streamlit_apps")

    # Portas onde os apps Streamlit ficam disponíveis. São embutidos na página
    # de "Análise de Dados" via <iframe> (ver templates/shared/graficos_streamlit.html).
    PORTA_STREAMLIT_ANOS = 8501
    PORTA_STREAMLIT_ESTADO = 8502
