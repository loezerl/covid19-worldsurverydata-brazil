import pandas as pd
import requests
import json
import argparse
from datetime import datetime

BASE_URL = "https://covidmap.umd.edu/api/resources?"

ESTADOS = [
  'sp', 'pr', 'sc', 'rs',
  'ms', 'ro', 'ac', 'am',
  'rr', 'pa', 'ap', 'to',
  'ma', 'rn', 'pb', 'pe',
  'al', 'se', 'ba', 'mg',
  'rj', 'mt', 'go', 'df',
  'pi', 'ce', 'es',
]

REGIOES = {
  "norte": ['ac', 'ap', 'am', 'pa', 'ro', 'rr', 'to'],
  "nordeste": ['al', 'ba', 'ce', 'ma', 'pb', 'pe', 'pi', 'rn', 'se'],
  "centro-oeste": ['go', 'mt', 'ms', 'df'],
  "sudeste": ['es', 'mg', 'rj', 'sp',],
  "sul": ['pr', 'rs', 'sc'],
}

ESTADOS_MAP = {
    "sp": "São Paulo",
    "pr": "Paraná",
    "sc": "Santa Catarina",
    "rs": "Rio Grande do Sul",
    "ms": "Mato Grosso do Sul",
    "ro": "Rondônia",
    "ac": "Acre",
    "am": "Amazonas",
    "rr": "Roraima",
    "pa": "Pará",
    "ap": "Amapá",
    "to": "Tocantins",
    "ma": "Maranhão",
    "rn": "Rio Grande do Norte",
    "pb": "Paraíba",
    "pe": "Pernambuco",
    "al": "Alagoas",
    "se": "Sergipe",
    "ba": "Bahia",
    "mg": "Minas Gerais",
    "rj": "Rio de Janeiro",
    "mt": "Mato Grosso",
    "go": "Goiás",
    "df": "Distrito Federal",
    "pi": "Piauí",
    "ce": "Ceará",
    "es": "Espírito Santo"
}

INDICADORES = [
    ## Sintomas
    'covid',
    'flu',
    'anosmia', 
    'cmty_covid', 
    ############
    ## Sintomas pós-atualizacao do indicador covid
    'cli_w11',
    'ili_w11',
    ## Comportamento
    'mask',
    'contact',
    'work_outside_home_1d',
    'shop_1d',
    'restaurant_1d',
    'spent_time_1d',
    'large_event_1d',
    'public_transit_1d',
    ###############
    ## Economico
    'finance',
    #############
    ## Vacina
    'vaccine_acpt',
    'covid_vaccine',
    'trust_fam',
    'trust_healthcare',
    'trust_who',
    'trust_govt',
    'trust_politicians',
    'twodoses',
    'concerned_sideeffects',
    'hesitant_sideeffects',
    'modified_acceptance',
    'barrier_reason_side_effects',
    'barrier_reason_wontwork',
    'barrier_reason_dontbelieve',
    'barrier_reason_dontlike',
    'barrier_reason_waitlater',
    'barrier_reason_otherpeople',
    'barrier_reason_cost',
    'barrier_reason_religious',
    'barrier_reason_government',
    'barrier_reason_other',
    'trust_doctors',
    'barrier_reason_dontneed_alreadyhad',
    'barrier_reason_dontneed_dontspendtime',
    'barrier_reason_dontneed_nothighrisk',
    'barrier_reason_dontneed_takeprecautions',
    'barrier_reason_dontneed_notserious',
    'barrier_reason_dontneed_notbeneficial',
    'barrier_reason_dontneed_other',
    'informed_access',
    'appointment_have',
    'appointment_tried',
    #################
    ## Saude mental
    'anxious_7d',
    'depressed_7d',
    'worried_become_ill',
    'food_security',
    ## Outros
    'access_wash',
    'wash_hands_24h_3to6',
    'wash_hands_24h_7orMore',
    #################
    
]


