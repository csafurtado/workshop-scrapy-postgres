from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from workshopbrisa.items import PilotosItem

class PilotosScraper(CrawlSpider):
    name = "pilotos_scraper"
    start_urls = ["https://www.formula1.com/en/drivers.html"]

    rules = (
        Rule(LinkExtractor(restrict_css="div.flex.flex-col.tablet\\:grid.tablet\\:grid-cols-12 a.outline.outline-offset-4.outline-brand-black.group"), callback="parse_pilotos"),
    )

    def parse_pilotos(self, response):
        piloto_item = PilotosItem()
        
        # Encontrando a <dl> com a classe específica
        dl_elements = response.css('dl.grid.gap-x-normal.gap-y-xs.f1-grid.grid-cols-1.tablet\\:grid-cols-2.items-baseline')

        # Extraindo todos os <dd> dentro da <dl> específica
        dd_elements = dl_elements.css('dd::text').getall()

        info_piloto = {
            "nome": response.css('div.f1-container.container.f1-utils-flex-container h1.f1-heading.tracking-normal::text').get(),
            "equipe": dd_elements[0],
            "pais_origem": dd_elements[1],
            "podiums": dd_elements[2],
            "pontos_carreira": dd_elements[3],
            "campeonatos_mundiais": dd_elements[5],
            "data_nascimento": dd_elements[8],
        }

        # Exemplo de como capturar outros campos (ajustar de acordo com a estrutura real)
        piloto_item["nome"] = info_piloto["nome"]
        piloto_item["equipe"] = info_piloto["equipe"]
        piloto_item["pais_origem"] = info_piloto["pais_origem"]
        piloto_item["podiums"] = info_piloto["podiums"]
        piloto_item["pontos_carreira"] = info_piloto["pontos_carreira"]
        piloto_item["campeonatos_mundiais"] = info_piloto["campeonatos_mundiais"]
        piloto_item["data_nascimento"] = info_piloto["data_nascimento"]
        
        return piloto_item

