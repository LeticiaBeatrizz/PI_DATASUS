// Cruzamento de dados: Casos Humanos x Epizootias em Primatas Não-Humanos.
// Os gráficos em si são gerados no servidor (Python + matplotlib, em graficos.py).
// Este arquivo só cuida da interação: ao trocar um filtro, busca as novas
// imagens via fetch (/api/grafico-anual e /api/grafico-uf) e troca o src das
// <img>, sem recarregar a página.

document.addEventListener("DOMContentLoaded", () => {
  const secaoGraficos = document.querySelector(".grafico-secao");
  if (!secaoGraficos) {
    return; // só executa na página que realmente tem os gráficos
  }

  // ------------------------------------------------------------------
  // Troca suave de uma <img>: baixa opacidade, troca o src, volta ao normal
  // ------------------------------------------------------------------
  function trocarImagem(imgEl, base64) {
    imgEl.style.transition = "opacity 150ms ease";
    imgEl.style.opacity = "0.25";
    const novaSrc = "data:image/png;base64," + base64;

    // espera a nova imagem carregar de fato antes de voltar a opacidade,
    // pra evitar um "flash" da imagem antiga com opacidade baixa
    const imagemTemp = new Image();
    imagemTemp.onload = () => {
      imgEl.src = novaSrc;
      imgEl.style.opacity = "1";
    };
    imagemTemp.src = novaSrc;
  }

  function animarTotal(spanEl, valorFinal) {
    const valorInicial = Number(spanEl.textContent) || 0;
    if (valorInicial === valorFinal) {
      spanEl.textContent = valorFinal;
      return;
    }
    const duracao = 300;
    const inicio = performance.now();

    function passo(agora) {
      const progresso = Math.min((agora - inicio) / duracao, 1);
      const valorAtual = Math.round(valorInicial + (valorFinal - valorInicial) * progresso);
      spanEl.textContent = valorAtual;
      if (progresso < 1) {
        requestAnimationFrame(passo);
      }
    }
    requestAnimationFrame(passo);
  }

  // ------------------------------------------------------------------
  // Gráfico 1: evolução anual — casos humanos x epizootias em PNH
  // ------------------------------------------------------------------
  const selectAno1 = document.getElementById("ano_grafico1");
  const imgHumAnual = document.getElementById("img-anual-humanos");
  const imgEpiAnual = document.getElementById("img-anual-epizootias");

  if (selectAno1 && imgHumAnual && imgEpiAnual) {
    selectAno1.addEventListener("change", () => {
      const params = new URLSearchParams({ ano: selectAno1.value });

      fetch(`/api/grafico-anual?${params.toString()}`)
        .then((resposta) => {
          if (!resposta.ok) {
            throw new Error(`Erro HTTP ${resposta.status}`);
          }
          return resposta.json();
        })
        .then((dados) => {
          trocarImagem(imgHumAnual, dados.img_humanos);
          trocarImagem(imgEpiAnual, dados.img_epizootias);
        })
        .catch((erro) => console.error("Erro ao atualizar o gráfico anual:", erro));
    });
  }

  // ------------------------------------------------------------------
  // Gráfico 2: ocorrências por estado, com filtro de ano e UF
  // ------------------------------------------------------------------
  const selectAno2 = document.getElementById("ano_grafico2");
  const selectUf2 = document.getElementById("uf_grafico2");
  const imgHumUf = document.getElementById("img-uf-humanos");
  const imgEpiUf = document.getElementById("img-uf-epizootias");
  const totalHumanosSpan = document.getElementById("total-humanos-uf");
  const totalEpizootiasSpan = document.getElementById("total-epizootias-uf");

  if (selectAno2 && selectUf2 && imgHumUf && imgEpiUf) {
    function atualizarGrafico2() {
      const params = new URLSearchParams({ ano: selectAno2.value, uf: selectUf2.value });

      fetch(`/api/grafico-uf?${params.toString()}`)
        .then((resposta) => {
          if (!resposta.ok) {
            throw new Error(`Erro HTTP ${resposta.status}`);
          }
          return resposta.json();
        })
        .then((dados) => {
          trocarImagem(imgHumUf, dados.img_humanos);
          trocarImagem(imgEpiUf, dados.img_epizootias);
          animarTotal(totalHumanosSpan, dados.total_humanos);
          animarTotal(totalEpizootiasSpan, dados.total_epizootias);
        })
        .catch((erro) => console.error("Erro ao atualizar o gráfico por estado:", erro));
    }

    selectAno2.addEventListener("change", atualizarGrafico2);
    selectUf2.addEventListener("change", atualizarGrafico2);
  }
});
