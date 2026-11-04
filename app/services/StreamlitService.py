import os
import subprocess
import sys

from config import Config


_processos_streamlit = []


class StreamlitService():
    @staticmethod
    def iniciar_apps():
        """Sobe os dois apps Streamlit (evolução anual e por estado) em segundo
        plano, cada um na sua porta, para serem exibidos via <iframe>.

        --server.enableCORS false e --server.enableXsrfProtection false são
        necessários porque, por padrão, o Streamlit bloqueia ser exibido dentro
        de um <iframe> de outra origem (nesse caso, a página servida pelo Flask).
        """
        apps = [
            ("app_anos.py", Config.PORTA_STREAMLIT_ANOS),
            ("app_estado.py", Config.PORTA_STREAMLIT_ESTADO),
        ]

        for nome_arquivo, porta in apps:
            caminho_app = os.path.join(Config.STREAMLIT_APPS_DIR, nome_arquivo)
            processo = subprocess.Popen(
                [
                    sys.executable, "-m", "streamlit", "run", caminho_app,
                    "--server.port", str(porta),
                    "--server.headless", "true",
                    "--server.enableCORS", "false",
                    "--server.enableXsrfProtection", "false",
                    "--browser.gatherUsageStats", "false",
                ]
            )
            _processos_streamlit.append(processo)

    @staticmethod
    def encerrar_apps():
        for processo in _processos_streamlit:
            processo.terminate()
