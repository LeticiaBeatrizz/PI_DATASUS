Ao iniciar o estudo sobre a Febre Amarela e analisar as estatísticas disponibilizadas pelo [Portal de Dados Abertos do SUS](https://dadosabertos.saude.gov.br/){target="_blank" rel="noopener"}, foi notório a necessidade de não só apenas trabalhar com a análise das ocorrências - tanto em humanos como em primatas não-humanos - e dos casos de óbitos em humanos, mas também que era preciso compreender como campanhas de vacinação afetam tais dados positivamente ou negativamente. Nesse sentido, foi decidido iniciar o estudo e análise da vacinação contra Febre Amarela no Brasil através das bases de dados denominadas de "Doses aplicadas pelo Programa de Nacional de Imunizações (PNI) - [ano]" durante os anos de 2020, 2021, 2023, 2024, 2025 e 2026, a fim de complementar nosso estudo, olhando para todas as variáveis, e assimilar de melhor maneira como a presença desse antígeno detêm influência no aumento ou diminuição de casos ao longo dos anos em diferentes regiões do território nacional. 


## 1. Dispõe da tradução do dicionário de variáveis

O dicionário da base de dados, intitulado como “Dados anonimizados dos pacientes” possui 60 variáveis com seus nomes definidos a partir da sigla que os compõem. Abaixo, há uma breve descrição das variáveis selecionadas para este projeto.


| Campo | Descrição |
|---|---|
| CO_DOCUMENTO | Código de Documento: Código do documento na Rede Nacional de Dados em Saúde (RNDS). Todo documento Fast Healthcare Interoperability Resources (FHIR) que entra na RNDS recebe um código |
| CO_PACIENTE | Código do Paciente: Código identificador do paciente. Valor atribuído na RNDS |
| TP_SEXO_PACIENTE | Descrição do sexo biológico do paciente: Identifica o sexo biológico do indivíduo que tomou a vacina, atribuindo F ou M |
| CO_RACA_COR_PACIENTE | Código que identifica a raça/cor do paciente |
| NO_RACA_COR_PACIENTE | Nome que identifica a raça/cor do paciente |
| CO_MUNICIPIO_PACIENTE | Código IBGE do município de residência do paciente, expresso por número inteiro |
| CO_PAIS_PACIENTE | Código do país de residência do paciente, expresso por número inteiro |
| NO_MUNICIPIO_PACIENTE | Nome do município de residência do paciente |
| NO_PAIS_PACIENTE | Nome do país de residência do paciente |
| SG_UF_PACIENTE | Sigla da Unidade Federativa (UF) do paciente |
| NU_CEP_PACIENTE | Nome da Unidade Federativa (UF) do paciente |
| DS_NACIONALIDADE_PACIENTE | Descrição da nacionalidade do paciente |
| ST_VIDA_PACIENTE | Status de vida do paciente. Indica se o paciente está vivo ou já foi a óbito |
| NO_ETNIA_INDIGENA_PACIENTE | Nome da etnia indígena do paciente |
| CO_ETNIA_INDIGENA_PACIENTE | Código da etnia indígena do paciente, é expresso em valor inteiro |
| CO_CNES_ESTABELECIMENTO | Código do Cadastro Nacional de Estabelecimento de Saúde (CNES) do estabelecimento |
| NO_RAZAO_SOCIAL_ESTABELECIMENTO | Nome da razão social do Estabelecimento de Saúde no CNES |
| NO_FANTASIA_ESTALECIMENTO | Nome fantasia do estabelecimento de saúde, é o apelido comercial ou título de fachada que a empresa usa para ser conhecida pelo público |
| CO_MUNICIPIO_ESTABELECIMENTO | Código IBGE do município do estabelecimento |
| NO_MUNICIPIO_ESTABELECIMENTO | Nome do município do estabelecimento |
| SG_UF_ESTABELECIMENTO | Sigla da Unidade Federativa (UF) do estabelecimento, indica o estado onde a vacina foi aplicada |
| CO_TROCA_DOCUMENTO | Código que identifica o documento que foi substituído ou alterado, ou seja, não é o original |
| CO_VACINA | Código da vacina administrada, expresso em valor inteiro |
| SG_VACINA | Sigla da vacina administrada, é a abreviação do antígeno administrado |
| DT_VACINA | Data da vacinação, indica a data em que a dose foi administrada |
| CO_DOSE_VACINA | Código da dose da vacina administrada |
| DS_DOSE_VACINA | Descrição da dose da vacina administrada |
| CO_LOCAL_APLICACAO | Código do local de aplicação da vacina, expresso em valor inteiro |
| DS_LOCAL_APLICACAO | Descrição do local de aplicação da vacina, indica a região do corpo em que a dose foi aplicada no paciente |
| CO_VIA_ADMINISTRACAO | Código da via de administração da vacina |
| DS_VIA_ADMINISTRACAO | Descrição da via de administração da vacina, indica se a vacina foi administrada de forma intramuscular, subcutânea, intradérmica ou oral |
| CO_LOTE_VACINA | Código do lote da vacina |
| DS_VACINA_FABRICANTE | Descrição do fabricante da vacina administrada, indica a empresa/laboratório |
| DT_ENTRADA_DATALAKE | Data e hora de entrada no Datalake no momento do cadastro |
| DT_ENTRADA_RNDS | Data e hora de entrada do registro na RNDS |
| CO_SISTEMA_ORIGEM | Código do sistema de origem |
| DS_SISTEMA_ORIGEM | Descrição do sistema de origem |
| CO_IDENTIFICADOR_SISTEMA | Código identificador do sistema de origem |
| ST_DOCUMENTO | Status do documento. Aponta se o documento foi substituído ou alterado ou é um registro final |
| CO_ESTRATEGIA_VACINACAO | Código da estratégia de vacinação |
| DS_ESTRATEGIA_VACINACAO | Descrição da estratégia de vacinação, indica se a dose foi administrada seguindo um calendário regular ou uma indicação específica, por exemplo, rotina (campanhas nacionais de imunização), vacinação escolar, especial (grupos clínicos específicos e com condições especiais)... |
| CO_ORIGEM_REGISTRO | Código que identifica o registro de origem como transcrição, indica de que livro, base de dados ou sistema os dados foram retirados |
| DS_ORIGEM_REGISTRO | Descrição que identifica o registro de origem como transcrição, irá indicar de qual sistema os dados vacinais foram retirados |
| CO_VACINA_GRUPO_ATENDIMENTO | Código do grupo de atendimento da vacinação, vai indicar a qual recorte social a dose foi administrada |
| DS_VACINA_GRUPO_ATENDIMENTO | Descrição do grupo de atendimento da vacinação, podem ser: Pessoas de 60 anos ou mais institucionalizadas (201), Trabalhadores da Saúde (602), Gestantes (926), Povos Indígenas vivendo em Terras Indígenas (102), Pessoas com Comorbidades (206)... |
| CO_VACINA_CATEGORIA_ATENDIMENTO | Código da categoria do grupo de atendimento da vacinação |
| DS_VACINA_CATEGORIA_ATENDIMENTO | Descrição da categoria do grupo de atendimento da vacinação |
| CO_VACINA_FABRICANTE | Código do fabricante da vacina administrada |
| DS_VACINA | Descrição da vacina administrada |
| DS_CONDICAO_MATERNAL | Descrição da condição maternal do paciente, campo de preenchimento obrigatório caso o sexo do paciente esteja definido como "feminino" ou "indeterminado". Diz respeito ao estágio em que o paciente que recebeu a vacina se encontra: "Gestante", "Nenhuma" ou "Puérpera" |
| CO_TIPO_ESTABELECIMENTO | Código do tipo de estabelecimento no CNES |
| DS_TIPO_ESTABELECIMENTO | Descrição do tipo de estabelecimento no CNES |
| CO_NATUREZA_ESTABELECIMENTO | Código da natureza do estabelecimento no CNES, se é clínica, hospital, posto de saúde... |
| DS_NATUREZA_ESTABELECIMENTO | Descrição da natureza do estabelecimento no CNES |
| NU_IDADE_PACIENTE | Idade do paciente |
| CO_CONDICAO_MATERNAL | Código da condição maternal do paciente |
| NO_UF_PACIENTE | Nome da Unidade Federativa (UF) do paciente: Sigla da UF de onde o paciente se originou |
| DT_DELETED | Data de alteração do registro: Exibe a última data em que houve alguma alteração no registro de vacinação do paciente |
| DS_IDENTIFICADOR_SISTEMA | Descrição do identificador do sistema de origem, indica qual sistema foi utilizado para postar as informações |
| NO_UF_ESTABELECIMENTO | Nome da Unidade Federativa (UF) do estabelecimento: indica o estado onde a vacina foi aplicada |

