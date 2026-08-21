from flask import Flask, render_template, abort

app = Flask(__name__)

OPCOES = {
    1: {"titulo": "Casos confirmados", "subtitulo": "Febre Amarela", "texto": "..."},
    2: {"titulo": "Óbitos e letalidade", "subtitulo": "Febre Amarela", "texto": "..."},
    3: {"titulo": "Distribuição geográfica", "subtitulo": "Febre Amarela", "texto": "..."},
}

@app.route('/')
def home():
    return render_template("index.html", dados={"subtitulo": "Febre Amarela"})

@app.route("/opcao/<int:num>")
def opcao(num):
    dados = OPCOES.get(num)
    if not dados:
        abort(404)
    return render_template("opcao.html", numero=num, dados=dados)

@app.route("/destaque")
def destaque():
    return render_template(
        "opcao.html",
        numero=None,
        dados={ "titulo": "Destaque", "texto": "Conteúdo em destaque"},
    )

if __name__ == "__main__":
    app.run(debug=True)