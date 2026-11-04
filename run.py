import atexit
import os

from app import app
from app.services.StreamlitService import StreamlitService


if __name__ == "__main__":
    # evita subir os apps Streamlit duas vezes por causa do reloader do Flask
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        StreamlitService.iniciar_apps()
        atexit.register(StreamlitService.encerrar_apps)

    app.run(debug=True)
