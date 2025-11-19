"""
Módulo interface.py
Implementa a interface de usuário com menu interativo
"""

import os


class InterfaceUsuario:
    """Classe responsável pela interface de usuário"""
    
    def __init__(self, grafo, dijkstra, visualizador, gerador_pesos, persistencia):
        """
        Inicializa a interface
        
        Args:
            grafo: objeto Grafo
            dijkstra: objeto Dijkstra
            visualizador: objeto VisualizadorMapa
            gerador_pesos: classe GeradorPesos
            persistencia: objeto SistemaPersistencia
        """
        self.grafo = grafo
        self.dijkstra = dijkstra
        self.visualizador = visualizador
        self.gerador_pesos = gerador_pesos
        self.persistencia = persistencia
    
    def limpar_tela(self):
        """Limpa a tela do terminal"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def exibir_cabecalho(self):
        """Exibe o cabeçalho do sistema"""
        print("\n" + "=" * 70)
        print("          SISTEMA DE MAPA DE ROTAS DE CIDADES")
        print("            Algoritmo de Dijkstra - Menor Caminho")
        print("=" * 70 + "\n")
    
    def exibir_menu_principal(self):
        """Exibe o menu principal"""
        print("\n" + "-" * 70)
        print("                        MENU PRINCIPAL")
        print("-" * 70)
        print("1. Calcular melhor rota entre dois pontos")
        print("2. Visualizar mapa da cidade")
        print("3. Reiniciar sistema (gerar novos pesos)")
        print("4. Ver detalhes de todas as rotas")
        print("5. Ver pontos disponíveis")
        print("6. Ver condições possíveis das ruas")
        print("7. Salvar estado atual")
        print("8. Sair")
        print("-" * 70)
    
    def obter_opcao(self):
        """
        Obtém a opção escolhida pelo usuário
        
        Returns:
            opção escolhida (string)
        """
        return input("\nEscolha uma opção: ").strip()
    
    def listar_vertices(self):
        """Lista todos os vértices disponíveis"""
        print("\n" + "=" * 70)
        print("                    PONTOS DISPONÍVEIS")
        print("=" * 70)
        print(f"{'ID':<5} {'Nome':<20}")
        print("-" * 70)
        
        vertices_ordenados = sorted(self.grafo.vertices.items())
        for v_id, vertice in vertices_ordenados:
            print(f"{v_id:<5} {vertice.nome:<20}")
        
        print("=" * 70)
    
    def solicitar_origem_destino(self):
        """
        Solicita origem e destino ao usuário
        
        Returns:
            tupla (origem_id, destino_id) ou (None, None) se inválido
        """
        print("\n")
        self.listar_vertices()
        
        origem_id = input("\nDigite o ID do ponto de ORIGEM: ").strip().upper()
        if origem_id not in self.grafo.vertices:
            print(f"\n❌ Erro: Ponto '{origem_id}' não existe!")
            return None, None
        
        destino_id = input("Digite o ID do ponto de DESTINO: ").strip().upper()
        if destino_id not in self.grafo.vertices:
            print(f"\n❌ Erro: Ponto '{destino_id}' não existe!")
            return None, None
        
        if origem_id == destino_id:
            print("\n❌ Erro: Origem e destino devem ser diferentes!")
            return None, None
        
        return origem_id, destino_id
    
    def calcular_e_exibir_rota(self):
        """Calcula e exibe a melhor rota"""
        origem_id, destino_id = self.solicitar_origem_destino()
        
        if origem_id is None:
            input("\nPressione Enter para continuar...")
            return
        
        print("\n🔍 Calculando melhor rota...")
        
        # Calcula o menor caminho
        caminho, custo_total, detalhes = self.dijkstra.calcular_menor_caminho(origem_id, destino_id)
        
        # Exibe resultado
        resultado = self.dijkstra.formatar_resultado(caminho, custo_total, detalhes, self.grafo)
        print(resultado)
        
        # Pergunta se quer visualizar no mapa
        if caminho:
            resposta = input("\nDeseja visualizar o caminho no mapa? (s/n): ").strip().lower()
            if resposta == 's':
                print("\n📊 Gerando visualização do mapa...")
                self.visualizador.desenhar_mapa(caminho_destacado=caminho)
        
        input("\nPressione Enter para continuar...")
    
    def visualizar_mapa(self):
        """Visualiza o mapa completo"""
        print("\n📊 Gerando visualização do mapa...")
        self.visualizador.desenhar_mapa()
        input("\nPressione Enter para continuar...")
    
    def reiniciar_pesos(self):
        """Reinicia o sistema gerando novos pesos"""
        print("\n🔄 Reiniciando sistema...")
        print("Gerando novos pesos aleatórios para todas as rotas...")
        
        self.gerador_pesos.gerar_pesos_para_grafo(self.grafo)
        
        print("✅ Pesos atualizados com sucesso!")
        print("\nAs condições das ruas foram alteradas.")
        
        # Salva automaticamente
        self.persistencia.salvar_pesos_atuais(self.grafo)
        print("💾 Estado salvo automaticamente.")
        
        input("\nPressione Enter para continuar...")
    
    def ver_detalhes_rotas(self):
        """Exibe detalhes de todas as rotas"""
        self.visualizador.exibir_tabela_arestas()
        input("\nPressione Enter para continuar...")
    
    def ver_condicoes_possiveis(self):
        """Exibe as condições possíveis das ruas"""
        self.gerador_pesos.exibir_estatisticas_condicoes()
        input("\nPressione Enter para continuar...")
    
    def salvar_estado(self):
        """Salva o estado atual do sistema"""
        print("\n💾 Salvando estado atual...")
        self.persistencia.salvar_grafo_estrutura(self.grafo)
        self.persistencia.salvar_pesos_atuais(self.grafo)
        print("✅ Estado salvo com sucesso!")
        input("\nPressione Enter para continuar...")
    
    def executar(self):
        """Executa o loop principal da interface"""
        while True:
            self.limpar_tela()
            self.exibir_cabecalho()
            self.exibir_menu_principal()
            
            opcao = self.obter_opcao()
            
            if opcao == '1':
                self.calcular_e_exibir_rota()
            elif opcao == '2':
                self.visualizar_mapa()
            elif opcao == '3':
                self.reiniciar_pesos()
            elif opcao == '4':
                self.ver_detalhes_rotas()
            elif opcao == '5':
                self.listar_vertices()
                input("\nPressione Enter para continuar...")
            elif opcao == '6':
                self.ver_condicoes_possiveis()
            elif opcao == '7':
                self.salvar_estado()
            elif opcao == '8':
                print("\n👋 Encerrando sistema...")
                print("Obrigado por usar o Sistema de Mapa de Rotas!")
                break
            else:
                print("\n❌ Opção inválida! Tente novamente.")
                input("\nPressione Enter para continuar...")
