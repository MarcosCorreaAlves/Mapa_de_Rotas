"""
Módulo persistencia.py
Gerencia salvamento e carregamento de dados do grafo
"""

import json
import os
from grafo import Vertice, Grafo


class SistemaPersistencia:
    """Classe responsável pela persistência de dados"""
    
    def __init__(self, diretorio_dados='dados'):
        """
        Inicializa o sistema de persistência
        
        Args:
            diretorio_dados: diretório onde os dados serão salvos
        """
        self.diretorio_dados = diretorio_dados
        self.arquivo_grafo = os.path.join(diretorio_dados, 'grafo_cidade.json')
        self.arquivo_pesos = os.path.join(diretorio_dados, 'pesos_atuais.json')
        
        # Cria diretório se não existir
        os.makedirs(diretorio_dados, exist_ok=True)
    
    def salvar_grafo_estrutura(self, grafo):
        """
        Salva a estrutura do grafo (vértices e conexões) em arquivo JSON
        
        Args:
            grafo: objeto Grafo a ser salvo
        """
        dados = {
            'vertices': [],
            'arestas': []
        }
        
        # Salva vértices
        for vertice_id, vertice in grafo.vertices.items():
            dados['vertices'].append(vertice.to_dict())
        
        # Salva arestas (sem duplicatas)
        arestas_salvas = set()
        for origem_id, vizinhos in grafo.adjacencias.items():
            for vizinho in vizinhos:
                destino_id = vizinho['destino']
                # Evita duplicatas em grafos bidirecionais
                aresta_tuple = tuple(sorted([origem_id, destino_id]))
                if aresta_tuple not in arestas_salvas:
                    arestas_salvas.add(aresta_tuple)
                    dados['arestas'].append({
                        'origem': origem_id,
                        'destino': destino_id
                    })
        
        # Salva em arquivo
        with open(self.arquivo_grafo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
    
    def carregar_grafo_estrutura(self):
        """
        Carrega a estrutura do grafo de arquivo JSON
        
        Returns:
            objeto Grafo carregado ou None se arquivo não existir
        """
        if not os.path.exists(self.arquivo_grafo):
            return None
        
        with open(self.arquivo_grafo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        grafo = Grafo()
        
        # Carrega vértices
        for v_dados in dados['vertices']:
            vertice = Vertice.from_dict(v_dados)
            grafo.adicionar_vertice(vertice)
        
        # Carrega arestas (com pesos padrão)
        for a_dados in dados['arestas']:
            grafo.adicionar_aresta(
                a_dados['origem'],
                a_dados['destino'],
                peso=1,
                motivo="Condição normal",
                bidirecional=True
            )
        
        return grafo
    
    def salvar_pesos_atuais(self, grafo):
        """
        Salva os pesos e motivos atuais das arestas
        
        Args:
            grafo: objeto Grafo com os pesos atuais
        """
        dados = {
            'arestas': []
        }
        
        # Salva todas as arestas com seus pesos e motivos
        arestas_salvas = set()
        for origem_id, vizinhos in grafo.adjacencias.items():
            for vizinho in vizinhos:
                destino_id = vizinho['destino']
                # Evita duplicatas
                aresta_tuple = tuple(sorted([origem_id, destino_id]))
                if aresta_tuple not in arestas_salvas:
                    arestas_salvas.add(aresta_tuple)
                    dados['arestas'].append({
                        'origem': origem_id,
                        'destino': destino_id,
                        'peso': vizinho['peso'],
                        'motivo': vizinho['motivo']
                    })
        
        # Salva em arquivo
        with open(self.arquivo_pesos, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
    
    def carregar_pesos_atuais(self, grafo):
        """
        Carrega os pesos e motivos salvos e aplica ao grafo
        
        Args:
            grafo: objeto Grafo a ter seus pesos atualizados
            
        Returns:
            True se carregou com sucesso, False caso contrário
        """
        if not os.path.exists(self.arquivo_pesos):
            return False
        
        with open(self.arquivo_pesos, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        # Atualiza pesos das arestas
        for aresta in dados['arestas']:
            grafo.atualizar_peso(
                aresta['origem'],
                aresta['destino'],
                aresta['peso'],
                aresta['motivo'],
                bidirecional=True
            )
        
        return True
    
    def criar_grafo_padrao(self):
        """
        Cria um grafo padrão com a estrutura da cidade
        
        Returns:
            objeto Grafo com estrutura padrão
        """
        grafo = Grafo()
        
        # Cria 26 vértices (A-Z)
        import string
        letras = string.ascii_uppercase
        
        # Coordenadas para uma grade 5x6 (para visualização)
        # 6 colunas (1 a 6) e 5 linhas (1 a 5)
        # 26 vértices: A-Z
        
        vertices_dados = []
        nomes_padrao = [
            "Centro", "Shopping", "Hospital", "Escola", "Praça", "Estação",
            "Parque", "Mercado", "Biblioteca", "Aeroporto", "Rodoviária", "Prefeitura",
            "Museu", "Teatro", "Estádio", "Jardim Botânico", "Universidade", "Fórum",
            "Delegacia", "Correios", "Padaria", "Farmácia", "Banco", "Posto de Saúde",
            "Pizzaria", "Cinema"
        ]
        
        for i, letra in enumerate(letras):
            nome = nomes_padrao[i] if i < len(nomes_padrao) else f"Ponto {letra}"
            # Distribuição em grade 5x6 com espaçamento maior para visualização
            # Multiplica por 3 para espaçar e adiciona 1 para offset
            x = ((i % 6) + 1) * 3
            y = (5 - (i // 6)) * 3 # Inverte y para que A-F fiquem no topo
            
            vertice = Vertice(letra, nome, x, y)
            grafo.adicionar_vertice(vertice)
            vertices_dados.append(letra)

        # Cria arestas (conexões entre pontos)
        # Conexões em grade (horizontal e vertical)
        arestas = []
        
        # Conexões horizontais (linha por linha)
        for i in range(26):
            if (i + 1) % 6 != 0 and i < 25: # Não conecta o último de cada linha com o primeiro da próxima
                origem = letras[i]
                destino = letras[i+1]
                arestas.append((origem, destino))
        
        # Conexões verticais (coluna por coluna)
        for i in range(20): # 26 - 6 = 20 (até a letra T)
            origem = letras[i]
            destino = letras[i+6]
            arestas.append((origem, destino))
        
        # Conexões diagonais adicionais para mais opções de rota
        # Exemplo: A-H, B-G, C-I, etc.
        for i in range(20):
            if (i + 1) % 6 != 0 and i < 25:
                # Diagonal direita-baixo (A -> H)
                if i + 7 < 26:
                    origem = letras[i]
                    destino = letras[i+7]
                    arestas.append((origem, destino))
                # Diagonal esquerda-baixo (B -> G)
                if i + 5 < 26 and i % 6 != 0:
                    origem = letras[i]
                    destino = letras[i+5]
                    arestas.append((origem, destino))
        
        # Remove a criação de arestas anterior
        # A criação de arestas será feita a partir da lista 'arestas' gerada acima.
        
        # Cria arestas (conexões entre pontos)
        # Formato: (origem, destino)
        # arestas = [
        #     ('A', 'B'), ('B', 'C'),  # Linha superior
        #     ('A', 'D'), ('B', 'E'), ('C', 'F'),  # Verticais superiores
        #     ('D', 'E'), ('E', 'F'),  # Linha do meio
        #     ('D', 'G'), ('E', 'H'), ('F', 'I'),  # Verticais inferiores
        #     ('G', 'H'), ('H', 'I'),  # Linha inferior
        #     ('H', 'J'),  # Conexão ao aeroporto
        #     ('A', 'E'), ('E', 'I'),  # Diagonais para mais opções de rota
        # ]
        
        # A lista 'arestas' já foi criada acima com as novas conexões de A-Z.
        # Apenas o loop de criação de arestas é mantido.
        
        for origem, destino in arestas:
            grafo.adicionar_aresta(origem, destino, peso=1, motivo="Condição normal", bidirecional=True)
        
        return grafo
