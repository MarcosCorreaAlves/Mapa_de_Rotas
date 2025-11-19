"""
Módulo dijkstra.py
Implementa o algoritmo de Dijkstra para encontrar o menor caminho
"""

import heapq


class Dijkstra:
    """Classe que implementa o algoritmo de Dijkstra"""
    
    def __init__(self, grafo):
        """
        Inicializa o algoritmo com um grafo
        
        Args:
            grafo: objeto Grafo a ser processado
        """
        self.grafo = grafo
    
    def calcular_menor_caminho(self, origem_id, destino_id):
        """
        Calcula o menor caminho entre dois vértices usando Dijkstra
        
        Args:
            origem_id: id do vértice de origem
            destino_id: id do vértice de destino
            
        Returns:
            tupla (caminho, custo_total, detalhes) onde:
            - caminho: lista de ids dos vértices no caminho
            - custo_total: soma dos pesos do caminho
            - detalhes: lista de dicionários com informações de cada aresta
            Retorna (None, None, None) se não houver caminho
        """
        # Verifica se os vértices existem
        if origem_id not in self.grafo.vertices or destino_id not in self.grafo.vertices:
            return None, None, None
        
        # Inicialização
        distancias = {v_id: float('infinity') for v_id in self.grafo.vertices}
        distancias[origem_id] = 0
        predecessores = {v_id: None for v_id in self.grafo.vertices}
        visitados = set()
        
        # Fila de prioridade: (distancia, vertice_id)
        fila = [(0, origem_id)]
        
        while fila:
            # Extrai o vértice com menor distância
            distancia_atual, vertice_atual = heapq.heappop(fila)
            
            # Se já foi visitado, ignora
            if vertice_atual in visitados:
                continue
            
            # Marca como visitado
            visitados.add(vertice_atual)
            
            # Se chegou no destino, pode parar
            if vertice_atual == destino_id:
                break
            
            # Processa todos os vizinhos
            vizinhos = self.grafo.obter_vizinhos(vertice_atual)
            for vizinho in vizinhos:
                vizinho_id = vizinho['destino']
                peso = vizinho['peso']
                
                # Se já foi visitado, ignora
                if vizinho_id in visitados:
                    continue
                
                # Calcula nova distância
                nova_distancia = distancias[vertice_atual] + peso
                
                # Se encontrou caminho melhor, atualiza
                if nova_distancia < distancias[vizinho_id]:
                    distancias[vizinho_id] = nova_distancia
                    predecessores[vizinho_id] = vertice_atual
                    heapq.heappush(fila, (nova_distancia, vizinho_id))
        
        # Reconstrói o caminho
        if distancias[destino_id] == float('infinity'):
            # Não há caminho
            return None, None, None
        
        caminho = self._reconstruir_caminho(predecessores, origem_id, destino_id)
        custo_total = distancias[destino_id]
        detalhes = self._obter_detalhes_caminho(caminho)
        
        return caminho, custo_total, detalhes
    
    def _reconstruir_caminho(self, predecessores, origem_id, destino_id):
        """
        Reconstrói o caminho a partir dos predecessores
        
        Args:
            predecessores: dicionário de predecessores
            origem_id: id do vértice de origem
            destino_id: id do vértice de destino
            
        Returns:
            lista de ids dos vértices no caminho
        """
        caminho = []
        atual = destino_id
        
        while atual is not None:
            caminho.append(atual)
            atual = predecessores[atual]
        
        caminho.reverse()
        return caminho
    
    def _obter_detalhes_caminho(self, caminho):
        """
        Obtém detalhes de cada aresta no caminho
        
        Args:
            caminho: lista de ids dos vértices
            
        Returns:
            lista de dicionários com informações de cada aresta
        """
        detalhes = []
        
        for i in range(len(caminho) - 1):
            origem_id = caminho[i]
            destino_id = caminho[i + 1]
            
            peso = self.grafo.obter_peso(origem_id, destino_id)
            motivo = self.grafo.obter_motivo(origem_id, destino_id)
            
            origem = self.grafo.vertices[origem_id]
            destino = self.grafo.vertices[destino_id]
            
            detalhes.append({
                'origem': origem.nome,
                'destino': destino.nome,
                'peso': peso,
                'motivo': motivo
            })
        
        return detalhes
    
    @staticmethod
    def formatar_resultado(caminho, custo_total, detalhes, grafo):
        """
        Formata o resultado do caminho para exibição
        
        Args:
            caminho: lista de ids dos vértices
            custo_total: custo total do caminho
            detalhes: lista de detalhes das arestas
            grafo: objeto Grafo
            
        Returns:
            string formatada com o resultado
        """
        if caminho is None:
            return "Não há caminho disponível entre os pontos selecionados!"
        
        resultado = "\n" + "=" * 60 + "\n"
        resultado += "           MELHOR CAMINHO ENCONTRADO\n"
        resultado += "=" * 60 + "\n\n"
        
        # Caminho resumido
        nomes_caminho = [grafo.vertices[v_id].nome for v_id in caminho]
        resultado += f"Rota: {' → '.join(nomes_caminho)}\n\n"
        
        # Detalhes de cada trecho
        resultado += "Detalhes do percurso:\n"
        resultado += "-" * 60 + "\n"
        
        for i, detalhe in enumerate(detalhes, 1):
            resultado += f"\n{i}. {detalhe['origem']} → {detalhe['destino']}\n"
            resultado += f"   Peso: {detalhe['peso']}\n"
            resultado += f"   Condição: {detalhe['motivo']}\n"
        
        # Custo total
        resultado += "\n" + "-" * 60 + "\n"
        resultado += f"CUSTO TOTAL: {custo_total}\n"
        resultado += "=" * 60 + "\n"
        
        return resultado
