"""
Sistema de Mapa de Rotas de Cidades
Trabalho Prático - Estruturas de Dados Avançadas (Árvores e Grafos)
Tema 7: Mapa de Rotas de Cidades

Implementa um sistema de cálculo de menor caminho usando o algoritmo de Dijkstra,
com pesos dinâmicos que representam condições das ruas (trânsito, obras, etc.)
"""

from grafo import Grafo
from dijkstra import Dijkstra
from gerador_pesos import GeradorPesos
from visualizador import VisualizadorMapa
from persistencia import SistemaPersistencia
from interface import InterfaceUsuario


def inicializar_sistema():
    """
    Inicializa o sistema carregando ou criando o grafo
    
    Returns:
        tupla (grafo, persistencia)
    """
    print("🚀 Inicializando Sistema de Mapa de Rotas...")
    
    # Cria sistema de persistência
    persistencia = SistemaPersistencia('dados')
    
    # Tenta carregar grafo existente
    grafo = persistencia.carregar_grafo_estrutura()
    
    if grafo is None:
        print("📝 Criando novo mapa da cidade...")
        grafo = persistencia.criar_grafo_padrao()
        persistencia.salvar_grafo_estrutura(grafo)
        print("✅ Mapa criado com sucesso!")
    else:
        print("✅ Mapa carregado com sucesso!")
    
    # Tenta carregar pesos salvos, senão gera novos
    if not persistencia.carregar_pesos_atuais(grafo):
        print("🎲 Gerando pesos aleatórios iniciais...")
        GeradorPesos.gerar_pesos_para_grafo(grafo)
        persistencia.salvar_pesos_atuais(grafo)
        print("✅ Pesos gerados e salvos!")
    else:
        print("✅ Pesos carregados com sucesso!")
    
    return grafo, persistencia


def main():
    """Função principal do programa"""
    try:
        # Inicializa o sistema
        grafo, persistencia = inicializar_sistema()
        
        # Cria objetos necessários
        dijkstra = Dijkstra(grafo)
        visualizador = VisualizadorMapa(grafo)
        
        # Cria e executa interface
        interface = InterfaceUsuario(
            grafo=grafo,
            dijkstra=dijkstra,
            visualizador=visualizador,
            gerador_pesos=GeradorPesos,
            persistencia=persistencia
        )
        
        print("\n✨ Sistema pronto para uso!\n")
        input("Pressione Enter para continuar...")
        
        # Executa loop principal
        interface.executar()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Sistema interrompido pelo usuário.")
        print("👋 Até logo!")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
