# ==============================
# MGPEB - Sistema de Pouso Marte
# ==============================

# ---------- ESTRUTURAS DE DADOS ----------

from collections import deque

# Fila principal (módulos aguardando pouso)
fila_pouso = deque()

# Listas auxiliares
modulos_pousados = []
modulos_espera = []
modulos_alerta = []

# Pilha (histórico de decisões)
historico = []


# ---------- CADASTRO DE MÓDULOS ----------

def criar_modulo(nome, prioridade, combustivel, massa, criticidade, horario):
    return {
        "nome": nome,
        "prioridade": prioridade,
        "combustivel": combustivel,
        "massa": massa,
        "criticidade": criticidade,
        "horario": horario
    }

# Criando módulos
fila_pouso.append(criar_modulo("Habitação", 5, 80, 2000, 9, 10))
fila_pouso.append(criar_modulo("Energia", 9, 60, 3000, 10, 9))
fila_pouso.append(criar_modulo("Laboratório", 7, 50, 2500, 8, 11))
fila_pouso.append(criar_modulo("Suporte Médico", 10, 40, 1800, 10, 8))


# ---------- BUSCA ----------

def buscar_menor_combustivel(lista):
    menor = lista[0]
    for modulo in lista:
        if modulo["combustivel"] < menor["combustivel"]:
            menor = modulo
    return menor


def buscar_maior_prioridade(lista):
    maior = lista[0]
    for modulo in lista:
        if modulo["prioridade"] > maior["prioridade"]:
            maior = modulo
    return maior


# ---------- ORDENAÇÃO ----------

def ordenar_por_prioridade(lista):
    return sorted(lista, key=lambda x: x["prioridade"], reverse=True)


# ---------- REGRAS LÓGICAS ----------

def autorizar_pouso(modulo, clima_ok, pista_livre, sensores_ok):
    combustivel_ok = modulo["combustivel"] > 30
    
    # Simulação de portas lógicas:
    # (combustivel_ok AND clima_ok AND pista_livre AND sensores_ok)
    if combustivel_ok and clima_ok and pista_livre and sensores_ok:
        return True
    else:
        return False


# ---------- SIMULAÇÃO ----------

def simular_pouso():
    global fila_pouso

    # Ordena fila antes
    fila_ordenada = ordenar_por_prioridade(list(fila_pouso))
    fila_pouso = deque(fila_ordenada)

    # Condições simuladas
    clima_ok = True
    pista_livre = True
    sensores_ok = True

    while fila_pouso:
        modulo = fila_pouso.popleft()
        
        autorizado = autorizar_pouso(modulo, clima_ok, pista_livre, sensores_ok)

        if autorizado:
            print(f"{modulo['nome']} POUSOU com sucesso!")
            modulos_pousados.append(modulo)
            historico.append(f"Pouso autorizado: {modulo['nome']}")
        else:
            print(f"{modulo['nome']} EM ESPERA!")
            modulos_espera.append(modulo)
            historico.append(f"Pouso negado: {modulo['nome']}")

        # Exemplo de alerta
        if modulo["combustivel"] < 30:
            modulos_alerta.append(modulo)
            print(f"ALERTA: {modulo['nome']} com pouco combustível!")


# ---------- EXECUÇÃO ----------

print("=== INICIANDO SIMULAÇÃO MGPEB ===\n")

simular_pouso()

print("\n=== RELATÓRIO FINAL ===")
print("Pousados:", [m["nome"] for m in modulos_pousados])
print("Em espera:", [m["nome"] for m in modulos_espera])
print("Alertas:", [m["nome"] for m in modulos_alerta])