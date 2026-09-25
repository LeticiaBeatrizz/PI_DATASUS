Um dos conjuntos de dados escolhidos para este Projeto Integrador (PI) se intitula
**"Febre Amarela em humanos e primatas não-humanos - 1994 a 2025"**, disponibilizado
pelo Ministério da Saúde através do Portal de Dados Abertos do SUS e acessado em 27 de Agosto de 2026. A escolha desta
temática se deu em razão da tecnologia consolidada e da longa base de dados disponível,
o que oferece maior embasamento para análises e mais flexibilidade quanto à área a ser
pesquisada, além de permitir uma integração com as ciências biológicas, já que o vírus
também atinge primatas não-humanos. 

## 1. Análise do dicionário de variáveis

O dicionário de dados se demonstrou bastante curto, possuindo apenas 26 entradas,
divididas entre **"Casos Humanos"** e **"Epizootias em primatas não-humanos"**, com
siglas intuitivas quanto às suas descrições.

Um ponto interessante é a forma como os dados são distribuídos ao longo do tempo.
Diferentemente do convencional — em que o monitoramento se distribui entre janeiro e
dezembro — neste conjunto de dados o monitoramento se dá de junho de um determinado
ano a julho do ano seguinte. Essa escolha de período ocorre em razão do período sazonal
de transmissão, método adotado pelo Ministério da Saúde desde o ano de 2008.

### 1.1 Casos humanos

A tabela de casos humanos possui 15 variáveis, cujos nomes são definidos a partir da
sigla que os compõem.

| Variável | Significado | Definição
| --- | --- | --- |
| ID | Identificador sequencial único | Número que identifica o caso registrado de maneira única, ou seja, nenhum outro registro deve possuir o mesmo ID já registrado, mantendo assim a integridade do banco de dados. |
| MACRORREG_LPI | Sigla da macrorregião do local provável de infecção | Identifica em qual macrorregião — Norte (N), Nordeste (NO), Centro-Oeste (CO), Sul (S) e Sudeste (SE) — a infecção provavelmente aconteceu. Pode abrir margem para a identificação de qual macrorregião possui o maior índice de casos registrados.
| COD_UF_LPI | Código IBGE da Unidade Federada do local provável de infecção | Identificador de dois dígitos dos estados brasileiros, definido pelo IBGE. Identifica a provável Unidade Federativa em que ocorreu o caso, permitindo análises de estados com maiores índices registrados no país e/ou macrorregião. |
| UF_LPI | Sigla da Unidade Federada do local provável de infecção | Identifica nominalmente a Unidade Federativa que obteve a ocorrência, permitindo análises de estados com maiores índices registrados no país e/ou macrorregião. |
| COD_MUN_LPI | Código IBGE do município do local provável de infecção | Identificador de sete dígitos dos municípios brasileiros, definido pelo IBGE, cujos dois primeiros dígitos correspondem ao Código IBGE da Unidade Federativa. Identifica o provável município em que ocorreu o caso, permitindo análises de municípios com maiores índices registrados no país, macrorregião e/ou estado. |
| MUN_LPI | Nome do município do local provável de infecção | Identifica nominalmente o município que obteve a ocorrência, permitindo análises de municípios com maiores índices registrados no país, macrorregião e/ou estado. |
| SEXO | Sexo do indivíduo | Identifica o gênero da pessoa registrada, permitindo análises de maiores índices por gênero. |
| IDADE | Idade do indivíduo | Identifica a idade do indivíduo, permitindo perceber qual a faixa etária mais impactada pela proliferação do vírus. |
| DT_IS | Data de início dos sintomas do indivíduo (dd/mm/aaaa) | Data de início dos sintomas do indivíduo; identifica quando os sintomas iniciaram, permitindo criar estatísticas em relação às datas de maiores ocorrências. |
| SE_IS | Semana epidemiológica de início dos sintomas do indivíduo | Define numericamente a semana em que os sintomas se iniciam, permitindo estatísticas em relação às semanas de maiores ocorrências. |
| MES_IS | Mês de início dos sintomas do indivíduo | Mês de início dos sintomas do indivíduo; define numericamente o mês em que os sintomas se iniciam, permitindo estatísticas em relação aos meses de maiores ocorrências. |
| ANO_IS | Ano de início dos sintomas do indivíduo | Define o ano em que os sintomas se iniciam, permitindo estatísticas em relação aos anos de maiores ocorrências. |
| MONITORAMENTO_IS | Período de monitoramento de início dos sintomas do indivíduo | Define o período de maneira sazonal (aaaa/aaaa) em que os sintomas se iniciam, permitindo estatísticas em relação aos períodos de maiores ocorrências. |
| OBITO | Evolução para óbito | Define se o caso evoluiu para óbito, permitindo saber a estatística de quantos casos evoluem a óbito. |
| DT_OBITO | Data do óbito (dd/mm/aaaa) | Caso haja óbito, define a data em que ocorreu, permitindo saber as datas em que mais ocorreram óbitos por Febre Amarela. |


