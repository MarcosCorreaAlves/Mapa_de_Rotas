"""
Script de teste do sistema
Testa as funcionalidades principais sem interação do usuário
"""

from grafo import Grafo, Vertice
from dijkstra import Dijkstra
from gerador_pesos import GeradorPesos
from persistencia import SistemaPersistencia


def teste_criar_grafo():
    """Testa criação de grafo"""
    print("\n=== Teste 1: Criação de Grafo ===")
    grafo = Grafo()
    
    # Adiciona vértices
    v1 = Vertice('A', 'Centro', 0, 0)
    v2 = Vertice('B', 'Shopping', 1, 0)
    v3 = Vertice('C', 'Hospital', 2, 0)
    
    grafo.adicionar_vertice(v1)
    grafo.adicionar_vertice(v2)
    grafo.adicionar_vertice(v3)
    
    # Adiciona arestas
    grafo.adicionar_aresta('A', 'B', 5, 'Trânsito moderado')
    grafo.adicionar_aresta('B', 'C', 3, 'Trânsito livre')
    grafo.adicionar_aresta('A', 'C', 10, 'Trânsito intenso')
    
    print(f"Vértices: {len(grafo.vertices)}")
    print(f"Arestas: {len(grafo.obter_todas_arestas())}")
    print("✅ Teste de criação de grafo passou!")
    
    return grafo


def teste_dijkstra(grafo):
    """Testa algoritmo de Dijkstra"""
    print("\n=== Teste 2: Algoritmo de Dijkstra ===")
    dijkstra = Dijkstra(grafo)
    
    caminho, custo, detalhes = dijkstra.calcular_menor_caminho('A', 'C')
    
    print(f"Caminho: {' -> '.join(caminho)}")
    print(f"Custo total: {custo}")
    print(f"Número de passos: {len(detalhes)}")
    
    assert caminho == ['A', 'B', 'C'], "Caminho incorreto!"
    assert custo == 8, "Custo incorreto!"
    
    print("✅ Teste de Dijkstra passou!")


def teste_gerador_pesos():
    """Testa gerador de pesos"""
    print("\n=== Teste 3: Gerador de Pesos ===")
    
    # Gera 10 pesos aleatórios
    pesos_gerados = []
    for i in range(10):
        peso, motivo = GeradorPesos.gerar_peso_e_motivo()
        pesos_gerados.append((peso, motivo))
        print(f"{i+1}. Peso: {peso:3d} - {motivo}")
    
    # Verifica se os pesos estão no intervalo esperado
    for peso, motivo in pesos_gerados:
        assert peso >= 1, "Peso muito baixo!"
        assert isinstance(motivo, str), "Motivo deve ser string!"
    
    print("✅ Teste de gerador de pesos passou!")


def teste_persistencia():
    """Testa sistema de persistência"""
    print("\n=== Teste 4: Sistema de Persistência ===")
    
    persistencia = SistemaPersistencia('dados_teste')
    
    # Cria grafo padrão
    grafo = persistencia.criar_grafo_padrao()
    print(f"Grafo padrão criado com {len(grafo.vertices)} vértices")
    
    # Gera pesos
    GeradorPesos.gerar_pesos_para_grafo(grafo)
    
    # Salva
    persistencia.salvar_grafo_estrutura(grafo)
    persistencia.salvar_pesos_atuais(grafo)
    print("Grafo salvo com sucesso")
    
    # Carrega
    grafo_carregado = persistencia.carregar_grafo_estrutura()
    persistencia.carregar_pesos_atuais(grafo_carregado)
    print(f"Grafo carregado com {len(grafo_carregado.vertices)} vértices")
    
    assert len(grafo.vertices) == len(grafo_carregado.vertices), "Número de vértices diferente!"
    
    print("✅ Teste de persistência passou!")
    
    return grafo_carregado


def teste_caminho_completo(grafo):
    """Testa cálculo de caminho no grafo completo"""
    print("\n=== Teste 5: Caminho Completo no Grafo Padrão ===")
    
    dijkstra = Dijkstra(grafo)
    
    # Testa alguns caminhos
    testes = [
        ('A', 'J'),  # Centro para Aeroporto
        ('G', 'C'),  # Parque para Hospital
        ('D', 'I'),  # Escola para Biblioteca
    ]
    
    for origem, destino in testes:
        caminho, custo, detalhes = dijkstra.calcular_menor_caminho(origem, destino)
        origem_nome = grafo.vertices[origem].nome
        destino_nome = grafo.vertices[destino].nome
        
        if caminho:
            print(f"\n{origem_nome} -> {destino_nome}:")
            print(f"  Caminho: {' -> '.join(caminho)}")
            print(f"  Custo: {custo}")
        else:
            print(f"\n{origem_nome} -> {destino_nome}: Sem caminho disponível")
    
    print("\n✅ Teste de caminho completo passou!")


def executar_todos_testes():
    """Executa todos os testes"""
    print("\n" + "=" * 70)
    print("          EXECUTANDO TESTES DO SISTEMA")
    print("=" * 70)
    
    try:
        # Teste 1: Criar grafo simples
        grafo_simples = teste_criar_grafo()
        
        # Teste 2: Dijkstra no grafo simples
        teste_dijkstra(grafo_simples)
        
        # Teste 3: Gerador de pesos
        teste_gerador_pesos()
        
        # Teste 4: Persistência
        grafo_completo = teste_persistencia()
        
        # Teste 5: Caminho completo
        teste_caminho_completo(grafo_completo)
        
        print("\n" + "=" * 70)
        print("          ✅ TODOS OS TESTES PASSARAM!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ ERRO NO TESTE: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    executar_todos_testes()
