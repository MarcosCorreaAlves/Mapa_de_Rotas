# Guia Rápido de Uso

## Instalação

```bash
# 1. Instalar dependências
pip3 install matplotlib

# 2. Navegar até o diretório
cd mapa_rotas_cidades
```

## Executar o Sistema

```bash
python3.11 main.py
```

## Uso Básico

### 1️⃣ Calcular uma Rota

1. No menu, escolha opção **1**
2. Digite o ID da origem (ex: **A** para Centro)
3. Digite o ID do destino (ex: **J** para Aeroporto)
4. Veja o resultado com o melhor caminho e custo total
5. Digite **s** para visualizar o caminho no mapa

### 2️⃣ Ver o Mapa Completo

1. No menu, escolha opção **2**
2. Uma janela com o mapa será aberta
3. Feche a janela para voltar ao menu

### 3️⃣ Reiniciar (Gerar Novos Pesos)

1. No menu, escolha opção **3**
2. O sistema gerará novos pesos aleatórios
3. As condições das ruas mudarão
4. Calcule rotas novamente para ver as diferenças

### 4️⃣ Ver Detalhes das Rotas

1. No menu, escolha opção **4**
2. Veja uma tabela com todas as rotas
3. Cada rota mostra: origem, destino, peso e condição

## Pontos Disponíveis

| ID | Local       |
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

## Condições das Ruas

- 🟢 **Via expressa** (peso 1-2): rota rápida
- 🟢 **Trânsito livre** (peso 2-4): fluxo normal
- 🟡 **Trânsito moderado** (peso 4-7): algum congestionamento
- 🟠 **Trânsito intenso** (peso 7-10): muito congestionamento
- 🔴 **Rua em obras** (peso 10-15): desvios necessários
- 🔴 **Acidente na via** (peso 12-18): bloqueio parcial
- ⛔ **Rua fechada** (peso 999): rota bloqueada

## Dicas

💡 **Experimente reiniciar o sistema** (opção 3) e calcular a mesma rota novamente. Você verá que o caminho pode mudar devido às novas condições das ruas!

💡 **Use a visualização gráfica** (opção 2) para entender melhor a estrutura da cidade e as conexões entre os pontos.

💡 **Veja os detalhes das rotas** (opção 4) antes de calcular um caminho para saber quais ruas estão com problemas.

## Exemplo Completo

```
1. Execute: python3.11 main.py
2. Escolha opção: 1
3. Digite origem: A
4. Digite destino: J
5. Veja o resultado: Centro → Praça → Mercado → Aeroporto (custo: 9)
6. Digite: s (para ver no mapa)
7. Feche o mapa
8. Escolha opção: 3 (reiniciar)
9. Escolha opção: 1 novamente
10. Digite origem: A
11. Digite destino: J
12. Veja o novo resultado: pode ser diferente!
```

## Sair do Sistema

- No menu, escolha opção **8**
- Ou pressione **Ctrl+C** a qualquer momento

---

**Divirta-se explorando as rotas da cidade! 🚗🗺️**
