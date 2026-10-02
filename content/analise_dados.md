## 1. Cruzamento de dados: casos humanos x epizootias em PNH

Além da análise do dicionário de variáveis, foi realizado um cruzamento entre as
duas tabelas do conjunto de dados — **Casos Humanos** e **Epizootias em Primatas
Não-Humanos** — a fim de comparar a evolução da Febre Amarela nas duas populações
ao longo do tempo e por localidade.

Para isso, cada registro das tabelas foi reduzido a apenas dois campos relevantes
para a comparação: o **ano** de ocorrência (`ANO_IS` para casos humanos e
`ANO_OCOR` para epizootias) e a **Unidade Federativa** (`UF_LPI` e `UF_OCOR`,
respectivamente). A partir disso, foram construídos dois painéis interativos,
exibidos logo abaixo:

- **Evolução anual:** compara, ano a ano, a quantidade de casos humanos e de
  epizootias registrados, permitindo observar se os picos de ocorrência em
  primatas não-humanos antecedem ou acompanham os picos em humanos — um indício
  importante da circulação do vírus no ciclo silvestre antes de atingir a
  população.
- **Ocorrências por estado:** compara a distribuição geográfica dos casos
  humanos e das epizootias por Unidade Federativa, com filtros de ano e de
  estado, permitindo identificar se as regiões mais afetadas em humanos
  coincidem com as regiões de maior circulação viral entre os primatas.

Os dois gráficos são construídos a partir dos mesmos arquivos JSON que
alimentam a base de dados, então os totais refletem exatamente os registros
descritos no dicionário de variáveis apresentado acima.

