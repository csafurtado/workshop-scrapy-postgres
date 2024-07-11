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

    def limpar_terminal(self):
        sistema_operacional = platform.system()
        if sistema_operacional == "Windows":
            os.system('cls')
        else:
            os.system('clear')

    def ver_info_piloto(self):
        self.limpar_terminal()
        piloto = input("Digite o nome do piloto: ")
        
        self.cursor = self.connection.cursor()

        self.cursor.execute(
                        '''
                        SELECT * FROM pilotos 
                        WHERE nome LIKE (%s);
                        ''', (f'%{piloto.capitalize()}%',)
                        )
        
        result = self.cursor.fetchone()

        if result is None:
            print(f"*******************************")
            print("Piloto não encontrado! Tente novamente!")
            print(f"*******************************")
            
        else:
            print(f"*******************************")
            print(f"Nome: {result[0]}",
                f"Equipe Atual: {result[1]}",
                f"Nascido em: {result[2]}",
                f"Podiums: {result[3]}",
                f"Pontos na carreira: {result[4]}",
                f"Campeonatos Mundiais: {result[5]}",
                f"Nascido em: {result[6]}",
                f"\nSobre: {result[7]}", sep="\n")
            print(f"*******************************")
        
        input("\nPressione Enter para voltar ao menu...")

        self.cursor.close()
               
    def ver_info_equipe(self):
        self.limpar_terminal()
        equipe = input("Digite o nome da equipe: ")
        
        self.cursor = self.connection.cursor()

        self.cursor.execute(
                        '''
                        SELECT * FROM equipes 
                        WHERE nome LIKE (%s);
                        ''', (f'%{equipe.capitalize()}%',)
                        )
        
        result = self.cursor.fetchone()

        if result is None:
            print(f"*******************************")
            print("Equipe não encontrada! Tente novamente!")
            print(f"*******************************")
            
        else:
            print(f"*******************************")
            print(f"Nome Completo: {result[1]}",
                f"Baseado em: {result[2]}",
                f"Chefe de Equipe: {result[3]}",
                f"Chefe Técnico: {result[4]}",
                f"Chassis Atual: {result[5]}",
                f"Campeonatos Mundiais: {result[6]}",
                f"Estreou em: {result[7]}",
                f"\nSobre: {result[8]}", sep="\n")
            print(f"*******************************")

        self.cursor.close()
        input("\nPressione Enter para voltar ao menu...")

    def ver_grid_atual(self):
        self.limpar_terminal()
        self.cursor = self.connection.cursor()

        self.cursor.execute(
                        '''
                        SELECT nome, equipe FROM pilotos;
                        '''
                        )
        
        result = self.cursor.fetchall()


        print(f"*******************************")

        is_tab = False

        for linha in result:
            if is_tab:
                print(f"\tPiloto: {linha[0]}\n\tEquipe: {linha[1]}")
            else:
                print(f"Piloto: {linha[0]}\nEquipe: {linha[1]}")
            
            print(f"*******************************")
            
            is_tab = not is_tab
            

        self.cursor.close()
        
        input("\nPressione Enter para voltar ao menu...")

    def ver_vitorias_piloto(self):
        self.limpar_terminal()
        piloto = input("Digite o nome do piloto: ")

        self.cursor = self.connection.cursor()
        
        self.cursor.execute(
            '''
            SELECT nome FROM pilotos
            WHERE nome LIKE (%s)
            ''', (f'%{piloto.capitalize()}%',)
        )
        
        nome_piloto = self.cursor.fetchone()[0]
        
        self.cursor.execute(
                        '''
                        SELECT grande_premio, COUNT(piloto_vencedor) 
                        FROM resultados_corridas 
                        WHERE piloto_vencedor LIKE (%s)
                        GROUP BY grande_premio;
                        ''', (f'%{piloto.capitalize()}%',)
                        )        
        
        result = self.cursor.fetchall()
        
        if len(result) == 0:
            print("*****************************")
            print("Não foram encontradas vitórias para este piloto!")
            print("*****************************\n")
        
        else:
            print("\n\n")
            print("*****************************")
            
            print(f"PILOTO: {str(nome_piloto).upper()}")
            print("==================================\n")
            for linha in result:
                print(f"{linha[0]}: {linha[1]} Vitórias")

            self.cursor.execute(
                '''
                SELECT COUNT(piloto_vencedor)
                FROM resultados_corridas 
                WHERE piloto_vencedor LIKE (%s);
                ''', (f'%{piloto.capitalize()}%',)
                )
        
            result = self.cursor.fetchone()
            
            print(f"\n=====================")
            print(f"TOTAL: {result[0]} Vitórias")
            print(f"=====================\n")

        print("*****************************")
        
        input("\n\nPressione Enter para voltar ao menu...")

        self.cursor.close()

    def encerrar(self):
        print("Saindo...")
        
        self.connection.close()
        

    def menu(self):
        while True:
            self.limpar_terminal()
            print("+---------------------------------------------+")
            print("|                   F1 INFO                   |")
            print("+---------------------------------------------+")
            print("| 1- Ver informação de um piloto              |")
            print("| 2- Ver informação de uma equipe             |")
            print("| 3- Ver pilotos ou equipes atuais do Grid    |")
            print("| 4- Ver quantidade de vitórias de um piloto  |")
            print("| 5- Sair                                     |")
            print("+---------------------------------------------+\n")

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
                self.encerrar()
                
                break
            else:
                self.limpar_terminal()
                print("Opção inválida. Por favor, escolha novamente.")
                input("\nPressione Enter para voltar ao menu...")


