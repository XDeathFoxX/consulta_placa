import time # Importamos o Time para fazer pequenas pausas na execução do programa
from playwright.sync_api import sync_playwright # Importamos o PlayWright para fazer o Scraping e retornar os dados
import re # Importamos o Regex para fazer a validação da entrada


def pesquisa_placa():
    placa = input('Digite a placa [XXX-0000] OU [XXX-0X00] : ')
    
    """ 
    Aqui usamos o Regex para validar a entrada da placa,aceitando o padrão antigo e
    o padrão mercosul
    """
    regex = re.compile('^[a-zA-Z]{3}[0-9][A-Za-z0-9][0-9]{2}$')

    while placa != 'sair': # Abrimos loop para se ocorrer erro na entrada da placa ele
                           # continue pedindo até que atenda os requisitos da entrada
        """ 
        Aqui fazemos a comparação da entrada do usuário se está no padrão Regex que
        definimos,se sim será executada a pesquisa,se não será retornada uma mensagem
        de erro para o usuário
        """
        if re.match(regex,placa):
            playwright = sync_playwright().start() # Inicamos o playwright
            navegador = playwright.firefox.launch() # Iniciamos o navegador
            site = navegador.new_page() # Criamos a página de acesso no navegador
            site.goto('https://consultarplaca.online/') # Aqui indicamos o link para acesso
            site.locator('#plate').click() # Aqui fazemos o clique no campo de placa do site
            site.locator('#plate').fill(placa) # Aqui simulamos a digitação no campo de placa
            site.locator('.main-button').click() # Aqui fazemos o clique no botão para pesquisa
            """
            Aqui fazemos a coleta dos campos que nos interessa os dados,por via do 
            CSS Selector.
            """
            chassi = site.locator('div.col-md-4:nth-child(7) > div:nth-child(1) > p:nth-child(2)')
            modelo = site.locator('div.col-md-4:nth-child(15) > div:nth-child(1) > p:nth-child(2)')
            marca = site.locator('div.col-md-4:nth-child(16) > div:nth-child(1) > p:nth-child(2)')
            cor = site.locator('div.col-md-4:nth-child(13) > div:nth-child(1) > p:nth-child(2)')
            ano_fabricacao = site.locator('div.col-md-4:nth-child(9) > div:nth-child(1) > p:nth-child(2)')
            ano_modelo = site.locator('div.col-md-4:nth-child(10) > div:nth-child(1) > p:nth-child(2)')
            cidade = site.locator('div.col-md-4:nth-child(23) > div:nth-child(1) > p:nth-child(2)')
            estado = site.locator('div.col-md-4:nth-child(24) > div:nth-child(1) > p:nth-child(2)')
            motor = site.locator('div.col-md-4:nth-child(26) > div:nth-child(1) > p:nth-child(2)')
            placa_nova = site.locator('div.col-md-4:nth-child(4) > div:nth-child(1) > p:nth-child(2)')
            situacao_placa = site.locator('div.col-md-4:nth-child(5) > div:nth-child(1) > p:nth-child(2)')
            combustivel = site.locator('div.col-md-4:nth-child(11) > div:nth-child(1) > p:nth-child(2)')
            numero_motor = site.locator('div.col-md-4:nth-child(8) > div:nth-child(1) > p:nth-child(2)')
            
            if marca.text_content() == '-': # Se não houver dados da placa ele apresenta erro
                print('Veículo não encontrado')
            # Se a placa for válida e encontrar dados no site,aqui fazemos o print 
            # dos dados que nos interessa.
            else:
                print(f'Marca: {marca.text_content()}')
                print(f'Modelo: {modelo.text_content()}')
                print(f'Ano Fabricação: {ano_fabricacao.text_content()}')
                print(f'Ano Modelo: {ano_modelo.text_content()}')
                print(f'Motor: {motor.text_content()}')
                print(f'Cor: {cor.text_content()}')
                print(f'Chassi: {chassi.text_content()}')
                #print(f'Numero Motor: {numero_motor.text_content()}')
                print(f'Combustível: {combustivel.text_content()}')
                print(f'Localidade: {cidade.text_content()} - {estado.text_content()}')

            time.sleep(2)
            navegador.close() # Aqui fechamos o navegador
            playwright.stop() # Aqui fechamos o processo do PlayWright
            consulta_nova() # Aqui perguntamos para o usuário se ele deseja fazer nova consulta
    
        else: # Aqui apresentamos a mensagem de erro se a entrada da placa for inválida
            print('')
            print('Placa inválida,digite novamente ')
            print('')
            placa = input('Digite a placa [XXX-0000] OU [XXX-0X00] : ') # Pedimos novamente a placa
            print('')
    
def consulta_nova(): # Essa função pergunta se o usuário deseja consultar novamente
                     # sem fechar o programa
    cons_nova = 0
    while cons_nova != 'sair':
        try:
            cons_nova = int(input('Deseja calcular novamente? \n1 - Sim \n2 - Não \n3 - Menu\n'))
        except ValueError:
            print('Digite apenas o número correspondente da função ')
            print('')
        else:
            if cons_nova == 1:
                pesquisa_placa()
            elif cons_nova == 2:
                print('Fechando...')
                exit()
            elif cons_nova == 3:
                print('')

pesquisa_placa()