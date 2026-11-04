import os

import markdown
from config import Config


class ConteudoService():
    @staticmethod
    def carregar_markdown(nome_arquivo):
        """Lê um arquivo .md em content/ e devolve o HTML já renderizado."""
        caminho = os.path.join(Config.CONTENT_DIR, nome_arquivo)
        with open(caminho, "r", encoding="utf-8") as arquivo:
            texto_md = arquivo.read()
        return markdown.markdown(texto_md, extensions=["tables", "extra"])
