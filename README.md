# Raspagem de dados com Scrapy e armazenamento no Postgres 12


Workshop elaborado para a atividade do BRISA que envolve o uso da biblioteca Scrapy (Python) para raspagem de dados em um site e do banco de dados Postgres para salvar estes dados.


## PASSOS:

0. Configurar o ambiente:

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