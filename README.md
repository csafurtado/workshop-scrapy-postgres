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

2. Iniciar um projeto scrapy pelo comando no terminal:

```bash
scrapy startproject workshopbrisa
```

3. Criar os itens de dados que serão raspados e os spiders (raspadores) respectivos

```py
# No arquivo items.py
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
```

```py
# Criar os arquivos pilotosscraper.py, equipesscraper.py e resultados_corridasscraper.py


```
