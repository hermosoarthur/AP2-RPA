import requests
import sqlite3
from datetime import datetime

def criar_tabela_paises():
    conn = sqlite3.connect('paises.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS paises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_comum TEXT,
        nome_oficial TEXT,
        capital TEXT,
        continente TEXT,
        regiao TEXT,
        subregiao TEXT,
        populacao INTEGER,
        area REAL,
        moeda_nome TEXT,
        moeda_simbolo TEXT,
        idioma_principal TEXT,
        fuso_horario TEXT,
        url_bandeira TEXT,
        data_insercao TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

def extrair_dados_pais(pais):
    url = f"https://restcountries.com/v3.1/name/{pais}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()[0]
        
        moedas = data.get('currencies', {})
        moeda_nome = moeda_simbolo = "Não disponível"
        if moedas:
            primeira_moeda = list(moedas.keys())[0]
            moeda_nome = moedas[primeira_moeda].get('name', 'Não disponível')
            moeda_simbolo = moedas[primeira_moeda].get('symbol', 'Não disponível')
        
        idiomas = data.get('languages', {})
        idioma_principal = list(idiomas.values())[0] if idiomas else "Não disponível"
        
        return {
            'nome_comum': data.get('name', {}).get('common', 'Não disponível'),
            'nome_oficial': data.get('name', {}).get('official', 'Não disponível'),
            'capital': data.get('capital', ['Não disponível'])[0],
            'continente': data.get('continents', ['Não disponível'])[0],
            'regiao': data.get('region', 'Não disponível'),
            'subregiao': data.get('subregion', 'Não disponível'),
            'populacao': data.get('population', 0),
            'area': data.get('area', 0),
            'moeda_nome': moeda_nome,
            'moeda_simbolo': moeda_simbolo,
            'idioma_principal': idioma_principal,
            'fuso_horario': data.get('timezones', ['Não disponível'])[0],
            'url_bandeira': data.get('flags', {}).get('png', 'Não disponível'),
            'data_insercao': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        print(f"Erro ao buscar dados para {pais}: {str(e)}")
        return None

def inserir_pais_no_banco(pais_info):
    conn = sqlite3.connect('paises.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO paises (
        nome_comum, nome_oficial, capital, continente, regiao, subregiao, 
        populacao, area, moeda_nome, moeda_simbolo, idioma_principal, 
        fuso_horario, url_bandeira, data_insercao
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        pais_info['nome_comum'], pais_info['nome_oficial'], pais_info['capital'],
        pais_info['continente'], pais_info['regiao'], pais_info['subregiao'],
        pais_info['populacao'], pais_info['area'], pais_info['moeda_nome'],
        pais_info['moeda_simbolo'], pais_info['idioma_principal'],
        pais_info['fuso_horario'], pais_info['url_bandeira'], pais_info['data_insercao']
    ))
    
    conn.commit()
    conn.close()

def executar_parte_1():

    criar_tabela_paises()
    
    print("\n" + "="*50)
    print("EXTRAÇÃO DE DADOS DE PAÍSES VIA API")
    print("="*50)
    
    paises = []
    for i in range(3):
        pais = input(f"Digite o nome do {i+1}º país: ").strip()
        paises.append(pais)
    
    for pais in paises:
        dados_pais = extrair_dados_pais(pais)
        if dados_pais:
            inserir_pais_no_banco(dados_pais)
            print(f"✅ Dados de {pais} armazenados com sucesso!")
        else:
            print(f"❌ Não foi possível obter dados para {pais}")