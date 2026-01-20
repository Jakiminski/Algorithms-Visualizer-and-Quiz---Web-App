import json
import sys
import os
from datetime import datetime
from config import *


# Validar se a entrada é um número inteiro dentro do intervalo permitido
def validate_number(value:str, min_range:int=ARRAY_VALUE_MIN_RANGE, max_range:int=ARRAY_VALUE_MAX_RANGE) -> bool:
    is_negative = False
    value = value.strip()
    
    # Verifica se o número é negativo, separando o sinal
    if value.startswith('-'):
        value = value[1:]  # Remove o sinal para verificação
        is_negative = True
    elif value.startswith('+'):
        value = value[1:]  # Remove o sinal para verificação

    # Checa se o valor da string é numérico
    is_valid = True if value.isdigit() else False
    # Converte para inteiro se válido, senão usa 0
    x = int(value) if is_valid else 0            
    x = -x if is_negative else x
    # Checa se o número está dentro do intervalo permitido
    is_valid = True if min_range <= x <= max_range else False
    
    return is_valid


# Converter a entrada para inteiro, retornando 0 se inválido
def convert_to_int(value:str) -> int:
    value = value.strip()
    is_negative = False
    
    # Verifica se o número é negativo, separando o sinal
    if value.startswith('-'):
        value = value[1:]  # Remove o sinal para verificação
        is_negative = True
    elif value.startswith('+'):
        value = value[1:]  # Remove o sinal para verificação

    # Checa se o valor da string é numérico
    is_valid = True if value.isdigit() else False
    # Converte para inteiro se válido, senão usa 0
    x = int(value) if is_valid else 0            
    x = -x if is_negative else x
    
    return x

# Validar e converter a entrada para inteiro dentro do intervalo permitido
def valid_input(value:str, min_range:int=ARRAY_VALUE_MIN_RANGE, max_range:int=ARRAY_VALUE_MAX_RANGE) -> int:

    value = value.strip()
    output = convert_to_int(value) if validate_number(value, min_range, max_range) else 0
    
    return output

# Obter o caminho absoluto do recurso, útil para PyInstaller
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

LOG_FILE_PATH = get_resource_path(LOG_FILE_NAME)
QUIZ_LOG_PATH = get_resource_path(QUIZ_LOG_FILE_NAME)


# Salvar o rastro de execução em um arquivo JSON
def save_trace_to_json(trace, filename=LOG_FILE_NAME):
    
    full_path = get_resource_path(filename) # Caminho absoluto do arquivo

    # 1. Preparar os metadados desta execução
    execution_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "algoritmo": trace[0]["alg"] if trace else "Desconhecido",
        "tamanho_array": len(trace[0]["array"]) if trace else 0,
        "passos": trace
    }

    # 2. Carregar histórico existente ou criar nova lista
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                history = json.load(f)
                if not isinstance(history, list):
                    history = []
        except (json.JSONDecodeError, IOError):
            history = []
    else:
        history = []

    # 3. Adicionar nova execução e salvar
    history.append(execution_data)
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)
        
    return trace


# Remover o arquivo de log de execução, se existir
def clear_execution_log():
    file_path = LOG_FILE_NAME
    if os.path.exists(file_path):
        os.remove(file_path)
        print("Log de execução removido.")


# Gerar rastro de execução para Busca Linear
def gen_linear_search(v, target_key, filename=LOG_FILE_NAME):
    trace = []
    count_comparisons = 0
    found = False
    for i in range(len(v)):
        count_comparisons += 1 # Incrementa o contador de comparações
        found = (v[i] == target_key)
        state = {"alg": "Busca Linear", "idx": i, "encontrado": found, "finalizado": False, "array": list(v), "target_key": target_key, "comparações": count_comparisons}
        trace.append(state)
        if found: 
            break
    
    # Se percorreu tudo e não achou, adiciona estado de falha
    if not found:
        trace.append({"alg": "Busca Linear", "idx": -1, "encontrado": False, "finalizado": True, "array": list(v), "target_key": target_key, "comparações": count_comparisons})
    return save_trace_to_json(trace, filename)


# Gerar rastro de execução para Busca Binária
def gen_binary_search(v, target_key, filename=LOG_FILE_NAME):
    trace = []
    l, r = 0, len(v) - 1
    count_comparisons = 0
    found = False
    while l <= r:
        m = (l + r) // 2
        count_comparisons += 1 # Incrementa o contador de comparações
        found = (v[m] == target_key)
        state = {"alg": "Busca Binária", "l": l, "r": r, "m": m, "encontrado": found, "finalizado": False, "array": list(v), "target_key": target_key, "comparações": count_comparisons}
        trace.append(state)
        if found: 
            break
        elif v[m] < target_key: 
            l = m + 1
        else: 
            r = m - 1
    
    if not found:
        trace.append({"alg": "Busca Binária", "l": l, "r": r, "m": -1, "encontrado": False, "finalizado": True, "array": list(v), "target_key": target_key, "comparações": count_comparisons})
    return save_trace_to_json(trace, filename)


# Gerar rastro de execução para Insertion Sort
def gen_insertion_sort(v, filename=LOG_FILE_NAME):
    trace = []
    trace.append({"alg": "Insertion", "target_key_idx": 0, "target_key_val": v[0], "curr_j": 0, "array": list(v)})
    for i in range(1, len(v)):
        target_key = v[i]
        j = i - 1
        while j >= 0 and v[j] > target_key:
            v[j + 1] = v[j]
            trace.append({"alg": "Insertion", "target_key_idx": i, "target_key_val": target_key, "curr_j": j, "array": list(v)})
            j -= 1
        v[j + 1] = target_key
        trace.append({"alg": "Insertion", "target_key_idx": i, "target_key_val": target_key, "curr_j": j + 1, "array": list(v)})
    return save_trace_to_json(trace, filename)

