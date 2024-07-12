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
