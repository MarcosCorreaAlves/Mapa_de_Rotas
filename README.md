# Sistema de Mapa de Rotas de Cidades

**Trabalho Prático - Estruturas de Dados Avançadas (Árvores e Grafos)**  
**Tema 7: Mapa de Rotas de Cidades**  
**Disciplina:** ITI275 - Algoritmos e Estruturas de Dados II  
**Instituição:** UFAM - ICET

---

## Descrição do Projeto

Este sistema implementa um mapa de rotas de cidades utilizando **grafos ponderados** e o **algoritmo de Dijkstra** para encontrar o menor caminho entre dois pontos. O diferencial do sistema é a capacidade de gerar **pesos dinâmicos** que representam condições reais das ruas (trânsito, obras, acidentes, etc.), com a possibilidade de reinicializar o sistema para simular mudanças nas condições das vias.

---

## Características Principais

### ✅ Funcionalidades Implementadas

1. **Estrutura de Grafo Ponderado**
   - Vértices representam pontos importantes da cidade
   - Arestas representam ruas/conexões entre pontos
   - Pesos representam dificuldade/tempo/custo de cada rota

2. **Algoritmo de Dijkstra**
   - Implementação própria (sem bibliotecas externas de grafos)
   - Calcula o menor caminho entre dois pontos
   - Retorna caminho completo com custo total

3. **Sistema de Pesos Dinâmicos**
   - Pesos gerados aleatoriamente
   - Cada peso tem uma justificativa (motivo)
   - 7 condições possíveis das ruas:
     - Via expressa (peso 1-2)
     - Trânsito livre (peso 2-4)
     - Trânsito moderado (peso 4-7)
     - Trânsito intenso (peso 7-10)
     - Rua em obras (peso 10-15)
     - Acidente na via (peso 12-18)
     - Rua fechada (peso 999)

4. **Reinicialização do Sistema**
   - Gera novos pesos aleatórios
   - Mantém a estrutura do grafo
   - Simula mudanças nas condições das ruas

5. **Visualização Gráfica**
   - Mapa visual do grafo usando matplotlib
   - Destaque do caminho encontrado
   - Cores diferentes para cada condição de rua
   - Legenda explicativa

6. **Persistência de Dados**
   - Salva estrutura do grafo em JSON
   - Salva pesos atuais em JSON
   - Carrega dados salvos ao iniciar

7. **Interface Interativa**
   - Menu no terminal
   - Navegação intuitiva
   - Feedback visual claro

---

## Estrutura do Projeto

```
mapa_rotas_cidades/
│
├── main.py              # Ponto de entrada do programa
├── grafo.py             # Classes Vertice, Aresta e Grafo
├── dijkstra.py          # Implementação do algoritmo de Dijkstra
├── gerador_pesos.py     # Geração de pesos aleatórios com motivos
├── visualizador.py      # Visualização gráfica do mapa
├── persistencia.py      # Sistema de salvamento/carregamento
├── interface.py         # Interface de usuário (menu interativo)
├── teste_sistema.py     # Script de testes automatizados
├── README.md            # Este arquivo
│
└── dados/               # Diretório de dados persistentes
    ├── grafo_cidade.json    # Estrutura do grafo
    └── pesos_atuais.json    # Pesos e motivos atuais
```

---

## Mapa da Cidade

O sistema utiliza um mapa com **10 pontos** conectados por **16 rotas**:

```
A (Centro) ─── B (Shopping) ─── C (Hospital)
│              │                │
D (Escola) ─── E (Praça) ────── F (Estação)
│              │                │
G (Parque) ─── H (Mercado) ──── I (Biblioteca)
               │
               J (Aeroporto)
```

### Pontos Disponíveis

| ID | Nome        |
|----|-------------|
| A  | Centro      |
| B  | Shopping    |
| C  | Hospital    |
| D  | Escola      |
| E  | Praça       |
| F  | Estação     |
| G  | Parque      |
| H  | Mercado     |
| I  | Biblioteca  |
| J  | Aeroporto   |

---

## Como Usar

### Requisitos

- Python 3.11 ou superior
- Bibliotecas: matplotlib (para visualização)

### Instalação

```bash
# Instalar matplotlib (se necessário)
pip3 install matplotlib
```

### Executar o Sistema

```bash
cd mapa_rotas_cidades
python3.11 main.py
```

### Executar Testes

```bash
python3.11 teste_sistema.py
```

---

## Menu Principal

Ao executar o sistema, você verá o seguinte menu:

```
1. Calcular melhor rota entre dois pontos
2. Visualizar mapa da cidade
3. Reiniciar sistema (gerar novos pesos)
4. Ver detalhes de todas as rotas
5. Ver pontos disponíveis
6. Ver condições possíveis das ruas
7. Salvar estado atual
8. Sair
```

### Opção 1: Calcular Melhor Rota

- Solicita ponto de origem e destino
- Calcula o menor caminho usando Dijkstra
- Exibe o caminho completo com detalhes
- Mostra o custo total
- Oferece visualização gráfica do caminho

**Exemplo de saída:**

```
============================================================
           MELHOR CAMINHO ENCONTRADO
============================================================

Rota: Centro → Praça → Mercado → Aeroporto

Detalhes do percurso:
------------------------------------------------------------

1. Centro → Praça
   Peso: 2
   Condição: Trânsito livre

2. Praça → Mercado
   Peso: 3
   Condição: Trânsito livre

3. Mercado → Aeroporto
   Peso: 4
   Condição: Trânsito moderado

------------------------------------------------------------
CUSTO TOTAL: 9
============================================================
```

