from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import logging

#Pegando a tabela  dos produtos
tb_buscas = pd.read_excel(r'C:\Users\user\Desktop\Projeto 2\buscas.xlsx')

#Criando o navegador

nav = webdriver.Chrome()

def verificar_tem_termo_banido(lista_termos_banidos, nome) -> bool:
    for palavra in lista_termos_banidos:
        if palavra in nome:
            return True
    return False

def verificar_tem_todos_termos_produto(lista_termos_nomes_produtos, nome) -> bool :
    for palavra in lista_termos_nomes_produtos:
        if palavra not in nome:
            return False
    return True

# Funções para ambos sites

def google_shopping(nav, produto, termos_banidos, preco_maximo, preco_minimo) -> int | str:
    
    #Tratamentos de dados
    produto = produto.lower()
    termos_banidos = termos_banidos.lower()
    lista_termos_banidos = termos_banidos.split(" ")
    lista_termos_nomes_produtos = produto.split(" ")
    preco_maximo = float(preco_maximo)
    preco_minimo = float(preco_minimo)


    
    #Lista dos ofertas 
    lista_ofertas = []

    #Acessando o google
    nav.get('https://www.google.com.br')
    inputGoogle = nav.find_element(By.NAME, "q")
    inputGoogle.send_keys(produto, Keys.ENTER)
    
    # Selecionando Shopping no google
    WebDriverWait(nav, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Shopping"))
    ).click()

    # Pegando as informações do produto
    WebDriverWait(nav, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "i0X6df"))
    )

    resultados = nav.find_elements(By.CLASS_NAME, "i0X6df")
    for resultado in resultados:
        nome = resultado.find_element(By.CLASS_NAME, "tAxDx").text.lower()

        #Analisar o filtro para termo banido
        
        tem_termo_banido = verificar_tem_termo_banido(lista_termos_banidos, nome)
            
        #Analisar o filtro para os termos do produto
        tem_todos_termos_produto = verificar_tem_todos_termos_produto(lista_termos_nomes_produtos, nome)

        # Selecionar os elementos corretos e verificados 

        if not tem_termo_banido and tem_todos_termos_produto :
            preco = resultado.find_element(By.CLASS_NAME, "a8Pemb").text
            preco = preco.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
            try:
                preco = float(preco)
            except NoSuchElementException:
                print(f"Erro no valor do produto : {nome}")
                continue

            if preco_minimo <= preco <= preco_maximo:
                link = resultado.find_element(By.XPATH, ".//a[contains(@class, 'shntl')]").get_attribute("href")
                lista_ofertas.append((nome, preco, link))


    return lista_ofertas    

def buscape(nav, produto, termos_banidos, preco_maximo, preco_minimo, ) -> int | str:
    #Tratamentos de dados

    produto = produto.lower()
    termos_banidos = termos_banidos.lower()
    lista_termos_banidos = termos_banidos.split(" ")
    lista_termos_nomes_produtos = produto.split(" ")
    preco_maximo = float(preco_maximo)
    preco_minimo = float(preco_minimo)
    

    #Acessando o buscape

    nav.get('https://www.buscape.com.br')

    
    inputBuscape = nav.find_element(By.CLASS_NAME, "AutoCompleteStyle_input__WAC2Y")
    inputBuscape.send_keys(produto, Keys.ENTER)
    

    # Pegando as informações do produto
    try:  
        WebDriverWait(nav, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'Select_Select__1HNob'))
        )
    except:
        print(F"Não foi possível encontrar resultados para o produto {nome} no Buscapé ! ")
        return []


    #Lista dos ofertas 
    lista_ofertas = []

    resultados = nav.find_elements(By.CLASS_NAME, 'ProductCard_ProductCard_Inner__gapsh')

    #Texto de erro
    for resultado in resultados:

        nome = resultado.find_element(By.CLASS_NAME, 'ProductCard_ProductCard_Name__U_mUQ').text
        nome = nome.lower()

        #Analisar o filtro para termo banido
        tem_termo_banido = verificar_tem_termo_banido(lista_termos_banidos, nome)
            

        #Analisar o filtro para os termos do produto
        tem_todos_termos_produto = verificar_tem_todos_termos_produto(lista_termos_nomes_produtos, nome)
            

        # Selecionar os elementos corretos e verificados 

        if tem_termo_banido == False and tem_todos_termos_produto :
            preco = resultado.find_element(By.CLASS_NAME, 'Text_MobileHeadingS__HEz7L').text
            preco = preco.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
            try:
                preco = float(preco)
            except ValueError:
                print(f"Erro no valor do produto {nome}")

            if preco_minimo <= preco <= preco_maximo:
                
                try:
                    link = resultado.get_attribute('href')
                    lista_ofertas.append((nome, preco, link))
                except NoSuchElementException:
                    logging.error(f"Erro no seguinte produto : {nome}")
                
    return lista_ofertas    

# Loop para verificar cada linha da tabela 

tabela_ofertas = pd.DataFrame()

for linha in tb_buscas.index:

    produto = tb_buscas.loc[linha, "Nome"]
    termos_banidos = tb_buscas.loc[linha, "Termos banidos"]
    preco_minimo = tb_buscas.loc[linha, "Preço mínimo"]
    preco_maximo = tb_buscas.loc[linha, "Preço máximo"]
    
    lista_ofertas_google_shopping = google_shopping(nav, produto, termos_banidos, preco_maximo, preco_minimo)
    if lista_ofertas_google_shopping:
        tabela_google_shopping = pd.DataFrame(lista_ofertas_google_shopping, columns=['produto', 'preco', 'link']) # Cria-se uma nova tabela em basa da função do Google Shopping
        tabela_ofertas = pd.concat([tabela_ofertas, tabela_google_shopping]) # Concatena a tabela criada com a tabela_ofertas
    else:
        tabela_google_shopping = None
        
    lista_ofertas_buscape = buscape(nav, produto, termos_banidos, preco_maximo, preco_minimo)
    if lista_ofertas_buscape:
        tabela_buscape = pd.DataFrame(lista_ofertas_buscape, columns=['produto', 'preco', 'link']) # Cria-se uma nova tabela em base da função do Buscapé
        tabela_ofertas = pd.concat([tabela_ofertas, tabela_buscape]) # Concatena a tabela criada com a tabela_ofertas
    else:
        tabela_buscape = None
     
# Exportando a tabela para um arquivo excel

tabela_ofertas = tabela_ofertas.reset_index(drop=True)
tabela_ofertas.to_excel('tabela_ofertas.xlsx', index=False)
