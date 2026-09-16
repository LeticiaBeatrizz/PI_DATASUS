O conjunto de dados escolhido para este Projeto Integrador (PI) se intitula
**"Febre Amarela em humanos e primatas não-humanos - 1994 a 2025"**, disponibilizado
pelo Ministério da Saúde através do Portal de Dados Abertos do SUS. A escolha desta
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
dezembro —, neste conjunto de dados o monitoramento se dá de junho de um determinado
ano a julho do ano seguinte. Essa escolha de período ocorre em razão do período sazonal
de transmissão, método adotado pelo Ministério da Saúde desde o ano de 2008.

### 1.1 Casos humanos

A tabela de casos humanos possui 15 variáveis, cujos nomes são definidos a partir da
sigla que os compõem.

| Variável | Descrição |
| --- | --- |
| ID | Identificador sequencial único |
| MACRORREG_LPI | Sigla da macrorregião do local provável de infecção |
| COD_UF_LPI | Código IBGE da Unidade Federada do local provável de infecção |
| UF_LPI | Sigla da Unidade Federada do local provável de infecção |
| COD_MUN_LPI | Código IBGE do município do local provável de infecção |
| MUN_LPI | Nome do município do local provável de infecção |
| SEXO | Sexo do indivíduo |
| IDADE | Idade do indivíduo |
| DT_IS | Data de início dos sintomas do indivíduo (dd/mm/aaaa) |
| SE_IS | Semana epidemiológica de início dos sintomas do indivíduo |
| MES_IS | Mês de início dos sintomas do indivíduo |
| ANO_IS | Ano de início dos sintomas do indivíduo |
| MONITORAMENTO_IS | Período de monitoramento de início dos sintomas do indivíduo |
| OBITO | Evolução para óbito |
| DT_OBITO | Data do óbito (dd/mm/aaaa) |

1. **ID:** identificador sequencial único; número que identifica o caso registrado de
   maneira única, ou seja, nenhum outro registro deve possuir o mesmo ID já registrado,
   mantendo assim a integridade do banco de dados.
2. **MACRORREG_LPI:** macrorregião do local provável de infecção; identifica em qual
   macrorregião — Norte (N), Nordeste (NO), Centro-Oeste (CO), Sul (S) e Sudeste (SE) —
   a infecção provavelmente aconteceu. Pode abrir margem para a identificação de qual
   macrorregião possui o maior índice de casos registrados.
3. **COD_UF_LPI:** código IBGE da Unidade Federativa do local provável de infecção;
   identificador de dois dígitos dos estados brasileiros, definido pelo IBGE. Identifica a
   provável Unidade Federativa em que ocorreu o caso, permitindo análises de estados com
   maiores índices registrados no país e/ou macrorregião.
4. **UF_LPI:** sigla da Unidade Federativa do local provável de infecção; identifica
   nominalmente a Unidade Federativa que obteve a ocorrência, permitindo análises de
   estados com maiores índices registrados no país e/ou macrorregião.
5. **COD_MUN_LPI:** código IBGE do município do local provável de infecção; identificador
   de sete dígitos dos municípios brasileiros, definido pelo IBGE, cujos dois primeiros
   dígitos correspondem ao Código IBGE da Unidade Federativa. Identifica o provável
   município em que ocorreu o caso, permitindo análises de municípios com maiores índices
   registrados no país, macrorregião e/ou estado.
6. **MUN_LPI:** nome do município do local provável de infecção; identifica nominalmente o
   município que obteve a ocorrência, permitindo análises de municípios com maiores
   índices registrados no país, macrorregião e/ou estado.
7. **SEXO:** gênero do indivíduo; identifica o gênero da pessoa registrada, permitindo
   análises de maiores índices por gênero.
8. **IDADE:** identifica a idade do indivíduo, permitindo perceber qual a faixa etária mais
   impactada pela proliferação do vírus.
9. **DT_IS:** data de início dos sintomas do indivíduo; identifica quando os sintomas
   iniciaram, permitindo criar estatísticas em relação às datas de maiores ocorrências.
10. **SE_IS:** semana epidemiológica de início dos sintomas do indivíduo; define
    numericamente a semana em que os sintomas se iniciam, permitindo estatísticas em
    relação às semanas de maiores ocorrências.
11. **MES_IS:** mês de início dos sintomas do indivíduo; define numericamente o mês em que
    os sintomas se iniciam, permitindo estatísticas em relação aos meses de maiores
    ocorrências.
12. **ANO_IS:** ano de início dos sintomas do indivíduo; define o ano em que os sintomas se
    iniciam, permitindo estatísticas em relação aos anos de maiores ocorrências.
13. **MONITORAMENTO_IS:** período de monitoramento dos sintomas do indivíduo; define o
    período de maneira sazonal (aaaa/aaaa) em que os sintomas se iniciam, permitindo
    estatísticas em relação aos períodos de maiores ocorrências.
14. **OBITO:** evolução para óbito; define se o caso evoluiu para óbito, permitindo saber a
    estatística de quantos casos evoluem a óbito.
