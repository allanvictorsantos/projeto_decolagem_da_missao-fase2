# MGPEB - Módulo de Gerenciamento de Pouso e Estabilização de Base
## Missão Aurora Siger - Colônia Marciana

**Fase:** Integração 2 - Design e Protótipo  
**Documentação Técnica e Governança**

---

## Índice

1. [Visão Geral](#visão-geral)
2. [Modelagem do Cenário de Pouso](#1-modelagem-do-cenário-de-pouso)
3. [Regras de Decisão e Portas Lógicas](#2-regras-de-decisão-e-portas-lógicas)
4. [Protótipo Python do MGPEB](#3-protótipo-python-do-mgpeb)
5. [Modelagem Matemática Aplicada](#4-modelagem-matemática-aplicada)
6. [Contexto Histórico e Evolução da Computação](#5-contexto-histórico-e-evolução-da-computação)
7. [Princípios ESG na Base Aurora](#6-princípios-esg-na-base-aurora)
8. [Conclusão](#7-conclusão)
9. [Instruções de Execução](#instruções-de-execução)

---

## Visão Geral

O **MGPEB** é um sistema de computação embarcada responsável por:

- **Receber e gerenciar** uma fila de módulos aguardando pouso na superfície marciana
- **Avaliar condições críticas** (combustível, clima, disponibilidade de pista, integridade de sensores)
- **Autorizar ou adiar** pousos com base em regras de segurança modeladas por portas lógicas
- **Organizar módulos** em estruturas de dados lineares (filas, listas, pilhas)
- **Executar algoritmos** de busca e ordenação para priorização dinâmica
- **Registrar histórico** de decisões para auditoria e rastreabilidade

A missão **Aurora Siger** é uma colônia nascente em Marte que requer governance rigorosa, eficiência energética e sustentabilidade ambiental mesmo em ambiente extraplanetário.

---

## 1. Modelagem do Cenário de Pouso

### 1.1 Módulos da Colônia Aurora Siger

A base será constituída por 5 módulos especializados, cada um com atributos críticos para a operação:

| Módulo | Função Principal | Prioridade | Combustível (L) | Massa (kg) | Criticidade | ETA (h) |
|--------|------------------|-----------|-----------------|-----------|-------------|---------|
| **Habitação** | Acomodações, ciclo de vida | 5 | 80 | 2000 | Alta (9) | 10:00 |
| **Energia** | Geração solar + baterias | 9 | 60 | 3000 | Crítica (10) | 09:00 |
| **Laboratório Científico** | Pesquisa, análise marciana | 7 | 50 | 2500 | Alta (8) | 11:00 |
| **Logística e Suporte** | Armazenamento, ferramentas | 6 | 75 | 2200 | Média (7) | 12:00 |
| **Suporte Médico** | Saúde, quarentena | 10 | 40 | 1800 | Crítica (10) | 08:00 |

### 1.2 Atributos de Cada Módulo

Cada módulo é representado como uma estrutura de dados com os seguintes campos:

```
Módulo = {
  "nome": string,              # Identificação única
  "prioridade": int (1-10),    # Prioridade de pouso (10 = máxima)
  "combustível": int (L),      # Combustível disponível para manobras
  "massa": int (kg),           # Massa total do módulo
  "criticidade": int (1-10),   # Importância para sobrevivência (10 = crítica)
  "horario": int (h),          # ETA em órbita lunar (hora UTC+Mars)
  "status": string             # {fila, pousado, espera, alerta}
}
```

### 1.3 Estruturas de Dados Lineares

O sistema utiliza estruturas lineares para gerenciar o fluxo operacional:

- **Fila Principal (\`fila_pouso\`)**: Módulos aguardando autorização de pouso em ordem FIFO
  - Função: Garantir equidade de espera + respeitar sequência de chegada
  
- **Lista de Pousados (\`modulos_pousados\`)**: Registro de módulos que completaram pouso com sucesso
  - Função: Rastreabilidade operacional
  
- **Lista de Espera (\`modulos_espera\`)**: Módulos cujo pouso foi adiado (combustível crítico, pista ocupada, etc.)
  - Função: Fila de retry com possibilidade de reordenação por prioridade
  
- **Lista de Alerta (\`modulos_alerta\`)**: Módulos em situação crítica (combustível < 30%)
  - Função: Visualização rápida de anomalias para intervenção humana
  
- **Pilha de Histórico (\`historico\`)**: LIFO com registro das decisões tomadas
  - Função: Auditoria, troubleshooting, análise pós-missão

---

## 2. Regras de Decisão e Portas Lógicas

### 2.1 Variáveis Booleanas de Entrada

A autorização de pouso depende de 4 variáveis críticas:

| Variável | Fonte | Descrição |
|----------|-------|-----------|
| **\`combustivel_ok\`** | Sensor telemetria | Combustível > 30 L (margem de segurança) |
| **\`clima_ok\`** | Estação meteorológica | Velocidade vento < 25 km/h, visibilidade > 2 km |
| **\`pista_livre\`** | Câmera + GPS | Nenhum módulo ocupando zona de pouso |
| **\`sensores_ok\`** | Auto-diagnóstico | Sistema de sensores operacional e calibrado |

### 2.2 Função Booleana de Autorização

A decisão de autorizar pouso é modelada por uma **função booleana de porta lógica**:

```
AUTORIZAR_POUSO = combustivel_ok AND clima_ok AND pista_livre AND sensores_ok
```

**Interpretação em linguagem natural:**
- O módulo será autorizado a pousar **se e somente se** todas as 4 condições forem verdadeiras
- Se **qualquer uma** for falsa, o pouso será **negado e adiado**

### 2.3 Tabela de Verdade

| combustível_ok | clima_ok | pista_livre | sensores_ok | Resultado |
|---|---|---|---|---|
| 1 | 1 | 1 | 1 | **✓ POUSAR** |
| 1 | 1 | 1 | 0 | ✗ Adiar |
| 1 | 1 | 0 | 1 | ✗ Adiar |
| 1 | 1 | 0 | 0 | ✗ Adiar |
| 1 | 0 | 1 | 1 | ✗ Adiar |
| 1 | 0 | 1 | 0 | ✗ Adiar |
| 1 | 0 | 0 | 1 | ✗ Adiar |
| 1 | 0 | 0 | 0 | ✗ Adiar |
| 0 | 1 | 1 | 1 | ✗ Adiar |
| ... | ... | ... | ... | ... |
| 0 | 0 | 0 | 0 | ✗ Adiar |

**Resumo:** Apenas 1 combinação em 16 resulta em pouso autorizado (taxa de sucesso = 6.25%)

### 2.4 Diagrama de Portas Lógicas (ASCII)

```
                    ┌─────────┐
    combustivel_ok ─┤         │
                    │  AND-4  ├─→ AUTORIZAR_POUSO
    clima_ok ───────┤         │
                    │         │
    pista_livre ────┤         │
                    │         │
    sensores_ok ────┤         │
                    └─────────┘

Legenda: AND-4 = porta lógica AND com 4 entradas
         Saída = 1 apenas se TODAS as entradas = 1
         Saída = 0 se qualquer entrada = 0
```

### 2.5 Implementação em Estruturas Condicionais

No código Python, essa função booleana é traduzida por uma estrutura condicional simples:

```python
def autorizar_pouso(modulo, clima_ok, pista_livre, sensores_ok):
    combustivel_ok = modulo["combustível"] > 30  # Verificação local
    
    # Implementação da porta lógica AND com 4 entradas
    if combustivel_ok and clima_ok and pista_livre and sensores_ok:
        return True  # Pouso autorizado
    else:
        return False  # Pouso negado
```

**Mapeamento:**
- Cada variável booleana é um fio elétrico (1 = True, 0 = False)
- O operador \`and\` é a porta lógica AND
- Qualquer entrada falsa faz a saída ser falsa (comportamento AND)

### 2.6 Regras Adicionais de Segurança

Além da porta AND principal, há **regras secundárias** implementadas como monitoramento:

```
SE combustível < 30 L ENTÃO adicionar módulo à lista_alerta
SE modulo não autorizado ENTÃO mover para modulos_espera
SE modulo em alerta ≥ 3 ciclos ENTÃO notificar operação terrestre
```

---

## 3. Protótipo Python do MGPEB

### 3.1 Arquivo \`mgpeb.py\` - Análise Estrutural

O protótipo implementa 5 componentes principais, conforme especificação da atividade:

#### **A. Estruturas de Dados Lineares**

```python
from collections import deque

fila_pouso = deque()           # Fila FIFO de módulos aguardando
modulos_pousados = []          # Lista de pousados com sucesso
modulos_espera = []            # Lista de módulos em retry
modulos_alerta = []            # Lista de módulos com crítica
historico = []                 # Pilha de decisões (LIFO)
```

**Análise:**
- \`deque()\` é otimizada para operações FIFO (\`.append()\` e \`.popleft()\`)
- Listas simples usadas para acesso O(1) e compatibilidade com \`sorted()\`
- Histórico como lista (funciona como pilha para contexto simples)

#### **B. Cadastro de Módulos**

```python
def criar_modulo(nome, prioridade, combustivel, massa, criticidade, horario):
    return {
        "nome": nome,
        "prioridade": prioridade,
        "combustível": combustível,
        "massa": massa,
        "criticidade": criticidade,
        "horário": horário
    }

# Instanciação dos 5 módulos da missão Aurora Siger
fila_pouso.append(criar_modulo("Habitação", 5, 80, 2000, 9, 10))
fila_pouso.append(criar_modulo("Energia", 9, 60, 3000, 10, 9))
fila_pouso.append(criar_modulo("Laboratório", 7, 50, 2500, 8, 11))
fila_pouso.append(criar_modulo("Suporte Médico", 10, 40, 1800, 10, 8))
```

**Análise:**
- Função de fábrica padrão (factory pattern simplificado)
- Cada módulo é um dicionário com campos que correspondem aos atributos da Tabela 1.1
- Facilita extensibilidade: novos campos podem ser adicionados sem quebra de lógica

#### **C. Algoritmos de Busca**

```python
def buscar_menor_combustivel(lista):
    menor = lista[0]
    for modulo in lista:
        if modulo["combustível"] < menor["combustível"]:
            menor = modulo
    return menor

def buscar_maior_prioridade(lista):
    maior = lista[0]
    for modulo in lista:
        if modulo["prioridade"] > maior["prioridade"]:
            maior = modulo
    return maior
```

**Análise:**
- **Tipo:** Busca linear (O(n))
- **Função 1:** Localiza módulo com **menor combustível** (para alocar recursos)
- **Função 2:** Localiza módulo com **maior prioridade** (para alocar pista)
- **Limitação:** Não trata listas vazias (pré-requisito: lista com ≥1 elemento)
- **Otimização potencial:** Implementar busca binária se lista estivesse ordenada

#### **D. Algoritmo de Ordenação**

```python
def ordenar_por_prioridade(lista):
    return sorted(lista, key=lambda x: x["prioridade"], reverse=True)
```

**Análise:**
- **Tipo:** Ordenação por chave (usa Timsort internamente, O(n log n))
- **Critério:** Prioridade em ordem decrescente (máxima primeiro)
- **Uso:** Reorganizar fila antes de simulação para garantir módulos críticos pousem primeiro
- **Lambda:** Função anônima que extrai campo \`prioridade\` de cada módulo

#### **E. Função de Autorização de Pouso (Portas Lógicas)**

```python
def autorizar_pouso(modulo, clima_ok, pista_livre, sensores_ok):
    combustivel_ok = modulo["combustível"] > 30
    
    if combustivel_ok and clima_ok and pista_livre and sensores_ok:
        return True
    else:
        return False
```

**Análise:**
- **Implementação direta** da função booleana com porta AND-4
- **Verificação local:** Combustível extraído do objeto módulo
- **Parâmetros globais:** Clima, pista e sensores simulados externamente
- **Correspondência:** Mapeia a tabela de verdade (Seção 2.3) diretamente

#### **F. Simulação Principal**

```python
def simular_pouso():
    global fila_pouso

    # Passo 1: Ordenar fila por prioridade
    fila_ordenada = ordenar_por_prioridade(list(fila_pouso))
    fila_pouso = deque(fila_ordenada)

    # Passo 2: Definir condições simuladas
    clima_ok = True
    pista_livre = True
    sensores_ok = True

    # Passo 3: Processar fila
    while fila_pouso:
        modulo = fila_pouso.popleft()  # Remove primeiro da fila
        
        # Passo 4: Aplicar regra de decisão
        autorizado = autorizar_pouso(modulo, clima_ok, pista_livre, sensores_ok)

        if autorizado:
            modulos_pousados.append(modulo)
            historico.append(f"Pouso autorizado: {modulo['nome']}")
            print(f"{modulo['nome']} POUSOU com sucesso!")
        else:
            modulos_espera.append(modulo)
            historico.append(f"Pouso negado: {modulo['nome']}")
            print(f"{modulo['nome']} EM ESPERA!")

        # Passo 5: Verificar criticidade
        if modulo["combustível"] < 30:
            modulos_alerta.append(modulo)
            print(f"ALERTA: {modulo['nome']} com pouco combustível!")

# Execução
print("=== INICIANDO SIMULAÇÃO MGPEB ===\\n")
simular_pouso()

print("\\n=== RELATÓRIO FINAL ===")
print("Pousados:", [m["nome"] for m in modulos_pousados])
print("Em espera:", [m["nome"] for m in modulos_espera])
print("Alertas:", [m["nome"] for m in modulos_alerta])
```

**Fluxo de Execução:**

1. **Ordenação**: Reordena fila para priorizar módulos críticos
2. **Inicialização**: Define condições simuladas (em operação real, viriam de sensores)
3. **Processamento**: Loop sobre cada módulo da fila
4. **Decisão**: Aplica função booleana AND-4
5. **Registro**: Atualiza listas de status + histórico
6. **Monitoramento**: Verifica combustível para gerar alertas

### 3.2 Complexidade de Algoritmos

| Operação | Função | Complexidade | Justificativa |
|----------|--------|--------------|--------------|
| Busca linear | \`buscar_menor_combustivel()\` | O(n) | Percorre lista inteira |
| Busca linear | \`buscar_maior_prioridade()\` | O(n) | Percorre lista inteira |
| Ordenação | \`ordenar_por_prioridade()\` | O(n log n) | Timsort (Python) |
| Autorizar pouso | \`autorizar_pouso()\` | O(1) | Operações booleanas/comparação |
| Simulação completa | \`simular_pouso()\` | O(n²) | n iterações × O(n) para ordenação inicial |

**Nota:** Para 4-5 módulos, essas complexidades são negligenciáveis. Em operação real com centenas de módulos, seria recomendado: priority queue, índices, ou busca binária.

### 3.3 Como Executar o Protótipo

```bash
cd projeto_decolagem_da_missao-fase2
python3 mgpeb.py
```

**Saída esperada:**
```
=== INICIANDO SIMULAÇÃO MGPEB ===

Energia POUSOU com sucesso!
Suporte Médico POUSOU com sucesso!
Laboratório POUSOU com sucesso!
Habitação POUSOU com sucesso!

=== RELATÓRIO FINAL ===
Pousados: ['Energia', 'Suporte Médico', 'Laboratório', 'Habitação']
Em espera: []
Alertas: []
```

---

## 4. Modelagem Matemática Aplicada

### 4.1 Fenômeno Escolhido: Consumo de Combustível Durante o Pouso

**Justificativa da escolha:**
- Fenômeno crítico para operação (combustível é recurso finito)
- Influencia decisão de autorizar pouso (variável \`combustivel_ok\`)
- Correlaciona com tempo de descida e manobras de estabilização
- Permite modelagem realista com funções elementares

### 4.2 Modelo Matemático

**Cenário físico:** Um módulo em órbita inicia descida com combustível inicial C₀. Durante t segundos, realiza manobras de estabilização (acionamento de retrofoguetes e thrusters laterais). O consumo é proporcional ao tempo e intensidade das manobras.

**Função escolhida: Função Linear (com aceleração de consumo na fase crítica)**

Para simplificar e manter compatibilidade com conteúdo do curso, usaremos inicialmente a forma **linear simples**:

$$C(t) = C_0 - r \\cdot t$$

**Parâmetros:**
- **C₀** = Combustível inicial (litros) → Valor típico: 60 L
- **r** = Taxa de consumo constante (L/s) → Valor típico: 0.5 L/s
- **t** = Tempo decorrido desde início da descida (segundos)
- **C(t)** = Combustível remanescente em tempo t (litros)

**Domínio:**
- t ∈ [0, t_pouso] onde t_pouso é o tempo de descida até toque na superfície
- Tipicamente: t_pouso ≈ 120 segundos (2 minutos de manobra)

**Contradomínio:**
- C(t) ∈ [0, C₀]
- Quando C(t) = 30, o módulo atinge nível de alerta (margem de segurança)

### 4.3 Análise Qualitativa

**Características da função C(t) = C₀ - r·t:**

1. **Forma**: Reta com inclinação negativa
   - Coeficiente angular = -r (negativo → decrescimento)
   - Cada segundo, combustível diminui por taxa r

2. **Interceptos**:
   - Intercepto vertical: C(0) = C₀ (combustível inicial)
   - Intercepto horizontal: t* = C₀/r (tempo em que C(t) = 0)

3. **Monotonidade**: Função **estritamente decrescente**
   - dC/dt = -r < 0 para todo t
   - Combustível nunca aumenta (lei da conservação)

4. **Ponto crítico**: Quando C(t) = 30 L
   - Tempo crítico: t_crítico = (C₀ - 30) / r
   - Exemplo: Se C₀ = 60 e r = 0.5, então t_crítico = 60 segundos

### 4.4 Exemplo Numérico

Considere o módulo **Energia** com C₀ = 60 L e r = 0.5 L/s:

| Tempo (s) | C(t) = 60 - 0.5·t (L) | Status | Ação |
|-----------|------|--------|--------|
| 0 | 60.0 | ✓ Normal | Continuar manobra |
| 30 | 45.0 | ✓ Normal | Continuar manobra |
| 60 | 30.0 | ⚠️ Crítico | **ALERTA** - Preparar pouso de emergência |
| 90 | 15.0 | 🔴 Crítico | **ALERTA MÁXIMA** - Abrir paraquedas de emergência |
| 120 | 0.0 | 🔴 Vazio | **FALHA** - Módulo sem combustível (queda livre) |

### 4.5 Relação com Decisões de Engenharia do MGPEB

**Como essa função orienta o sistema:**

1. **Cálculo de Margem de Segurança**: O MGPEB calcula t_crítico para cada módulo:
   ```
   t_crítico = (combustível - 30) / taxa_consumo
   
   Se t_crítico < 60 segundos:
       → Priorizar pouso IMEDIATAMENTE (pista fica livre)
       → Negar novos pousos até este terminar
   ```

2. **Reordenação Dinâmica da Fila**: Módulos com t_crítico menor sobem na prioridade:
   ```
   Prioridade_ajustada = prioridade_nominal + (120 - t_crítico) × peso
   ```

3. **Acionamento de Retrofoguetes**: Sistema sabe que precisa:
   - 120 segundos totais de manobra
   - t_crítico segundos para fazer "braking" (desaceleração)
   - Restante para estabilização lateral e ajuste fino

4. **Limite de Módulos Simultâneos**: O MGPEB garante que:
   ```
   Número de módulos em pouso simultâneo ≤ (tempo_pouso) / t_crítico_máximo
   
   Exemplo: Se t_crítico_máximo = 60s e tempo_pouso = 120s:
   → Máximo 2 módulos pousando em paralelo (em pistas diferentes)
   ```

### 4.6 Visualização Gráfica (ASCII)

```
Combustível (L)
    |
 60 |●  (t=0, C₀=60)
    |  ╲
 50 |    ╲
    |      ╲
 40 |        ╲
    |          ╲
 30 |━━━━━━━━━●━━━━━━  ← ALERTA (t=60)
    |            ╲
 20 |              ╲
    |                ╲
 10 |                  ╲
    |                    ╲
  0 |━━━━━━━━━━━━━━━━━━━●  ← VAZIO (t=120)
    └─────────────────────────→ Tempo (s)
      0    30    60    90   120

Legenda:
● = Ponto de interesse
╲ = Trajetória linear decrescente
━ = Linhas de referência (alerta, vazio)
```

### 4.7 Extensões Futuras (Fora do Escopo Atual)

Para aumentar realismo (em fases futuras):

- **Modelo com aceleração variável**: C(t) = C₀ - r₁·t - r₂·t² (parábola)
  - r₂ > 0: consumo aumenta conforme retrofoguetes precisam trabalhar mais

- **Modelo exponencial**: C(t) = C₀ · e^(-kt)
  - Mais realista para dinâmica de propulsão

- **Sistema de equações diferenciais**: dC/dt = -r(t, a(t))
  - Onde r depende da aceleração instantânea

---

## 5. Contexto Histórico e Evolução da Computação

### 5.1 Trajetória: Computadores Gerais → Sistemas Embarcados Críticos

A história da computação pode ser dividida em eras:

| Era | Período | Características | Exemplo |
|-----|---------|-----------------|---------|
| **Computadores Gerais (Mainframe)** | 1940s-1960s | Gigantescos, processam múltiplas tarefas, ciclos lentos, confiabilidade moderada | IBM System/360 |
| **Computadores Pessoais** | 1970s-1990s | Portabilidade, aumento de poder de processamento, início de sistemas embarcados | Apple II, IBM PC |
| **Era da Internet** | 1990s-2000s | Conectividade, computação distribuída, aplicações tolerantes a falhas | Servidores Web, PCs em rede |
| **Computação Embarcada** | 2000s-presente | Processadores especializados, restrições severas, operação contínua, **confiabilidade crítica** | Aviônicos, marcapassos, rovers espaciais |

**Transição-chave:** A exploração espacial (Apollo, Viking, Curiosity) acelerou a demanda por sistemas embarcados que funcionassem sob condições extremas com **confiabilidade de 99.9%+**.

### 5.2 Limitações Típicas de Hardware em Missão Marte

Diferente de computadores terrestres, uma missão marciana enfrenta:

#### **Memória (RAM / ROM)**
- **Limite típico:** 2-8 GB RAM (vs. 16-32 GB em laptops modernos)
- **Razão:** Peso, consumo de energia, radiação degrada chips
- **Impacto no MGPEB:** Não podemos armazenar histórico completo de 5 anos; deve-se usar estruturas compactas (linked lists eficientes, não matrizes pré-alocadas)

#### **Processamento (CPU)**
- **Frequência:** 1-2 GHz (vs. 3-5 GHz em CPUs modernas)
- **Razão:** Dissipação térmica em ambiente de -60°C demanda menos potência, reduz aquecimento
- **Impacto no MGPEB:** O(n²) é aceitável para n ≤ 10 módulos; acima disso, seria problema

#### **Consumo de Energia**
- **Orçamento anual:** ~200-300 kWh para toda a base (inclui habitação, lab, etc.)
- **Razão:** Painéis solares marcianos geram ~70% da potência terrestre; ambiente marciano é ~24% da luminosidade
- **Impacto no MGPEB:** Algoritmos devem minimizar computação (prefira O(n) vs. O(n log n) quando diferença for pequena); sensores devem estar em idle entre consultas

#### **Tolerância à Radiação**
- **Dose anual em Marte:** ~230 mrad (vs. 0.3 mrad na Terra)
- **Efeito:** Bit flips aleatórios em memória (especialmente DRAM)
- **Impacto no MGPEB:** Implementar verificação de integridade (checksums, parity bits) em estruturas críticas; usar arquitetura redundante (triple modular redundancy) para decisões de pouso

#### **Comunicação com Terra**
- **Latência:** 3-22 minutos (um sentido) conforme distância orbital
- **Bandwidth:** ~1 Mbps (downlink), ~100 kbps (uplink) em condições ideais
- **Impacto no MGPEB:** Sistema deve ser **autônomo**. Não pode esperar aprovação da Terra a cada pouso. Decisões são locais e irrevogáveis.

### 5.3 Como Essas Limitações Influenciam MGPEB

#### **1. Escolha de Estruturas de Dados**

| Estrutura | Razão da Escolha |
|-----------|-----------------|
| Fila (\`deque\`) | Operações O(1), não requer alocação dinâmica frequente |
| Listas simples | RAM é limitada; evita overhead de objetos complexos |
| Pilha para histórico | Só retém N decisões mais recentes; histórico completo inacessível |
| Dicionários (módulos) | Python é dinamicamente tipado; alternativa seria struct em C (mais rápido, menos memória) |

**Limitação**: Não usamos \`heapq\` (priority queue) apesar de ser O(log n), porque:
- Overhead de memória para manter invariante de heap
- Para n ≤ 5, O(n) em busca linear é mais simples e suficiente
- Sistema embarcado: simplicidade reduz falhas

#### **2. Escolha de Algoritmos**

| Algoritmo | Escolha |
|-----------|---------|
| Busca linear | O(n) vs. O(log n) binária; mas: lista não está *sempre* ordenada, reordenar custa mais |
| Timsort (\`sorted()\`) | Excelente para dados parcialmente ordenados (caso real); melhor que quicksort médio |
| Autorização com portas AND | Operação booleana: O(1), mínimo consumo de CPU |
| Sem recursão profunda | Risco de estouro de pilha; iterativo é preferido |

#### **3. Estratégia de Programação**

**Princípios adotados no MGPEB:**

- **Determinismo**: Função autorizar_pouso() sempre executa em tempo constante (sem branch imprevisível)
- **Robustez**: Listas de alerta/espera servem como fallback se fila principal ficar corrompida
- **Auditoria**: Histórico permite revisar decisão tomada em caso de anomalia
- **Modularidade**: Funções pequenas, responsabilidade única (facilita testing & debug via TX de dados para Terra)
- **Sem alocação dinâmica durante crítica operação**: Todos os módulos alocados na inicialização

### 5.4 Comparação com Rovers Históricos

**Apollo Guidance Computer (1969):**
- RAM: 4 KB (!)
- CPU: 1 MHz
- Sem possibilidade de decisões autônomas
- Computações eram feitas na Terra; astronautas executavam commands

**Mars Rover Curiosity (2012):**
- RAM: 2 GB
- CPU: 200 MHz dual-core
- Sistemas autônomos para navegação e ciência
- Decisões locais sobre qual rocha analisar

**Aurora Siger Base (2026):**
- RAM: 4-8 GB (base + múltiplos subsistemas)
- CPU: 1-2 GHz multi-core
- Sistemas autônomos para governança operacional
- Decisões críticas: alocação de recursos, sequência de pousos, gestão energética
- **Diferença:** Base é *estacionária e permanente*, não rover; requer disponibilidade 24/7/365

---

## 6. Princípios ESG na Base Aurora

### 6.1 Governança Ambiental (E - Environment)

#### **Questão Central:** Como selecionar e gerenciar o impacto da área de pouso no ambiente marciano?

**Critérios de Seleção de Área de Pouso:**

1. **Minimizar Alteração do Regolito**
   - Preferir áreas já impactadas (ex: cratera com exposição mineral)
   - Evitar depósitos de gelo de água ou CO₂ (potencial futuro para recurso)
   - Mapear via satélite: evitar ravinas ativas (risco de colapso)

2. **Proximidade a Recursos Marcianos**
   - Água subterrânea: locais com baixa altitude (vale Hellas Planitia, Valles Marineris)
   - Depósitos de ferro: reduz necessidade de importação da Terra
   - Rochas vulcânicas: fonte de minerais, potencial para energia geotérmica

3. **Condições Atmosféricas Previsíveis**
   - Altitudes baixas = pressão atmosférica mais alta (facilita pouso)
   - Regiões com pouca atividade de dust storms sazonais
   - Latitude favorável para painéis solares (equador recebe mais insolação anual)

4. **Radiação e Proteção Geomagnética**
   - Evitar regiões com anomalias magnéticas locais (aumentam exposição a radiação cósmica)
   - Preferir regiões próximas a estruturas geológicas que ofereçam blindagem natural

**Exemplo de Seleção: Plateau de Syrtis Major**
- Altitude: ~1 km abaixo de referência marciana
- Proximidade: Jazidas de hematita (Fe₂O₃) a ~50 km
- Radiação: Anomalia magnética próxima oferece proteção passiva
- Impacto: Pouso não destrói gelo crítico; reduz ciclos de importação da Terra

#### **Gestão Ambiental Pós-Pouso:**

- **Craterização controlada:** Retrofoguetes criam crateras; regolito ejetado mapeado e estudado
- **Zoneamento:** Área industrial (hangares de manutenção) separada de área científica
- **Investigação paleontológica:** Antes de escavações, buscar sinais de vida microbiana ancestral
- **Protocolo de não-contaminação:** Não introduzir microrganismos terrestres em ambiente não-estudado

---

### 6.2 Governança Social (S - Social)

#### **Questão Central:** Como garantir que decisões críticas sobre tecnologia e recursos sejam éticas e inclusivas, mesmo em ambiente remoto?

**Princípios de Governança Social para Aurora:**

1. **Tomada de Decisão Descentralizada**
   - Sistema MGPEB não é "caixa preta": decisões são auditáveis
   - Conselho de módulos: representantes de cada especialidade (habitação, energia, ciência) votam em alocação de recursos
   - Transparência: histórico de pouso é acessível a todos (não apenas operadores)

2. **Equidade no Acesso a Recursos**
   - Combustível é recurso finito; algoritmo de priorização deve ser consensual
   - Não favorecer pesquisa sobre sobrevivência (conflito de interesse)
   - Mecanismo: Prioridade base + bônus por criticidade + malus por solicitações repetidas (evita monopólio)

3. **Segurança Psicológica e Operacional**
   - Documentação multilíngue de procedimentos (não apenas inglês)
   - Treinamento contínuo: cada membro sabe como MGPEB funciona
   - Simulações regulares: equipe pratica falhas de cenários (combustível crítico, pista danificada, etc.)

4. **Representação e Inclusão**
   - Composição da equipe reflete diversidade terrestre (gênero, origem, formação)
   - Diversidade cognitiva melhora resolução de problemas em ambiente stressante

**Exemplo Prático:** Módulo de Suporte Médico com combustível crítico
```
Cenário: Suporte Médico = 40L combustível, Energia = 60L, ambas pousando hoje

Decisão sem governance social:
  MGPEB: Pousa Energia (maior prioridade por criticidade)
  Resultado: Suporte Médico adia 6 horas

Decisão com governance social:
  Conselho debate:
    - Médico: "Possível emergência médica; precisamos módulo hoje"
    - Engenheiro de energia: "Baterias duram 18h; Energia pode adiar 12h"
    - Consenso: Energia adia, Suporte Médico pousa primeiro
  MGPEB reprograma ordem; ambos pousam no dia

Diferença: Inclusão previne decisões sub-ótimas fruto de prioridades singulares
```

---

### 6.3 Governança Corporativa (G - Governance)

#### **Questão Central:** Como estruturar autoridade, accountability e mecanismos de controle em uma base autônoma?

**Estrutura de Governance para Aurora:**

```
┌─────────────────────────────────────────────────────┐
│            Conselho de Base Aurora                  │
│  (5 membros + 1 representante via TX com Terra)   │
│  Autoridade: Decisões estratégicas, alocação       │
│  orçamentária, conflitos não-resolvidos             │
└────────────────────────┬────────────────────────────┘
                         │
         ┌───────────────┼────────────────┐
         │               │                │
┌────────▼────────┐ ┌──▼────────────┐ ┌─▼────────────┐
│ Diretor Técnico │ │Dir. Científica │ │Dir. Operações│
│ (Engenharia)    │ │ (Pesquisa)     │ │ (Logística)  │
│                 │ │                │ │              │
│ Auditoria:      │ │ Auditoria:     │ │ Auditoria:   │
│ - Integridade   │ │ - Protocolo de │ │ - Conformidade
│   de sensores   │ │   contaminação │ │   ESG        │
│ - Eficiência    │ │ - Dados únicos  │ │ - Falhas     │
│   energética    │ │ - IP científico│ │ - Histórico  │
└────────────────┘ └────────────────┘ └─────────────┘
                         │
                         ▼
         ┌──────────────────────────────┐
         │  MGPEB (Sistema Autônomo)   │
         │  Executor de decisões       │
         │  Implementa policy do       │
         │  Conselho de Base            │
         └──────────────────────────────┘
```

**Mecanismos de Accountability:**

1. **Auditoria Contínua**
   - Todos os comandos de pouso registrados com timestamp
   - Verificação semanal: MGPEB cumpre policies aprovadas?
   - Anomalias (ex: Suporte Médico adiado 3x seguidas) triggers investigação

2. **Escalation de Conflitos**
   - Primeira instância: Sistema automático (regras booleanas)
   - Segunda instância: Supervisão humana (Diretor Técnico)
   - Terceira instância: Conselho de Base (votação)

3. **Documentação e Justificativa**
   - Cada decisão deve ter rastreabilidade
   - Exemplos:
     ```
     [2026-04-01 09:15:32] MÓDULO=Energia | STATUS=POUSAR
     Razão: combustível=60L > 30L ✓, clima_ok=1 ✓, 
             pista_livre=1 ✓, sensores_ok=1 ✓
     Autorizado por: MGPEB v2.1 | Supervisionado por: Eng. Silva
     
     [2026-04-01 09:17:42] MÓDULO=Suporte_Médico | STATUS=ADIAR
     Razão: combustível=40L > 30L ✓, clima_ok=1 ✓,
             pista_livre=0 ✗ (Energia ocupando)
     Autorizado por: MGPEB v2.1 | Supervisionado por: Eng. Silva
     ```

4. **Revisão Periódica de Policies**
   - Trimestral: Conselho reúne para avaliar desempenho de MGPEB
   - Dados analisados: taxa de sucesso, anomalias, feedback operacional
   - Ajustes dinâmicos: regras booleanas podem evoluir conforme aprendizado

**Exemplo: Política de Combustível Crítico**

Policy atual (fase 1):
```
SE combustível < 30L ENTÃO adicionar à lista_alerta
```

Após 6 meses de operação:
```
Conselho identifica: Módulos em alerta experimentam adiamentos em cascata
Proposta: Reduzir limite de crítica para 25L (ganha margem de manobra)

Votação:
  - Diretor Técnico: SIM (reduz falsos positivos)
  - Diretora Científica: NÃO (menor margem é risco)
  - Diretor de Operações: SIM (melhor throughput)
  
Resultado: 2x1 a favor
Nova policy implementada em v2.2 do MGPEB
```

---

### 6.4 Integração ESG no MGPEB

**Como ESG influencia o design técnico:**

| Aspecto | Requisito ESG | Implementação MGPEB |
|--------|---------------|-----------------|
| **Ambiental** | Minimizar impacto em recurso marciano (água) | Histórico completo de pousos em zona protegida; auditoria anual |
| **Social** | Transparência em alocação de recursos | Histórico acessível; explicação de cada decisão de adiamento |
| **Corporativo** | Rastreabilidade de decisões críticas | Pilha de histórico; checksums para integridade |
| **Ambiental** | Eficiência energética | Algoritmos O(n) preferidos; sensores em idle; computação batch (não contínua) |
| **Social** | Segurança psicológica | Documentação clara; simulações de falha; debate prévia antes de mudança de rules |
| **Corporativo** | Revisão periódica | Conselho reúne trimestralmente; políticas evoluem via votação |

---

## 7. Conclusão

### 7.1 Síntese do Projeto MGPEB

O **MGPEB (Módulo de Gerenciamento de Pouso e Estabilização de Base)** representa um sistema integrado que combina:

- **Estruturas de dados lineares** (fila, listas, pilha) para gerenciar fluxo operacional
- **Lógica booleana e portas AND** para decisões de segurança crítica
- **Algoritmos clássicos** (busca linear, Timsort) adaptados a restrições de hardware embarcado
- **Modelagem matemática** (função linear de consumo de combustível) para previsão operacional
- **Contexto histórico** (evolução de computadores gerais → embarcados críticos) para justificar design
- **Princípios ESG** (ambiental, social, corporativo) para garantir operação ética e sustentável

### 7.2 Inovações Técnicas

1. **Porta Lógica AND-4 Simplificada**: Todas as 4 condições devem ser satisfeitas; sem hierarquia (evita decisões enviesadas por prioridade)

2. **Auditoria por Pilha**: Histórico funciona como "caixa preta" para investigação pós-incidente

3. **Reordenação Dinâmica**: Fila se reordena por prioridade antes de cada ciclo, evitando starvation

4. **Alertas Tiered**: Combustível < 30L gera alerta, mas não bloqueia automaticamente (permite intervenção humana)

### 7.3 Adaptabilidade e Evolução

O projeto foi concebido para ser **modular e evolutivo**:

- **Fase 1 (atual):** 5 módulos, 4 condições de autorização, decisão automática
- **Fase 2:** Priority queue para n > 10 módulos, integração com sensor real de clima
- **Fase 3:** Machine learning para prever falhas de sensores; redundância ativa
- **Fase 4:** Swarm de mini-bases coordenadas via MGPEB distribuído

### 7.4 Lições de Engenharia Aplicada

Este projeto ilustra como conceitos de **lógica computacional, matemática aplicada e governança** convergem em sistemas reais:

- **Simplicidade vence:** Portas AND simples > lógica fuzzy complexa (em sistema crítico)
- **Documentação é código:** Histórico auditável > código sem rastreabilidade
- **Sustentabilidade é design:** ESG não é "compliance", é decisão arquitetural
- **Hardware limita:** O(n²) é aceitável aqui, seria inaceitável em IoT de baixo custo

---

## Referências & Recursos Adicionais

### Estruturas de Dados
- Python \`collections.deque\`: O(1) append/pop em ambas extremidades
- Timsort: Algoritmo de ordenação adaptativo, O(n) para dados parcialmente ordenados

### Algoritmos
- Busca Linear: O(n), determinística, sem pré-requisitos
- Sorted: O(n log n), estável, apropriado para listas pequenas

### Computação Embarcada & Espacial
- "The Lunar Module Computer" (1969): 4 KB RAM, 1 MHz CPU
- "Curiosity Rover Software Architecture" (JPL 2012)
- Mars Atmospheric Dynamics (NASA/GISS): Modelos climáticos de Marte

### ESG em Tecnologia
- ISO 14001 (Gestão Ambiental)
- SA 8000 (Responsabilidade Social)
- ISO 37001 (Compliance & Governance)

---

## Instruções de Execução

### Instalação
```bash
# Verificar Python 3.x
python3 --version

# Clonar repositório
git clone https://github.com/allanvictorsantos/projeto_decolagem_da_missao-fase2

# Acessar pasta do projeto
cd projeto_decolagem_da_missao-fase2
```

### Executar Simulação
```bash
python3 mgpeb.py
```

### Saída Esperada
```
=== INICIANDO SIMULAÇÃO MGPEB ===

Energia POUSOU com sucesso!
Suporte Médico POUSOU com sucesso!
Laboratório POUSOU com sucesso!
Habitação POUSOU com sucesso!

=== RELATÓRIO FINAL ===
Pousados: ['Energia', 'Suporte Médico', 'Laboratório', 'Habitação']
Em espera: []
Alertas: []
```
