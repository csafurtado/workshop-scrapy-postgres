from scrapy import Request
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from workshopbrisa.items import ResultadoCorridasItem

class ResultadoCorridasScraper(CrawlSpider):
    name = "resultadoscorridas_scraper"
    
    # Definindo os anos de interesse
    anos = range(2022, 2024)  # Exemplo: anos de 2022 a 2024
    
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
            # blabla = {
            #     'Grand Prix': linha.css('td:nth-child(0) a::text').get().strip(),
            #     'Date': linha.css('td:nth-child(1)::text').get().strip(),
            #     'Winner': linha.css('td:nth-child(2) span.hide-for-mobile::text').get().strip(),
            #     'Car': linha.css('td:nth-child(3)::text').get().strip(),
            #     'Laps': linha.css('td:nth-child(4)::text').get().strip(),
            #     'Time': linha.css('td:nth-child(5)::text').get().strip(),
            # }
            
            # print(blabla)

            # yield blabla
            item = ResultadoCorridasItem()

            # td_elementos = linha.css('td').get

            print(linha)

            # item["grande_premio"] = td_elementos[0].css('a::text').get()
            # item["data"] = td_elementos[1].get()
            # item["vencedor"] = td_elementos[2].css('span.hide-for-tablet::text').get() + " " +td_elementos[2].css('span.hide-for-mobile::text').get()
            # item["equipe"] = td_elementos[3].get()
            # item["voltas"] = td_elementos[4].get()
            # item["tempo_total"] = td_elementos[5].get()

            yield item