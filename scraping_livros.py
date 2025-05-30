from bs4 import BeautifulSoup
import requests
import sqlite3
from datetime import datetime

def criar_tabela_livros():
    """Cria a tabela de livros no banco de dados"""
    conn = sqlite3.connect('livraria.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        preco REAL,
        avaliacao TEXT,
        disponibilidade TEXT,
        data_insercao TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

def extrair_dados_livros():
    """Extrai dados dos livros do site"""
    url = "https://books.toscrape.com/"
    try:
        response = requests.get(url, timeout=10)
        response.encoding = response.apparent_encoding  # Detecta automaticamente o encoding correto
        soup = BeautifulSoup(response.text, 'html.parser')
        livros = soup.find_all('article', class_='product_pod')[:10]
        
        dados_livros = []
        
        for livro in livros:
            titulo = livro.h3.a['title']
            
            preco_texto = livro.find('p', class_='price_color').text
            preco_limpo = ''.join(c for c in preco_texto if c.isdigit() or c == '.')

            try:
                preco = float(preco_limpo)
            except ValueError:
                preco = 0.0  # ou continue se quiser ignorar livros com preço inválido
            
            # Avaliação por estrelas
            classes_estrelas = livro.p['class']
            avaliacao = {
                'One': '1 estrela',
                'Two': '2 estrelas',
                'Three': '3 estrelas',
                'Four': '4 estrelas',
                'Five': '5 estrelas'
            }.get(classes_estrelas[1], 'Não avaliado')
            
            disponibilidade = livro.find('p', class_='instock availability').text.strip()
            
            dados_livros.append({
                'titulo': titulo,
                'preco': preco,
                'avaliacao': avaliacao,
                'disponibilidade': disponibilidade,
                'data_insercao': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return dados_livros
    except Exception as e:
        print(f"Erro ao acessar o site: {str(e)}")
        return []


def inserir_livros_no_banco(dados_livros):
    """Insere os dados dos livros no banco de dados"""
    conn = sqlite3.connect('livraria.db')
    cursor = conn.cursor()
    
    for livro in dados_livros:
        cursor.execute('''
        INSERT INTO livros (titulo, preco, avaliacao, disponibilidade, data_insercao)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            livro['titulo'], livro['preco'], livro['avaliacao'],
            livro['disponibilidade'], livro['data_insercao']
        ))
    
    conn.commit()
    conn.close()

def executar_parte_2():
    """Função principal da Parte 2"""
    criar_tabela_livros()
    
    print("\n" + "="*50)
    print("WEB SCRAPING DE LIVROS")
    print("="*50)
    
    dados_livros = extrair_dados_livros()
    
    if dados_livros:
        inserir_livros_no_banco(dados_livros)
        print("✅ Dados dos 10 primeiros livros armazenados com sucesso!")
    else:
        print("❌ Não foi possível obter dados dos livros")