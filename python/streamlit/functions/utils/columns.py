# Dicionário de tradução de nomes de variáveis
traducao_variaveis = {
    'id': 'ID',
    'date': 'Data',
    'confirmed': 'Confirmados',
    'deaths': 'Mortes',
    'recovered': 'Recuperados',
    'tests': 'Testes Realizados',
    'vaccines': 'Doses de Vacina',
    'people_vaccinated': 'Pessoas Vacinadas (Pelo Menos uma Dose)',
    'people_fully_vaccinated': 'Pessoas Totalmente Vacinadas',
    'hosp': 'Hospitalizados',
    'icu': 'Em UTI',
    'vent': 'Com Ventilação Invasiva',
    'population': 'População',
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
    'administrative_area_level': 'Nível da Área Administrativa',
    'administrative_area_level_1': 'Área Administrativa de Nível 1',
    'administrative_area_level_2': 'Área Administrativa de Nível 2',
    'administrative_area_level_3': 'Área Administrativa de Nível 3'
}

variaveis = [
    'confirmed',
    'deaths',
    'recovered',
    'tests',
    'vaccines',
    'people_vaccinated',
    'people_fully_vaccinated',
    'hosp',
    'icu',
    'vent'
]

essenciais = [
    'id',
    'date',
    'administrative_area_level_1',
    'administrative_area_level_2',
    'administrative_area_level_3',
]

outros = [
    'population',
    'government_response_index',
    'stringency_index',
    'containment_health_index',
    'economic_support_index'
]

medidas = [
    'school_closing',
    'workplace_closing',
    'cancel_events',
    'gatherings_restrictions',
    'transport_closing',
    'stay_home_restrictions',
    'internal_movement_restrictions',
    'international_movement_restrictions',
    'information_campaigns',
    'testing_policy',
    'contact_tracing',
    'facial_coverings',
    'vaccination_policy',
    'elderly_people_protection'
]

