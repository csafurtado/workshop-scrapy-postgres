from scrapy import Field, Item


class AnuncioDFItem(Item):
    tipo = Field()
    valor = Field()
    qtd_quartos = Field()
    qtd_vagas = Field()
    descricao = Field()
    avaliacao = Field()
    endereco = Field()
    nome_anunciante = Field()

class AnuncianteDFItem(Item):
	nome = Field()
	endereco = Field()
	telefone = Field()
	saiba_mais = Field()

class WorkshopbrisaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
