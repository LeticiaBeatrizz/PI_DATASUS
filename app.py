from flask import Flask, render_template, abort

app = Flask(__name__)

ESTUDO_TEORICO_HTML = """
<p>Este trabalho apresenta um estudo teórico do arbovírus da febre amarela a fim de
fundamentar e consolidar a base conceitual para o desenvolvimento do Projeto Integrador
(PI) que analisa o conjunto de dados sobre Febre Amarela em humanos e primatas
não-humanos de 1994 a 2026, disponível no Portal de Dados Abertos do SUS. Nesse viés,
conta-se com linguagem de programação para o propósito final de criar um painel interativo
com as informações disponíveis. Assim, estrutura-se um documento contendo a definição da
patologia, seus fatores de transmissão e os elementos que colaboram para a perpetuação da
doença na sociedade brasileira.</p>

<h2>1. Febre amarela: estudo teórico</h2>

<h3>1.1 Definição</h3>
<p>Durante as pesquisas realizadas para o início deste relatório, a partir das informações
divulgadas pelo Ministério da Saúde, constata-se que, segundo o Brasil (2023), a febre
amarela é <em>“[...] uma doença infecciosa febril aguda, imunoprevenível, de evolução abrupta e
gravidade variável, com elevada letalidade nas suas formas [...]”</em>. Dentre os sintomas
apresentados pelos infectados, pode-se citar: início súbito de febre; dores no corpo em geral;
calafrios; náuseas e vômitos; dor de cabeça intensa; fadiga; dores nas costas e fraqueza. Após
o início das queixas, cerca de 85% dos doentes costuma melhorar. No entanto,
aproximadamente 15% apresentam um breve período de remissão clínica — que dura de
poucas horas a um dia — antes de desenvolverem uma forma mais grave da doença.</p>
<p>Nesse contexto, a patologia tem como necessidade a notificação compulsória
imediata, isto é, todo evento suspeito — tanto morte de primatas não-humanos, quanto casos
humanos com sintomatologia compatível — deve ser prontamente comunicado/notificado, em
até 24 (vinte e quatro) horas após a suspeita inicial, às autoridades locais competentes pela
via mais rápida.</p>

<h3>1.2 Transmissão</h3>
<p>A febre amarela é causada por um vírus transmitido por mosquitos, possuindo dois
ciclos de transmissão: urbano e silvestre. Apesar de possuir diferentes espécies de vetores,
a enfermidade tem as mesmas características sob o ponto de vista etiológico, clínico,
imunológico e fisiopatológico, independente do ciclo de transmissão.</p>
<p>No ciclo urbano, a transmissão ocorre a partir de vetores urbanos (<em>Aedes aegypti</em>)
infectados. No ciclo silvestre, os transmissores são mosquitos com hábitos
predominantemente silvestres, sendo os gêneros <em>Haemagogus</em> e <em>Sabethes</em> os mais presentes.
Os hospedeiros naturais do vírus são constituídos de Primatas Não Humanos (PNHs), que
funcionam como amplificadores da doença. O homem, caso não imunizado, entra nesse ciclo
acidentalmente.</p>
<p>Não há transmissão de primata a primata; o vírus é transmitido pela picada dos
mosquitos transmissores infectados. Apenas as fêmeas realizam a transmissão, pois o repasto
sanguíneo provê nutrientes essenciais para a maturação dos ovos e, consequentemente, a
completude do ciclo gonotrófico. A passagem também ocorre de forma vertical, na qual as
fêmeas podem transferir o vírus para a sua prole, favorecendo a manutenção do vírus na
natureza. A série histórica da doença no Brasil tem demonstrado maior frequência de
ocorrência de casos humanos nos meses de dezembro e maio, como um padrão sazonal.</p>

<h3>1.3 Fatores que colaboraram para a perpetuação da doença</h3>
<p>Ao analisar a permanência e recorrência da febre amarela no território brasileiro ao
longo dos anos, percebe-se que diversos fatores contribuíram para a perpetuação da doença.
Esses fatores envolvem aspectos históricos, biológicos e geográficos, que, em conjunto,
favorecem tanto a circulação do vírus quanto a ocorrência de surtos e epidemias.</p>

<h4>1.3.1 Fatores históricos (epidemias brasileiras)</h4>
<p>No que se refere aos fatores históricos, é importante destacar que a febre amarela
possui forte presença na história sanitária brasileira, especialmente entre os séculos XIX e
XX. Nesse período, grandes epidemias atingiram cidades portuárias como Rio de Janeiro e
Salvador, favorecidas pela intensa circulação de pessoas e mercadorias. A doença causava
elevado número de mortes e prejudicava o desenvolvimento econômico e social do país.</p>
<p>Além disso, as condições precárias de saneamento básico e o baixo conhecimento
científico sobre as formas de transmissão contribuíram para a rápida disseminação da doença.
Somente no início do século XX, após estudos comprovarem a participação do mosquito
<em>Aedes aegypti</em> na transmissão, campanhas sanitárias lideradas por Oswaldo Cruz passaram a
combater o vetor de forma mais eficiente.</p>
<p>Outro fator histórico importante foi a resistência da população às campanhas de
vacinação, como ocorreu durante a Revolta da Vacina, marcada pela desinformação e pela
desconfiança nas autoridades sanitárias. Mesmo após a erradicação da transmissão urbana da
febre amarela no Brasil, em 1942, o vírus continuou circulando no ciclo silvestre,
possibilitando novos surtos ao longo das décadas. Nesse sentido, a redução da cobertura
vacinal e o fortalecimento de movimentos antivacina também contribuíram para aumentar a
vulnerabilidade da população diante da doença.</p>

<h4>1.3.2 Fatores biológicos</h4>
<p>No âmbito biológico, a perpetuação da febre amarela está diretamente relacionada à
capacidade de adaptação do vírus e à participação de diferentes organismos no ciclo de
transmissão. Os mosquitos vetores apresentam elevada eficiência na disseminação viral,
principalmente em regiões de clima favorável ao seu desenvolvimento.</p>
<p>Ademais, os primatas não-humanos exercem papel fundamental na manutenção do
ciclo silvestre da doença, funcionando como hospedeiros e amplificadores do vírus na
natureza. Outro aspecto relevante diz respeito à baixa imunização de parte da população,
fator que favorece a ocorrência de novos casos humanos. Também é válido ressaltar que o
vírus possui rápida evolução no organismo, podendo causar quadros graves e elevada taxa de
letalidade em indivíduos não vacinados.</p>

<h4>1.3.3 Fatores geográficos</h4>
<p>Em relação aos fatores geográficos, observa-se que as características ambientais
brasileiras favorecem significativamente a manutenção da febre amarela. O clima tropical
predominante em grande parte do país, associado às altas temperaturas e aos períodos
chuvosos, cria condições ideais para a proliferação dos mosquitos transmissores.</p>
<p>Além disso, áreas de mata e regiões florestais contribuem para a permanência do ciclo
silvestre da doença, especialmente em locais com grande presença de primatas não-humanos
e vetores naturais. Outro fator importante é o crescimento urbano desordenado, acompanhado
por problemas de saneamento básico e acúmulo de água parada, condições que favorecem a
reprodução do mosquito <em>Aedes aegypti</em>. Dessa forma, a combinação entre condições
ambientais e ocupação humana amplia os riscos de disseminação da febre amarela em
diferentes regiões do Brasil.</p>

<h3>Referências bibliográficas</h3>
<ul class="referencias">
    <li>BRASIL. Ministério da Saúde. <em>Febre amarela: transmissão.</em> Brasília, DF: Ministério da Saúde, 2023.</li>
    <li>BRASIL. Ministério da Saúde. <em>Febre amarela.</em> Brasília, DF: Ministério da Saúde, 2025.</li>
    <li>FUNDAÇÃO OSWALDO CRUZ (FIOCRUZ). <em>Febre amarela.</em> Rio de Janeiro: Fiocruz, [s.d.].</li>
    <li>ORGANIZAÇÃO PAN-AMERICANA DA SAÚDE (OPAS). <em>Febre amarela.</em> Washington, D.C.: OPAS, [s.d.].</li>
    <li>VASCONCELOS, Pedro Fernando da Costa. Febre amarela. <em>Revista da Sociedade Brasileira de Medicina Tropical</em>, Uberaba, v. 36, n. 2, p. 275-293, 2003.</li>
    <li>SINTOMATOLOGIA. In: DICIO, Dicionário Online de Português. Porto: 7Graus, 2026.</li>
    <li>ETIOLÓGICO. In: DICIO, Dicionário Online de Português. Porto: 7Graus, 2026.</li>
    <li>PARANÁ. Secretaria da Saúde. <em>Febre amarela.</em> Curitiba: SESA, [202-?].</li>
    <li>CICLO Gonotrófico. In: PROJETO MILD-MALÁRIA. <em>Malariapedia.</em> [S. l.: s. n.], [s.d.].</li>
</ul>
"""

OPCOES = {
    1: {
        "titulo": "Estudo Teórico",
        "subtitulo": "Febre Amarela",
        "texto": ESTUDO_TEORICO_HTML,
        "html": True,
    },
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
    return render_template("estudo_teorico.html", numero=num, dados=dados)

@app.route("/destaque")
def destaque():
    return render_template(
        "estudo_teorico.html",
        numero=None,
        dados={ "titulo": "Destaque", "texto": "Conteúdo em destaque"},
    )

if __name__ == "__main__":
    app.run(debug=True)