# Dicionário para traduzir variáveis enum
traducao_variaveis_enum = {
    'school_closing': {
        0: 'Nenhuma medida',
        1: 'Recomendar fechamento ou abrir com alterações',
        2: 'Exigir fechamento (apenas alguns níveis ou categorias)',
        3: 'Exigir fechamento de todos os níveis'
    },
    'workplace_closing': {
        0: 'Nenhuma medida',
        1: 'Recomendar fechamento (ou recomendar trabalho em casa)',
        2: 'Exigir fechamento (ou trabalho em casa) para alguns setores ou categorias de trabalhadores',
        3: 'Exigir fechamento (ou trabalho em casa) para todos os locais, exceto essenciais'
    },
    'cancel_events': {
        0: 'Nenhuma medida',
        1: 'Recomendar cancelamento',
        2: 'Exigir cancelamento'
    },
    'gatherings_restrictions': {
        0: 'Nenhuma restrição',
        1: 'Restrições em grandes aglomerações (limite acima de 1000 pessoas)',
        2: 'Restrições em aglomerações de 101-1000 pessoas',
        3: 'Restrições em aglomerações de 11-100 pessoas',
        4: 'Restrições em aglomerações de 10 pessoas ou menos'
    },
    'transport_closing': {
        0: 'Nenhuma medida',
        1: 'Recomendar fechamento (ou redução significativa do volume/rota/meios de transporte disponíveis)',
        2: 'Exigir fechamento (ou proibir a maioria dos cidadãos de usá-lo)'
    },
    'stay_home_restrictions': {
        0: 'Nenhuma medida',
        1: 'Recomendar não sair de casa',
        2: 'Exigir não sair de casa com exceções para exercício diário, compras de supermercado e viagens essenciais',
        3: 'Exigir não sair de casa com exceções mínimas (por exemplo, permitido sair uma vez por semana, ou apenas uma pessoa pode sair por vez, etc.)'
    },
    'internal_movement_restrictions': {
        0: 'Nenhuma medida',
        1: 'Recomendar não viajar entre regiões/cidades',
        2: 'Restrições à movimentação interna em vigor'
    },
    'international_movement_restrictions': {
        0: 'Nenhuma restrição',
        1: 'Rastreamento de chegadas',
        2: 'Quarentena para chegadas de algumas ou todas as regiões',
        3: 'Proibição de chegadas de algumas regiões',
        4: 'Proibição de todas as regiões ou fechamento total da fronteira'
    },
    'information_campaigns': {
        0: 'Nenhuma campanha pública de informações sobre a COVID-19',
        1: 'Autoridades públicas recomendam cautela em relação à COVID-19',
        2: 'Campanha coordenada de informações públicas (por exemplo, através da mídia tradicional e social)'
    },
    'testing_policy': {
        0: 'Nenhuma política de testagem',
        1: 'Somente para aqueles que têm sintomas E atendem a critérios específicos (por exemplo, trabalhadores-chave, admitidos no hospital, entraram em contato com um caso conhecido, retornaram do exterior)',
        2: 'Testagem de qualquer pessoa com sintomas de COVID-19',
        3: 'Testagem pública aberta (por exemplo, testagem "drive-through" disponível para pessoas assintomáticas)'
    },
    'contact_tracing': {
        0: 'Nenhum rastreamento de contatos',
        1: 'Rastreamento de contatos limitado; não é feito para todos os casos',
        2: 'Rastreamento de contatos abrangente; feito para todos os casos identificados'
    },
    'facial_coverings': {
        0: 'Sem política',
        1: 'Recomendado',
        2: 'Obrigatório em alguns espaços públicos compartilhados/fora de casa com outras pessoas presentes ou em algumas situações em que o distanciamento social não é possível',
        3: 'Obrigatório em todos os espaços públicos compartilhados fora de casa com outras pessoas presentes ou em todas as situações em que o distanciamento social não é possível',
        4: 'Obrigatório fora de casa o tempo todo, independentemente do local ou da presença de outras pessoas'
    },
    'vaccination_policy': {
        0: 'Sem disponibilidade',
        1: 'Disponibilidade para UM dos seguintes: trabalhadores-chave/grupos clinicamente vulneráveis (não idosos)/grupos idosos',
        2: 'Disponibilidade para DOIS dos seguintes: trabalhadores-chave/grupos clinicamente vulneráveis (não idosos)/grupos idosos',
        3: 'Disponibilidade para TODOS os seguintes: trabalhadores-chave/grupos clinicamente vulneráveis (não idosos)/grupos idosos',
        4: 'Disponibilidade para todos os três, mais disponibilidade parcial adicional (selecionar grupos/idades amplos)',
        5: 'Disponibilidade universal'
    },
    'elderly_people_protection': {
        0: 'Nenhuma medida',
        1: 'Isolamento recomendado, medidas de higiene e restrição de visitantes em LTCFs e/ou idosos a ficar em casa',
        2: 'Restrições limitadas para isolamento e higiene em LTCFs, algumas limitações para visitantes externos e/ou restrições de proteção de idosos em casa',
        3: 'Restrições extensas para isolamento e higiene em LTCFs, todos os visitantes externos não essenciais proibidos e/ou todos os idosos obrigados a ficar em casa e não sair de casa com exceções mínimas, e a receber visitantes externos'
    }
}

def getColumnGroups(groupName: list[str]):
    if groupName == 'variaveis':
        return variaveis
    elif groupName == 'essenciais':
        return essenciais
    elif groupName == 'medidas':
        return medidas
    elif groupName == 'outros':
        return outros
    elif groupName == 'serie_temporal':
        return variaveis + medidas

def getVariableTranslation(varName):
    return traducao_variaveis[varName]

def getVariableKey(varName):
    return list(traducao_variaveis.keys())[list(traducao_variaveis.values()).index(varName)]

def getVariableTranslationList(varList):
    return [traducao_variaveis[varName] for varName in varList]

def getVariableKeyList(varList:list|str):
    if isinstance(varList, str):
        return [list(traducao_variaveis.keys())[list(traducao_variaveis.values()).index(varList)]]
    return [list(traducao_variaveis.keys())[list(traducao_variaveis.values()).index(varName)] for varName in varList]

def getAllVariablesTranslation():
    return traducao_variaveis.values()

def getVariableTranslationDict():
    return traducao_variaveis

def getVariableEnumTranslation(varName, enumValue):
    return traducao_variaveis_enum[varName][abs(enumValue)]

def getVariableEnumTranslationList(varName):
    return traducao_variaveis_enum[varName]