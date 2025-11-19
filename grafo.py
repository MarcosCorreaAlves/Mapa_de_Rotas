"""
Módulo grafo.py
Contém as classes Vertice, Aresta e Grafo para representar o mapa de rotas
"""

class Vertice:
    """Representa um ponto no mapa (intersecção, local importante)"""
    
    def __init__(self, id, nome, x=0, y=0):
        """
        Inicializa um vértice
        
        Args:
            id: identificador único do vértice
            nome: nome do local
            x: coordenada x para visualização
            y: coordenada y para visualização
        """
        self.id = id
        self.nome = nome
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"{self.id} - {self.nome}"
    
    def __repr__(self):
        return f"Vertice({self.id}, {self.nome})"
    
    def __eq__(self, outro):
        return self.id == outro.id
    
    def __hash__(self):
        return hash(self.id)
    
    def to_dict(self):
        """Converte o vértice para dicionário (para persistência)"""
        return {
            'id': self.id,
            'nome': self.nome,
            'x': self.x,
            'y': self.y
        }
    
    @staticmethod
    def from_dict(dados):
        """Cria um vértice a partir de um dicionário"""
        return Vertice(dados['id'], dados['nome'], dados['x'], dados['y'])


class Aresta:
    """Representa uma rua/conexão entre dois vértices"""
    
    def __init__(self, origem, destino, peso=1, motivo="Condição normal"):
        """
        Inicializa uma aresta
        
        Args:
            origem: vértice de origem
            destino: vértice de destino
            peso: custo/dificuldade da rota
            motivo: justificativa do peso (condição da rua)
        """
        self.origem = origem
        self.destino = destino
        self.peso = peso
        self.motivo = motivo
    
    def __str__(self):
        return f"{self.origem.id} -> {self.destino.id} (peso: {self.peso}, {self.motivo})"
    
    def __repr__(self):
        return f"Aresta({self.origem.id}, {self.destino.id}, {self.peso})"
    
    def to_dict(self):
        """Converte a aresta para dicionário (para persistência)"""
        return {
            'origem': self.origem.id,
            'destino': self.destino.id,
            'peso': self.peso,
            'motivo': self.motivo
        }


class Grafo:
    """Estrutura principal do mapa de rotas"""
    
    def __init__(self):
        """Inicializa um grafo vazio"""
        self.vertices = {}  # dicionário: id -> Vertice
        self.adjacencias = {}  # dicionário: id -> lista de (vizinho_id, peso, motivo)
    
    def adicionar_vertice(self, vertice):
        """
        Adiciona um vértice ao grafo
        
        Args:
            vertice: objeto Vertice a ser adicionado
        """
        if vertice.id not in self.vertices:
            self.vertices[vertice.id] = vertice
            self.adjacencias[vertice.id] = []
    
    def adicionar_aresta(self, origem_id, destino_id, peso=1, motivo="Condição normal", bidirecional=True):
        """
        Adiciona uma aresta entre dois vértices
        
        Args:
            origem_id: id do vértice de origem
            destino_id: id do vértice de destino
            peso: custo da aresta
            motivo: justificativa do peso
            bidirecional: se True, cria aresta nos dois sentidos
        """
        if origem_id in self.vertices and destino_id in self.vertices:
            # Adiciona aresta de origem para destino
            self.adjacencias[origem_id].append({
                'destino': destino_id,
                'peso': peso,
                'motivo': motivo
            })
            
            # Se bidirecional, adiciona aresta de destino para origem
            if bidirecional:
                self.adjacencias[destino_id].append({
                    'destino': origem_id,
                    'peso': peso,
                    'motivo': motivo
                })
    
    def obter_vizinhos(self, vertice_id):
        """
        Retorna os vizinhos de um vértice
        
        Args:
            vertice_id: id do vértice
            
        Returns:
            lista de dicionários com informações dos vizinhos
        """
        return self.adjacencias.get(vertice_id, [])
    
    def obter_peso(self, origem_id, destino_id):
        """
        Retorna o peso da aresta entre dois vértices
        
        Args:
            origem_id: id do vértice de origem
            destino_id: id do vértice de destino
            
        Returns:
            peso da aresta ou None se não existir
        """
        vizinhos = self.obter_vizinhos(origem_id)
        for vizinho in vizinhos:
            if vizinho['destino'] == destino_id:
                return vizinho['peso']
        return None
    
    def obter_motivo(self, origem_id, destino_id):
        """
        Retorna o motivo do peso da aresta entre dois vértices
        
        Args:
            origem_id: id do vértice de origem
            destino_id: id do vértice de destino
            
        Returns:
            motivo da aresta ou None se não existir
        """
        vizinhos = self.obter_vizinhos(origem_id)
        for vizinho in vizinhos:
            if vizinho['destino'] == destino_id:
                return vizinho['motivo']
        return None
    
    def atualizar_peso(self, origem_id, destino_id, novo_peso, novo_motivo, bidirecional=True):
        """
        Atualiza o peso e motivo de uma aresta
        
        Args:
            origem_id: id do vértice de origem
            destino_id: id do vértice de destino
            novo_peso: novo peso da aresta
            novo_motivo: novo motivo do peso
            bidirecional: se True, atualiza nos dois sentidos
        """
        # Atualiza de origem para destino
        vizinhos = self.adjacencias.get(origem_id, [])
        for vizinho in vizinhos:
            if vizinho['destino'] == destino_id:
                vizinho['peso'] = novo_peso
                vizinho['motivo'] = novo_motivo
                break
        
        # Se bidirecional, atualiza de destino para origem
        if bidirecional:
            vizinhos = self.adjacencias.get(destino_id, [])
            for vizinho in vizinhos:
                if vizinho['destino'] == origem_id:
                    vizinho['peso'] = novo_peso
                    vizinho['motivo'] = novo_motivo
                    break
    
    def obter_todas_arestas(self):
        """
        Retorna todas as arestas do grafo (sem duplicatas para arestas bidirecionais)
        
        Returns:
            lista de tuplas (origem_id, destino_id, peso, motivo)
        """
        arestas_vistas = set()
        arestas = []
        
        for origem_id, vizinhos in self.adjacencias.items():
            for vizinho in vizinhos:
                destino_id = vizinho['destino']
                # Para evitar duplicatas em grafos bidirecionais
                aresta_tuple = tuple(sorted([origem_id, destino_id]))
                if aresta_tuple not in arestas_vistas:
                    arestas_vistas.add(aresta_tuple)
                    arestas.append({
                        'origem': origem_id,
                        'destino': destino_id,
                        'peso': vizinho['peso'],
                        'motivo': vizinho['motivo']
                    })
        
        return arestas
    
    def __str__(self):
        resultado = "Grafo:\n"
        resultado += f"Vértices: {len(self.vertices)}\n"
        for vertice_id, vertice in self.vertices.items():
            resultado += f"  {vertice}\n"
        resultado += f"\nArestas:\n"
        for aresta in self.obter_todas_arestas():
            resultado += f"  {aresta['origem']} -> {aresta['destino']} (peso: {aresta['peso']}, {aresta['motivo']})\n"
        return resultado