### 1.2 Epizootias em primatas não-humanos

A tabela de casos de Epizootias em primatas não-humanos possui 11 variáveis, cujos
nomes também são definidos a partir da sigla que os compõem.

| Variável | Significado | Definição |
| --- | --- | --- |
| ID | Identificador sequencial único | Número que identifica o caso registrado de maneira única, mantendo a integridade do banco de dados. |
| MACRORREG_OCOR | Sigla da macrorregião do local de ocorrência | Identifica em qual macrorregião — Norte (N), Nordeste (NO), Centro-Oeste (CO), Sul (S) e Sudeste (SE) — a infecção provavelmente aconteceu, permitindo identificar qual macrorregião possui o maior índice de casos registrados. |
| COD_UF_OCOR | Código IBGE da Unidade Federada do local de ocorrência | Identificador de dois dígitos dos estados brasileiros, definido pelo IBGE, permitindo análises de estados com maiores índices registrados no país e/ou macrorregião. |
| UF_OCOR | Sigla da Unidade Federada do local de ocorrência | Identifica nominalmente a Unidade Federativa que obteve a ocorrência, permitindo análises de estados com maiores índices registrados no país e/ou macrorregião. |
| COD_MUN_OCOR | Código IBGE do município do local de ocorrência | Identificador de sete dígitos dos municípios brasileiros, definido pelo IBGE, cujos dois primeiros dígitos correspondem ao Código IBGE da Unidade Federativa, permitindo análises de municípios com maiores índices registrados no país, macrorregião e/ou estado. |
| MUN_OCOR | Nome do município do local de ocorrência | Identifica nominalmente o município que obteve a ocorrência, permitindo análises de municípios com maiores índices registrados no país, macrorregião e/ou estado. |
| DATA_OCOR | Data da ocorrência do evento (dd/mm/aaaa) | Identifica quando os sintomas iniciaram, permitindo estatísticas em relação às datas de maiores ocorrências. |
| SE_OCOR | Semana epidemiológica de ocorrência do evento |Define numericamente a semana em que os sintomas se iniciam, permitindo estatísticas em relação às semanas de maiores ocorrências. |
| MES_OCOR | Mês de ocorrência do evento | Define numericamente o mês em que os sintomas se iniciam, permitindo estatísticas em relação aos meses de maiores ocorrências. |
| ANO_OCOR | Ano de ocorrência do evento | Define o ano em que os sintomas se iniciam, permitindo estatísticas em relação aos anos de maiores ocorrências. |
| MONITORAMENTO_OCOR | Período de monitoramento de ocorrência do evento | Define o período de maneira sazonal (aaaa/aaaa) em que os sintomas se iniciam, permitindo estatísticas em relação aos períodos de maiores ocorrências. |


## 2. Cruzamento de dados: casos humanos x epizootias em PNH

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