### Opção 2: Visualizar Mapa

- Gera visualização gráfica do mapa completo
- Mostra todos os pontos e rotas
- Cores indicam condições das ruas
- Pesos exibidos em cada rota

### Opção 3: Reiniciar Sistema

- Gera novos pesos aleatórios para todas as rotas
- Mantém a estrutura do grafo
- Simula mudanças nas condições de trânsito
- Salva automaticamente o novo estado

### Opção 4: Ver Detalhes das Rotas

- Exibe tabela com todas as rotas
- Mostra origem, destino, peso e condição
- Útil para análise das condições atuais

### Opção 5: Ver Pontos Disponíveis

- Lista todos os pontos do mapa
- Mostra ID e nome de cada ponto

### Opção 6: Ver Condições Possíveis

- Exibe todas as condições possíveis das ruas
- Mostra faixa de peso de cada condição
- Indica probabilidade de ocorrência

### Opção 7: Salvar Estado Atual

- Salva a estrutura do grafo
- Salva os pesos e motivos atuais
- Permite continuar de onde parou

### Opção 8: Sair

- Encerra o sistema

---

## Detalhes Técnicos

### Algoritmo de Dijkstra

A implementação do algoritmo de Dijkstra utiliza:

- **Fila de prioridade** (heap) para eficiência
- **Complexidade:** O((V + E) log V) onde V = vértices e E = arestas
- **Estruturas auxiliares:**
  - Dicionário de distâncias
  - Dicionário de predecessores
  - Conjunto de vértices visitados

### Geração de Pesos

Os pesos são gerados usando:

- **Distribuição probabilística** para cada condição
- **Intervalos específicos** para cada tipo de condição
- **Aleatoriedade controlada** para simular realismo

### Persistência

Os dados são salvos em formato JSON:

- **grafo_cidade.json:** estrutura fixa do grafo (vértices e conexões)
- **pesos_atuais.json:** pesos e motivos dinâmicos

---

## Exemplos de Uso

### Exemplo 1: Calcular Rota Simples

```
Escolha uma opção: 1

Digite o ID do ponto de ORIGEM: A
Digite o ID do ponto de DESTINO: J

🔍 Calculando melhor rota...

Rota: Centro → Praça → Mercado → Aeroporto
CUSTO TOTAL: 9
```

### Exemplo 2: Reiniciar e Recalcular

```
Escolha uma opção: 3
🔄 Reiniciando sistema...
✅ Pesos atualizados com sucesso!

Escolha uma opção: 1
Digite o ID do ponto de ORIGEM: A
Digite o ID do ponto de DESTINO: J

Rota: Centro → Shopping → Praça → Mercado → Aeroporto
CUSTO TOTAL: 12
```

Note que após reiniciar, o caminho pode mudar devido aos novos pesos!

---

## Testes Implementados

O arquivo `teste_sistema.py` inclui:

1. **Teste de Criação de Grafo:** verifica criação de vértices e arestas
2. **Teste de Dijkstra:** valida cálculo de menor caminho
3. **Teste de Gerador de Pesos:** verifica geração aleatória
4. **Teste de Persistência:** valida salvamento e carregamento
5. **Teste de Caminho Completo:** testa múltiplos caminhos no grafo padrão

---

## Requisitos Atendidos

### ✅ Requisitos Técnicos do Trabalho

- [x] Implementar operações fundamentais sem bibliotecas prontas de grafos
- [x] Garantir persistência dos dados (arquivo JSON)
- [x] Menu interativo no terminal
- [x] Implementar algoritmo de caminho mínimo (Dijkstra)
- [x] Documentação clara do código
- [x] Estrutura organizada em módulos

### ✅ Funcionalidades Extras

- [x] Visualização gráfica do mapa
- [x] Sistema de pesos dinâmicos com motivos
- [x] Reinicialização com novos pesos
- [x] Testes automatizados
- [x] Interface amigável com feedback visual

---

## Possíveis Melhorias Futuras

1. **Interface Gráfica (GUI):** substituir menu de terminal por interface gráfica
2. **Mais Pontos:** expandir o mapa com mais locais
3. **Histórico de Rotas:** salvar rotas calculadas anteriormente
4. **Estatísticas:** análise de rotas mais usadas, tempos médios, etc.
5. **Exportação de Relatórios:** gerar relatórios em PDF
6. **Animação:** animar o processo de busca do Dijkstra
7. **Múltiplos Mapas:** permitir carregar diferentes mapas de cidades

---

## Conclusão

Este sistema demonstra a aplicação prática de **estruturas de dados avançadas** (grafos) e **algoritmos de busca** (Dijkstra) em um problema real de otimização de rotas. A implementação é completa, funcional e extensível, atendendo todos os requisitos do trabalho prático.

O sistema simula de forma realista as condições variáveis das ruas de uma cidade, permitindo explorar como diferentes condições de trânsito afetam a escolha da melhor rota.

---

## Autor

Sistema desenvolvido como trabalho prático da disciplina ITI275 - Algoritmos e Estruturas de Dados II.

**Data:** Novembro de 2025
