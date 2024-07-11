import os, dotenv, platform, psycopg2

dotenv.load_dotenv('.env')


class MenuInterativo:
    def __init__(self):
        # Cria a conexão com o banco de dados ao iniciar o menu
        self.connection = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )

        self.cursor = self.connection.cursor()

    def limpar_terminal(self):
        sistema_operacional = platform.system()
        if sistema_operacional == "Windows":
            os.system('cls')
        else:
            os.system('clear')

    def ver_info_piloto(self):
        self.limpar_terminal()
        piloto = input("Digite o nome do piloto: ")
        
        self.cursor.ex
        # Código para exibir as informações do piloto
        print(f"Exibindo informações do piloto {piloto}")
        input("\nPressione Enter para voltar ao menu...")

    def ver_info_equipe(self):
        self.limpar_terminal()
        equipe = input("Digite o nome da equipe: ")
        # Código para exibir as informações da equipe
        print(f"Exibindo informações da equipe {equipe}")
        input("\nPressione Enter para voltar ao menu...")

    def ver_grid_atual(self):
        self.limpar_terminal()
        # Código para exibir os pilotos ou equipes atuais do grid
        print("Exibindo pilotos e equipes atuais do grid")
        input("\nPressione Enter para voltar ao menu...")

    def ver_vitorias_piloto(self):
        self.limpar_terminal()
        piloto = input("Digite o nome do piloto: ")
        # Código para exibir a quantidade de vitórias do piloto
        self.cursor.execute(
                        '''
                        SELECT count(piloto_vencedor) FROM resultados_corridas 
                        WHERE piloto_vencedor = (%s);
                        ''', (piloto,)
                        )
        
        result = self.cursor.fetchone()
        
        print(f"Exibindo a quantidade de vitórias do piloto {piloto}: {result[0]}")
        input("\nPressione Enter para voltar ao menu...")

    def menu(self):
        while True:
            self.limpar_terminal()
            print("+-------------------------------+")
            print("|           Menu de escolhas           |")
            print("+-------------------------------+")
            print("| 1- Ver informação de um piloto         |")
            print("| 2- Ver informação de uma equipe        |")
            print("| 3- Ver pilotos ou equipes atuais do Grid |")
            print("| 4- Ver quantidade de vitórias de um piloto |")
            print("| 5- Sair                         |")
            print("+-------------------------------+")

            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                self.ver_info_piloto()
            elif escolha == '2':
                self.ver_info_equipe()
            elif escolha == '3':
                self.ver_grid_atual()
            elif escolha == '4':
                self.ver_vitorias_piloto()
            elif escolha == '5':
                self.limpar_terminal()
                print("Saindo...")
                break
            else:
                self.limpar_terminal()
                print("Opção inválida. Por favor, escolha novamente.")
                input("\nPressione Enter para voltar ao menu...")


