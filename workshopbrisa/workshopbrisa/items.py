from scrapy import Field, Item


class PilotosItem(Item):
    nome = Field()
    equipe  = Field()
    pais_origem = Field()
    podiums = Field()
    pontos_carreira = Field()
    campeonatos_mundiais = Field()
    data_nascimento = Field()

class EquipesItem(Item):
    nome = Field()
    nome_completo = Field()
    localizacao_base = Field()
    chefe_equipe = Field()
    chefe_tecnico = Field()
    chassis_carro = Field()
    unidade_potencia = Field()
    campeonatos_mundiais = Field()
    data_estreia = Field()

class ResultadoCorridasItem(Item):
    grande_premio = Field()
    data = Field()
    vencedor = Field()
    equipe = Field()
    voltas = Field()
    tempo_total = Field()

