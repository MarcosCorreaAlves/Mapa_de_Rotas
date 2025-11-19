"""
Módulo gerador_pesos.py
Gera pesos aleatórios com motivos/justificativas para as condições das ruas
"""

import random


class GeradorPesos:
    """Classe responsável por gerar pesos aleatórios com motivos"""
    
    # Definição das condições possíveis e seus pesos
    CONDICOES = [
        {
            'tipo': 'Via expressa',
            'peso_min': 1,
            'peso_max': 2,
            'probabilidade': 0.10  # 10% de chance
        },
        {
            'tipo': 'Trânsito livre',
            'peso_min': 2,
            'peso_max': 4,
            'probabilidade': 0.30  # 30% de chance
        },
        {
            'tipo': 'Trânsito moderado',
            'peso_min': 4,
            'peso_max': 7,
            'probabilidade': 0.25  # 25% de chance
        },
        {
            'tipo': 'Trânsito intenso',
            'peso_min': 7,
            'peso_max': 10,
            'probabilidade': 0.20  # 20% de chance
        },
        {
            'tipo': 'Rua em obras',
            'peso_min': 10,
            'peso_max': 15,
            'probabilidade': 0.08  # 8% de chance
        },
        {
            'tipo': 'Acidente na via',
            'peso_min': 12,
            'peso_max': 18,
            'probabilidade': 0.05  # 5% de chance
        },
        {
            'tipo': 'Rua fechada',
            'peso_min': 999,
            'peso_max': 999,
            'probabilidade': 0.02  # 2% de chance
        }
    ]
    
    @staticmethod
    def gerar_peso_e_motivo():
        """
        Gera um peso aleatório e seu motivo correspondente
        
        Returns:
            tupla (peso, motivo)
        """
        # Seleciona uma condição baseada nas probabilidades
        rand = random.random()
        acumulado = 0
        
        for condicao in GeradorPesos.CONDICOES:
            acumulado += condicao['probabilidade']
            if rand <= acumulado:
                # Gera peso dentro do intervalo da condição
                peso = random.randint(condicao['peso_min'], condicao['peso_max'])
                motivo = condicao['tipo']
                return peso, motivo
        
        # Fallback (não deveria acontecer)
        return 5, "Condição normal"
    
    @staticmethod
    def gerar_pesos_para_grafo(grafo):
        """
        Gera novos pesos aleatórios para todas as arestas do grafo
        
        Args:
            grafo: objeto Grafo a ter seus pesos atualizados
        """
        # Obtém todas as arestas
        arestas = grafo.obter_todas_arestas()
        
        # Para cada aresta, gera novo peso e motivo
        for aresta in arestas:
            peso, motivo = GeradorPesos.gerar_peso_e_motivo()
            grafo.atualizar_peso(
                aresta['origem'],
                aresta['destino'],
                peso,
                motivo,
                bidirecional=True
            )
    
    @staticmethod
    def exibir_estatisticas_condicoes():
        """Exibe as estatísticas das condições possíveis"""
        print("\n=== Condições Possíveis das Ruas ===\n")
        for condicao in GeradorPesos.CONDICOES:
            prob_percentual = condicao['probabilidade'] * 100
            print(f"• {condicao['tipo']}")
            print(f"  Peso: {condicao['peso_min']}-{condicao['peso_max']}")
            print(f"  Probabilidade: {prob_percentual:.0f}%")
            print()
