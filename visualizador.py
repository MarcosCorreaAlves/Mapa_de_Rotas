"""
Módulo visualizador.py
Responsável pela visualização gráfica do mapa de rotas
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D


class VisualizadorMapa:
    """Classe responsável pela visualização do mapa"""
    
    def __init__(self, grafo):
        """
        Inicializa o visualizador com um grafo
        
        Args:
            grafo: objeto Grafo a ser visualizado
        """
        self.grafo = grafo
        self.cores_peso = {
            'Via expressa': '#00FF00',      # Verde claro
            'Trânsito livre': '#90EE90',    # Verde
            'Trânsito moderado': '#FFD700', # Amarelo
            'Trânsito intenso': '#FFA500',  # Laranja
            'Rua em obras': '#FF6347',      # Vermelho claro
            'Acidente na via': '#FF0000',   # Vermelho
            'Rua fechada': '#8B0000'        # Vermelho escuro
        }
    
    def desenhar_mapa(self, caminho_destacado=None, salvar_arquivo=None):
        """
        Desenha o mapa completo do grafo
        
        Args:
            caminho_destacado: lista de ids de vértices do caminho a destacar
            salvar_arquivo: nome do arquivo para salvar a imagem (opcional)
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Desenha as arestas
        self._desenhar_arestas(ax, caminho_destacado)
        
        # Desenha os vértices
        self._desenhar_vertices(ax, caminho_destacado)
        
        # Configurações do gráfico
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        # ax.grid(True, alpha=0.3) # Removendo a grade para um visual mais limpo
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_title('Mapa de Rotas da Cidade', fontsize=16, fontweight='bold')
        
        # Adiciona legenda
        self._adicionar_legenda(ax)
        
        # Ajusta limites para garantir que todos os elementos caibam
        ax.set_xlim(min(v.x for v in self.grafo.vertices.values()) - 0.5, 
                    max(v.x for v in self.grafo.vertices.values()) + 1.5)
        ax.set_ylim(min(v.y for v in self.grafo.vertices.values()) - 0.5, 
                    max(v.y for v in self.grafo.vertices.values()) + 0.5)
        
        plt.tight_layout()
        
        if salvar_arquivo:
            plt.savefig(salvar_arquivo, dpi=300, bbox_inches='tight')
            print(f"\nMapa salvo em: {salvar_arquivo}")
        
        plt.show()
    
    def _desenhar_arestas(self, ax, caminho_destacado):
        """Desenha as arestas do grafo"""
        arestas = self.grafo.obter_todas_arestas()
        
        for aresta in arestas:
            origem = self.grafo.vertices[aresta['origem']]
            destino = self.grafo.vertices[aresta['destino']]
            
            # Verifica se a aresta faz parte do caminho destacado
            eh_caminho = False
            if caminho_destacado:
                for i in range(len(caminho_destacado) - 1):
                    if ((caminho_destacado[i] == aresta['origem'] and 
                         caminho_destacado[i+1] == aresta['destino']) or
                        (caminho_destacado[i] == aresta['destino'] and 
                         caminho_destacado[i+1] == aresta['origem'])):
                        eh_caminho = True
                        break
            
            # Define cor baseada no motivo
            cor = self.cores_peso.get(aresta['motivo'], '#808080')
            
            # Define estilo da linha
            if eh_caminho:
                linewidth = 4
                alpha = 1.0
                zorder = 10
            else:
                linewidth = 2
                alpha = 0.6
                zorder = 1
            
            # Desenha a linha
            ax.plot([origem.x, destino.x], [origem.y, destino.y],
                   color=cor, linewidth=linewidth, alpha=alpha, zorder=zorder)
            
            # Adiciona rótulo do peso no meio da aresta
            meio_x = (origem.x + destino.x) / 2
            meio_y = (origem.y + destino.y) / 2
            
            # Calcula o ângulo da linha para offset
            dx = destino.x - origem.x
            dy = destino.y - origem.y
            
            # Ajusta a posição do texto para ficar ligeiramente deslocado da linha
            offset_x = 0.05 * dy / (abs(dx) + abs(dy) + 1e-6)
            offset_y = 0.05 * dx / (abs(dx) + abs(dy) + 1e-6)
            
            ax.text(meio_x + offset_x, meio_y - offset_y, str(aresta['peso']),
                   fontsize=10, ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                           edgecolor='black', alpha=0.9, linewidth=0.5),
                   zorder=15) # Aumentando zorder para garantir que fique por cima
    
    def _desenhar_vertices(self, ax, caminho_destacado):
        """Desenha os vértices do grafo"""
        for vertice_id, vertice in self.grafo.vertices.items():
            # Verifica se o vértice faz parte do caminho destacado
            eh_caminho = caminho_destacado and vertice_id in caminho_destacado
            
            # Define cor e tamanho
            if eh_caminho:
                if vertice_id == caminho_destacado[0]:
                    cor = '#008000'  # Verde escuro para origem
                    tamanho = 800
                    label = 'ORIGEM'
                elif vertice_id == caminho_destacado[-1]:
                    cor = '#CC0000'  # Vermelho escuro para destino
                    tamanho = 800
                    label = 'DESTINO'
                else:
                    cor = '#FFD700'  # Amarelo para caminho
                    tamanho = 600
                    label = ''
            else:
                cor = '#1E90FF'  # Azul mais escuro para outros
                tamanho = 500
                label = ''
            
            # Desenha o vértice
            ax.scatter(vertice.x, vertice.y, s=tamanho, c=cor, 
                      edgecolors='black', linewidths=1.5, zorder=20, alpha=0.9)
            
            # Adiciona rótulo do vértice
            ax.text(vertice.x, vertice.y, f"{vertice.id}",
                   fontsize=12, ha='center', va='center',
                   fontweight='bold', color='white', zorder=21)
            
            # Adiciona nome do local abaixo do ID
            ax.text(vertice.x, vertice.y - 0.15, vertice.nome,
                   fontsize=9, ha='center', va='top',
                   fontweight='normal', color='black', zorder=21)
            
            # Adiciona label especial para origem/destino
            if label:
                ax.text(vertice.x, vertice.y + 0.25, label,
                       fontsize=9, ha='center', va='bottom',
                       fontweight='bold', color='white',
                       bbox=dict(boxstyle='round,pad=0.3', 
                               facecolor=cor, alpha=0.9),
                       zorder=22)
    
    def _adicionar_legenda(self, ax):
        """Adiciona legenda ao gráfico"""
        # Cria elementos da legenda
        elementos = []
        
        # Legenda de condições
        for motivo, cor in self.cores_peso.items():
            elementos.append(Line2D([0], [0], color=cor, linewidth=4, label=motivo))
        
        # Adiciona legenda
        ax.legend(handles=elementos, loc='upper left', 
                 bbox_to_anchor=(1.02, 1), fontsize=10,
                 title='Condições das Ruas (Peso)', title_fontsize=12,
                 frameon=True, fancybox=True, shadow=True)
    
    def exibir_tabela_arestas(self):
        """Exibe uma tabela com todas as arestas e suas informações"""
        print("\n" + "=" * 80)
        print("                    INFORMAÇÕES DAS ROTAS")
        print("=" * 80)
        print(f"{'Origem':<15} {'Destino':<15} {'Peso':<8} {'Condição':<30}")
        print("-" * 80)
        
        arestas = self.grafo.obter_todas_arestas()
        arestas_ordenadas = sorted(arestas, key=lambda x: (x['origem'], x['destino']))
        
        for aresta in arestas_ordenadas:
            origem_nome = self.grafo.vertices[aresta['origem']].nome
            destino_nome = self.grafo.vertices[aresta['destino']].nome
            print(f"{origem_nome:<15} {destino_nome:<15} {aresta['peso']:<8} {aresta['motivo']:<30}")
        
        print("=" * 80)
        