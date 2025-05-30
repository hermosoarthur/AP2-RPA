
from api_paises import executar_parte_1
from scraping_livros import executar_parte_2
from relatorio import executar_parte_3
from api_paises import executar_parte_1
from scraping_livros import executar_parte_2
from relatorio import executar_parte_3

def mostrar_menu():
    print("\n" + "="*50)
    print("AP2-RPA")
    print("="*50)
    print("1. Extrair dados de países via API")
    print("2. Extrair dados de livros via Web Scraping")
    print("3. Gerar relatório completo")
    print("4. Executar todas as etapas")
    print("0. Sair")
    print("="*50)

def main():
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            executar_parte_1()
        elif opcao == "2":
            executar_parte_2()
        elif opcao == "3":
            executar_parte_3()
        elif opcao == "4":
            executar_parte_1()
            executar_parte_2()
            executar_parte_3()
        elif opcao == "0":
            print("\nEncerrando o programa...")
            break
        else:
            print("\n❌ Opção inválida! Por favor, tente novamente.")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()