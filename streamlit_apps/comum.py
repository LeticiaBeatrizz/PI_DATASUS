import json
import os

import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def liberar_largura_total():
    # --- Ajuste de largura: no modo embed (iframe do Flask) o Streamlit ignora o layout="wide"
    # e limita o conteúdo a 736px. Este CSS libera a largura total do iframe.
    st.markdown("""
        <style>
            .block-container { max-width: 100% !important; padding-left: 1.5rem; padding-right: 1.5rem; }
        </style>
    """, unsafe_allow_html=True)


def carregar_dados():
    with open(os.path.join(DATA_DIR, "fa_casoshumanos_1994-2026.json"), "r", encoding="utf-8") as arquivo:
        dados_humanos = json.load(arquivo)

    with open(os.path.join(DATA_DIR, "fa_epizpnh_1994-2026.json"), "r", encoding="utf-8") as arquivo:
        dados_epizootias = json.load(arquivo)

    return dados_humanos, dados_epizootias


def fmt(n):
    return f"{int(n):,}".replace(",", ".")
