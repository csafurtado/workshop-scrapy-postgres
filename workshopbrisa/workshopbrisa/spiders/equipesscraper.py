from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from workshopbrisa.items import EquipesItem


class EquipesScraper(CrawlSpider):
    name = "equipes_scraper"
    start_urls = ["https://www.formula1.com/en/teams.html"]

    rules = (
        Rule(LinkExtractor(restrict_css="div.flex.flex-col.tablet\\:grid.tablet\\:grid-cols-12 a.outline.outline-offset-4.outline-brand-black.group"), callback="parse_equipes"),
    )

    def parse_equipes(self, response):
        equipe_item = EquipesItem()

        # Encontrando a <dl> com a classe específica
        dl_elements = response.css('dl.grid.gap-x-normal.gap-y-xs.f1-grid.grid-cols-1.tablet\\:grid-cols-2.items-baseline')

        # Extraindo todos os <dd> dentro da <dl> específica
        dd_elements = dl_elements.css('dd::text').getall()

        info_equipe = {
            "nome": response.css('div.f1-container.container.f1-utils-flex-container h1.f1-heading.tracking-normal::text').get(), 
            "nome_completo": dd_elements[0],
            "localizacao_base": dd_elements[1],
            "chefe_equipe": dd_elements[2],
            "chefe_tecnico": dd_elements[3],
            "chassis_carro": dd_elements[4],
            "unidade_potencia": dd_elements[5],
            "ano_estreia": dd_elements[6],
            "campeonatos_mundiais": dd_elements[7],
            "bio": response.css('div.f1-atomic-wysiwyg p::text').getall()[0],
        }
        
        print(dd_elements)

        # Exemplo de como capturar outros campos (ajustar de acordo com a estrutura real)
        equipe_item["nome"] = info_equipe["nome"]
        equipe_item["nome_completo"] = info_equipe["nome_completo"]
        equipe_item["localizacao_base"] = info_equipe["localizacao_base"]
        equipe_item["chefe_equipe"] = info_equipe["chefe_equipe"]
        equipe_item["chefe_tecnico"] = info_equipe["chefe_tecnico"]
        equipe_item["chassis_carro"] = info_equipe["chassis_carro"]
        equipe_item["unidade_potencia"] = info_equipe["unidade_potencia"]
        equipe_item["campeonatos_mundiais"] = info_equipe["campeonatos_mundiais"]
        equipe_item["ano_estreia"] = info_equipe["ano_estreia"]
        equipe_item["bio"] = info_equipe["bio"]

        return equipe_item