def query_api(indicador, estado, deadline):
    URL = BASE_URL + f"indicator={indicador}&type=daily&country=Brazil&daterange=20200101-{deadline}&region={estado}"
    data = requests.get(URL)
    jsonobj = json.loads(data.text)
    df_e = pd.json_normalize(jsonobj['data'])
    df_e['survey_date'] = pd.to_datetime(df_e['survey_date'], format="%Y%m%d")
    return df_e

parser = argparse.ArgumentParser(
    description='Esse script tem como funcionalidade se conectar na API COVID-19 World Survery DATA e gerar um relatório ordenado temporalmente \
      com informações sobre os resultados das pesquisas com o indicador parametrizado. \
        Autor - Lucas Loezer (loezer.lucas@gmail.com)')
parser.add_argument('-i', type=str, help="Indicador. Diz respeito ao indicador da pesquisa realizada. Consultar valores possíveis em: https://covidmap.umd.edu/api.html", default="covid")
parser.add_argument('-r', type=str, help="Região. Caso queira extrair a informação de uma região do Brasil. Valores possiveis: norte, nordeste, centro-oeste, sudeste e sul.", default="")
parser.add_argument('-e', type=str, help="Estado. Informe as siglas dos estados separado por vírgula. Caso não seja informado o relatório \
  estará contabilizando todos os estados brasileiros.", default="")
parser.add_argument('-f', help="Formato de saída do relatório: [xlsx] ou [csv]", default='xlsx')
parser.add_argument('-o', type=str, help="Nome do arquivo de saída. Não é preciso informar o tipo de saída.", default="Relatorio")
args = parser.parse_args()

ESTADO = args.e.lower()
INDICADOR = args.i
REGIAO = args.r.lower()
ESTADOS_LIST = []
OUTPUT_FILE = args.o
OUTPUT_FILE_FORMAT = args.f

OUTPUT_FILE = OUTPUT_FILE + f"_{INDICADOR}"
if REGIAO in REGIOES:
    ESTADOS_LIST = [ESTADOS_MAP[e_name] for e_name in REGIOES[REGIAO]]
    print("Relatório sendo gerado para a região", REGIAO)
    OUTPUT_FILE = OUTPUT_FILE + "_{}".format(REGIAO)

if ESTADO != "":
    ESTADO = [e for e in ESTADO.split(",") if e != ""]
    for e in ESTADO:
        if e not in ESTADOS:
            raise Exception(f"Sigla {e} inválida.")
    ESTADOS_LIST = [ESTADOS_MAP[e] for e in ESTADO]
    print("Relatório sendo gerado para os seguintes estados: ")
    print(ESTADOS_LIST)
    suffx = "_"
    for e in ESTADOS_LIST:
        suffx = suffx + e + "_"
    suffx = suffx[:-1]
    OUTPUT_FILE = OUTPUT_FILE + suffx
elif len(ESTADOS_LIST) == 0:
    ESTADOS_LIST = [ESTADOS_MAP[e] for e in ESTADOS]
    print("Relatório sendo gerado para todos os estados.")
    OUTPUT_FILE = OUTPUT_FILE + "_Brasil"

if INDICADOR not in INDICADORES:
    raise Exception(f"Indicador {INDICADOR} inválido. Por favor, consulte a lista de indicadores.")

print(f"Processando {ESTADOS_LIST[0]}")
today = datetime.today().strftime('%Y%m%d')
df = query_api(INDICADOR, ESTADOS_LIST[0], today)
for estado in ESTADOS_LIST[1:]:
    print(f"Processando {estado}")
    df_e = query_api(INDICADOR, estado, today)
    df = pd.concat([df, df_e], axis=0)

df.sort_values(by='survey_date', inplace=True)


if OUTPUT_FILE_FORMAT == "xlsx":
  df.to_excel(f'{OUTPUT_FILE}.{OUTPUT_FILE_FORMAT}', index=False)
elif OUTPUT_FILE_FORMAT == "csv":
  df.to_csv(f'{OUTPUT_FILE}.{OUTPUT_FILE_FORMAT}', index=False, sep=';')