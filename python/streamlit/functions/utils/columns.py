traducao_variaveis = {
    'id': 'ID',
    'date': 'Data',
    'confirmed': 'Casos Confirmados',
    'deaths': 'Mortes',
    'recovered': 'Recuperados',
    'tests': 'Testes Realizados',
    'vaccines': 'Vacinas Aplicadas',
    'people_vaccinated': 'Pessoas Vacinadas',
    'people_fully_vaccinated': 'Pessoas Totalmente Vacinadas',
    'hosp': 'Hospitalizações',
    'icu': 'Unidades de Terapia Intensiva (UTI)',
    'vent': 'Ventiladores',
    'school_closing': 'Fechamento de Escolas',
    'workplace_closing': 'Fechamento de Locais de Trabalho',
    'cancel_events': 'Cancelamento de Eventos',
    'gatherings_restrictions': 'Restrições a Aglomerações',
    'transport_closing': 'Fechamento de Transporte Público',
    'stay_home_restrictions': 'Restrições de Ficar em Casa',
    'internal_movement_restrictions': 'Restrições de Movimentação Interna',
    'international_movement_restrictions': 'Restrições de Movimentação Internacional',
    'information_campaigns': 'Campanhas de Informação',
    'testing_policy': 'Política de Testagem',
    'contact_tracing': 'Rastreamento de Contatos',
    'facial_coverings': 'Uso de Máscaras Faciais',
    'vaccination_policy': 'Política de Vacinação',
    'elderly_people_protection': 'Proteção de Idosos',
    'government_response_index': 'Índice de Resposta do Governo',
    'stringency_index': 'Índice de Restrição',
    'containment_health_index': 'Índice de Contenção da Saúde',
    'economic_support_index': 'Índice de Apoio Econômico',
    'administrative_area_level': 'Nível de Área Administrativa',
    'administrative_area_level_1': 'Área Administrativa de Nível 1',
    'administrative_area_level_2': 'Área Administrativa de Nível 2',
    'administrative_area_level_3': 'Área Administrativa de Nível 3',
    'latitude': 'Latitude',
    'longitude': 'Longitude',
    'population': 'População'
}

def getVariableTranslation(varName):
    return traducao_variaveis[varName]

def getVariableKey(varName):
    return list(traducao_variaveis.keys())[list(traducao_variaveis.values()).index(varName)]

def getVariableTranslationList(varList):
    return [traducao_variaveis[varName] for varName in varList]

def getVariableKeyList(varList):
    return [list(traducao_variaveis.keys())[list(traducao_variaveis.values()).index(varName)] for varName in varList]

def getAllVariablesTranslation():
    return traducao_variaveis.values()