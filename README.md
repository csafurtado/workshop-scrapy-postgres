# Raspagem de dados com Scrapy e armazenamento no Postgres 12


Workshop elaborado para a atividade do BRISA que envolve o uso da biblioteca Scrapy (Python) para raspagem de dados em um site e do banco de dados Postgres para salvar estes dados.


## PASSOS:

1. Configurar o ambiente:

```bash
# Instalando o gerenciador de container
sudo apt update
sudo apt install podman

# Criando o ambiente virtual e instalando as libs desejadas
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Criando as variáveis de ambienteevantando o container
cp env_local.env .env
podman-compose up --detach
```

* Caso dê erro de versão do CNI, executar o seguinte comando:
```bash
cat configs_podman.txt  > ~/.config/cni/net.d/workshop_brisa_default.conflist
```

2. Iniciar um projeto scrapy pelo comando no terminal e entrar na pasta do projeto recém criado:

```bash
scrapy startproject workshopbrisa
cd workshopbrisa
```

3. Criar os itens de dados que serão raspados no arquivo items.py

```py
from scrapy import Field, Item


class PilotosItem(Item):
    nome = Field()
    equipe  = Field()
    pais_origem = Field()
    podiums = Field()
    pontos_carreira = Field()
    campeonatos_mundiais = Field()
    data_nascimento = Field()
    bio = Field()

class EquipesItem(Item):
    nome = Field()
    nome_completo = Field()
    localizacao_base = Field()
    chefe_equipe = Field()
    chefe_tecnico = Field()
    chassis_carro = Field()
    unidade_potencia = Field()
    campeonatos_mundiais = Field()
    ano_estreia = Field()
    bio = Field()

class ResultadoCorridasItem(Item):
    grande_premio = Field()
    data = Field()
    vencedor = Field()
    equipe = Field()
    voltas = Field()
    tempo_total = Field()
```

4. Criar os arquivos que ficaram responsáveis pela raspagem dos dados (spiders ou scrapers) dentro da pasta 'spiders', acessando o site e retirando as informações

```py
# Arquivo pilotosscraper.py
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from workshopbrisa.items import PilotosItem
from deep_translator import GoogleTranslator

tradutor = GoogleTranslator(source='en', target='pt')


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
            "bio": " ".join(list(response.css('div.f1-atomic-wysiwyg p::text').getall())),
        }

        piloto_item["nome"] = info_piloto["nome"]
        piloto_item["equipe"] = info_piloto["equipe"]
        piloto_item["pais_origem"] = tradutor.translate(info_piloto["pais_origem"])
        piloto_item["podiums"] = info_piloto["podiums"]
        piloto_item["pontos_carreira"] = info_piloto["pontos_carreira"]
        piloto_item["campeonatos_mundiais"] = info_piloto["campeonatos_mundiais"]
        piloto_item["data_nascimento"] = info_piloto["data_nascimento"]
        piloto_item["bio"] = tradutor.translate(info_piloto["bio"])
        
        return piloto_item


# Arquivo pequipesscraper.py
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from workshopbrisa.items import EquipesItem
from deep_translator import GoogleTranslator

tradutor = GoogleTranslator(source='en', target='pt')


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
        equipe_item["bio"] = tradutor.translate(info_equipe["bio"])

        return equipe_item


# Arquivo presultados_corridasscraper.py
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
            item["vencedor"] = f"{linha.css('td:nth-child(4) span.hide-for-tablet::text').get()} {linha.css('td:nth-child(4) span.hide-for-mobile::text').get()}"
            item["equipe"] = linha.css('td:nth-child(5)::text').get()
            item["voltas"] = linha.css('td:nth-child(6)::text').get()
            item["tempo_total"] = linha.css('td:nth-child(7)::text').get()

            yield item

```

5. Criar o arquivo pipeline.py que fará o tratamento dos dados coletados em cada raspador e o salvamento no banco de dados 
(um pipeline será utilizado na execução de qualquer raspador)

```py
from itemadapter import ItemAdapter
import psycopg2
import dotenv, os
from datetime import datetime
from workshopbrisa.items import *

dotenv.load_dotenv('../.env')


class WorkshopbrisaPipeline:
    def open_spider(self, spider):
        # Cria a conexão com o banco de dados ao iniciar o raspador e já cria o cursor
        self.connection = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )

        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        
        if isinstance(item, PilotosItem):
            
            if item["nome"] is None:
                return
            
            self.cursor.execute('''
                INSERT INTO pilotos (\
                    nome, equipe, pais_origem, podiums, \
                    pontos_carreira, campeonatos_mundiais, data_nascimento, bio) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                item['nome'],
                item['equipe'],
                item['pais_origem'],
                int(item['podiums']),
                float(item['pontos_carreira']),
                int(item['campeonatos_mundiais']),
                datetime.strptime(item["data_nascimento"], '%d/%m/%Y').date(),
                item['bio'],
            ))

        elif isinstance(item, EquipesItem):
            if item["nome"] is None:
                return
            
            self.cursor.execute('''
            INSERT INTO equipes (\
                nome, nome_completo, localizacao_base, chefe_equipe, chefe_tecnico, \
                chassis_carro, unidade_potencia, campeonatos_mundiais, ano_estreia, bio) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
            item['nome'],
            item['nome_completo'],
            item['localizacao_base'],
            item['chefe_equipe'],
            item['chefe_tecnico'],
            item['chassis_carro'],
            item['unidade_potencia'],
            int(item["campeonatos_mundiais"]),
            int(item["ano_estreia"]),
            item['bio'],
            ))

        else:
            if item["vencedor"] is None:
                return
            
            self.cursor.execute('''
            INSERT INTO resultados_corridas \
                (grande_premio, data_gp, piloto_vencedor, equipe, voltas, tempo_total) \
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (
            str(item['grande_premio']),
            datetime.strptime(item['data'], '%d %b %Y').date(),
            item['vencedor'],
            item['equipe'],
            int(item['voltas']),
            f"0 {item['tempo_total']}"
            ))

        self.connection.commit()
        
        return item

```
6. Configurar o `settings.py` para utilizar a pipeline criada:
```py
# No settings.py

# (...)

# Set spiders configurations
ITEM_PIPELINES = {
    'workshopbrisa.pipelines.WorkshopbrisaPipeline': 300,
}
```

7. Fazer a raspagem de cada item (pilotos, equipes e resultados de corridas) pelo comando `scrapy crawl <nome_definido_no_raspador>` na base da pasta workshopbrisa (projeto scrapy)

8. Fazer a consulta dos dados executando o script `main.py` localizado na base do projeto.
