from scrapy import Request
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from workshopbrisa.items import ResultadoCorridasItem
from datetime import datetime


class ResultadoCorridasScraper(CrawlSpider):
    name = "resultadoscorridas_scraper"
    
    # Definindo os anos de interesse
    anos = range(2000, datetime.now().year+1)  # Exemplo: anos de 2022 a 2024
    
    # Gerando as URLs dinamicamente
    start_urls = [f"https://www.formula1.com/en/results.html/{ano}/races.html" for ano in anos]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        # Encontrando a tabela específica
        tabela_resultados_ano = response.css('div.table-wrap table.resultsarchive-table')

        # Extraindo os dados da tabela
        for linha in tabela_resultados_ano.css('tr'):
            item = ResultadoCorridasItem()

            item["grande_premio"] = str(linha.css('td a::text').get()).strip()
            item["data"] = linha.css('td:nth-child(3)::text').get()
            item["vencedor"] = f"{linha.css('td:nth-child(4) span.hide-for-tablet::text').get().strip()} {linha.css('td:nth-child(4) span.hide-for-mobile::text').get().strip()}"
            item["equipe"] = linha.css('td:nth-child(5)::text').get()
            item["voltas"] = linha.css('td:nth-child(6)::text').get()
            item["tempo_total"] = linha.css('td:nth-child(7)::text').get()

            yield item