15. **DT_OBITO:** data do óbito; caso haja óbito, define a data em que ocorreu, permitindo
    saber as datas em que mais ocorreram óbitos por Febre Amarela.

### 1.2 Epizootias em primatas não-humanos

A tabela de casos de Epizootias em primatas não-humanos possui 11 variáveis, cujos
nomes também são definidos a partir da sigla que os compõem.

| Variável | Descrição |
| --- | --- |
| ID | Identificador sequencial único |
| MACRORREG_OCOR | Sigla da macrorregião do local de ocorrência |
| COD_UF_OCOR | Código IBGE da Unidade Federada do local de ocorrência |
| UF_OCOR | Sigla da Unidade Federada do local de ocorrência |
| COD_MUN_OCOR | Código IBGE do município do local de ocorrência |
| MUN_OCOR | Nome do município do local de ocorrência |
| DATA_OCOR | Data da ocorrência do evento (dd/mm/aaaa) |
| SE_OCOR | Semana epidemiológica de ocorrência do evento |
| MES_OCOR | Mês de ocorrência do evento |
| ANO_OCOR | Ano de ocorrência do evento |
| MONITORAMENTO_OCOR | Período de monitoramento de ocorrência do evento |

1. **ID:** identificador sequencial único; número que identifica o caso registrado de
   maneira única, mantendo a integridade do banco de dados.
2. **MACRORREG_OCOR:** macrorregião do local de ocorrência; identifica em qual
   macrorregião — Norte (N), Nordeste (NO), Centro-Oeste (CO), Sul (S) e Sudeste (SE) —
   a infecção provavelmente aconteceu, permitindo identificar qual macrorregião possui o
   maior índice de casos registrados.
3. **COD_UF_OCOR:** código IBGE da Unidade Federativa do local de ocorrência;
   identificador de dois dígitos dos estados brasileiros, definido pelo IBGE, permitindo
   análises de estados com maiores índices registrados no país e/ou macrorregião.
4. **UF_OCOR:** sigla da Unidade Federativa do local de ocorrência; identifica
   nominalmente a Unidade Federativa que obteve a ocorrência, permitindo análises de
   estados com maiores índices registrados no país e/ou macrorregião.
5. **COD_MUN_OCOR:** código IBGE do município do local de ocorrência; identificador de
   sete dígitos dos municípios brasileiros, definido pelo IBGE, cujos dois primeiros
   dígitos correspondem ao Código IBGE da Unidade Federativa, permitindo análises de
   municípios com maiores índices registrados no país, macrorregião e/ou estado.
6. **MUN_OCOR:** nome do município do local de ocorrência; identifica nominalmente o
   município que obteve a ocorrência, permitindo análises de municípios com maiores
   índices registrados no país, macrorregião e/ou estado.
7. **DATA_OCOR:** data de início dos sintomas do indivíduo; identifica quando os sintomas
   iniciaram, permitindo estatísticas em relação às datas de maiores ocorrências.
8. **SE_OCOR:** semana epidemiológica de início dos sintomas do indivíduo; define
   numericamente a semana em que os sintomas se iniciam, permitindo estatísticas em
   relação às semanas de maiores ocorrências.
9. **MES_OCOR:** mês de início dos sintomas do indivíduo; define numericamente o mês em
   que os sintomas se iniciam, permitindo estatísticas em relação aos meses de maiores
   ocorrências.
10. **ANO_OCOR:** ano de início dos sintomas do indivíduo; define o ano em que os sintomas
    se iniciam, permitindo estatísticas em relação aos anos de maiores ocorrências.
11. **MONITORAMENTO_OCOR:** período de monitoramento dos sintomas do indivíduo; define o
    período de maneira sazonal (aaaa/aaaa) em que os sintomas se iniciam, permitindo
    estatísticas em relação aos períodos de maiores ocorrências.

## 2. Resultados e discussões

O dicionário da base de dados do conjunto "Febre Amarela em humanos e primatas
não-humanos - 1994 a 2025" se demonstrou bastante intuitivo de se aprender, já que suas
siglas indicam de maneira prática o que devem representar. Além disso, observa-se um
detalhamento satisfatório acerca da ambientação em que os dados são coletados, com nome
e código de identificação das localidades registradas. Isso possibilita a criação de gráficos
e mapas minuciosos em relação aos casos coletados pelo Ministério da Saúde, abrindo
margem para uma gama de possibilidades a serem trabalhadas posteriormente neste
Projeto Integrador.

## 3. Cruzamento de dados: casos humanos x epizootias em PNH

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

### Referências bibliográficas

- BRASIL. Ministério da Saúde. Secretaria de Vigilância em Saúde e Ambiente. Coordenação-Geral de Vigilância das Arboviroses. *Febre Amarela em humanos e primatas não-humanos - 1994 a 2025.* Brasília, DF: Ministério da Saúde, 2025.
- GUEDES, Maria Julia. Movimento antivacina: saiba o que é e como surgiu. *Politize!*, 24 mar. 2022.
