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
    # Estado inicial
    trace.append({"alg": "Insertion", "target_key_idx": 0, "target_key_val": v[0], "curr_j": -1, "array": list(v), "desc": "Início"})
    
    for i in range(1, len(v)):
        target_key = v[i]
        j = i - 1
        trace.append({"alg": "Insertion", "target_key_idx": i, "target_key_val": target_key, "curr_j": j, "array": list(v), "desc": f"Seleciona {target_key}"})
        
        while j >= 0 and v[j] > target_key:
            v[j + 1] = v[j]
            trace.append({"alg": "Insertion", "target_key_idx": i, "target_key_val": target_key, "curr_j": j, "array": list(v), "desc": f"Move {v[j]} para a direita"})
            j -= 1
        
        v[j + 1] = target_key
        trace.append({"alg": "Insertion", "target_key_idx": i, "target_key_val": target_key, "curr_j": j + 1, "array": list(v), "desc": f"Insere {target_key} na posição {j+1}"})
        
    return save_trace_to_json(trace, filename)


# Gerar rastro de execução para Bubble Sort
def gen_bubble_sort(v, filename=LOG_FILE_NAME):
    trace = []
    n = len(v)
    trace.append({"alg": "Bubble", "i": -1, "j": -1, "j_next": -1, "action": "start", "array": list(v), "desc": "Início"})
    
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            trace.append({"alg": "Bubble", "i": i, "j": j, "j_next": j+1, "action": "compare", "array": list(v), "desc": f"Compara {v[j]} e {v[j+1]}"})
            if v[j] > v[j + 1]:
                v[j], v[j + 1] = v[j + 1], v[j]
                swapped = True
                trace.append({"alg": "Bubble", "i": i, "j": j, "j_next": j+1, "action": "swap", "array": list(v), "desc": f"Troca {v[j]} com {v[j+1]}"})
        
        if not swapped:
            break
            
    trace.append({"alg": "Bubble", "i": -1, "j": -1, "j_next": -1, "action": "finished", "array": list(v), "desc": "Ordenação Concluída"})
    return save_trace_to_json(trace, filename)


# Gerar rastro de execução para Selection Sort
def gen_selection_sort(v, filename=LOG_FILE_NAME):
    trace = []
    n = len(v)
    trace.append({"alg": "Selection", "i": -1, "curr": -1, "min_idx": -1, "action": "start", "array": list(v), "desc": "Início"})

    for i in range(n):
        min_idx = i
        trace.append({"alg": "Selection", "i": i, "curr": i, "min_idx": min_idx, "action": "start_pass", "array": list(v), "desc": f"Define mínimo inicial como {v[min_idx]}"})
        
        for j in range(i + 1, n):
            trace.append({"alg": "Selection", "i": i, "curr": j, "min_idx": min_idx, "action": "compare", "array": list(v), "desc": f"Compara {v[j]} com mínimo atual {v[min_idx]}"})
            if v[j] < v[min_idx]:
                min_idx = j
                trace.append({"alg": "Selection", "i": i, "curr": j, "min_idx": min_idx, "action": "new_min", "array": list(v), "desc": f"Novo mínimo encontrado: {v[min_idx]}"})
        
        if min_idx != i:
            v[i], v[min_idx] = v[min_idx], v[i]
            trace.append({"alg": "Selection", "i": i, "curr": n, "min_idx": min_idx, "action": "swap", "array": list(v), "desc": f"Troca {v[i]} com {v[min_idx]}"})
        else:
            trace.append({"alg": "Selection", "i": i, "curr": n, "min_idx": min_idx, "action": "no_swap", "array": list(v), "desc": "Mínimo já está na posição correta"})

    trace.append({"alg": "Selection", "i": -1, "curr": -1, "min_idx": -1, "action": "finished", "array": list(v), "desc": "Ordenação Concluída"})
    return save_trace_to_json(trace, filename)


# Gerar rastro de execução para Quick Sort
def gen_quick_sort(v, filename=LOG_FILE_NAME):
    trace = []
    
    def partition(arr, low, high):
        pivot = arr[high]
        trace.append({"alg": "Quick", "low": low, "high": high, "pivot_idx": high, "i": low-1, "curr": -1, "action": "pivot_select", "array": list(arr), "desc": f"Pivô escolhido: {pivot}"})
        
        i = low - 1
        for j in range(low, high):
            trace.append({"alg": "Quick", "low": low, "high": high, "pivot_idx": high, "i": i, "curr": j, "action": "compare", "array": list(arr), "desc": f"Compara {arr[j]} com pivô {pivot}"})
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                trace.append({"alg": "Quick", "low": low, "high": high, "pivot_idx": high, "i": i, "curr": j, "action": "swap", "array": list(arr), "desc": f"Troca {arr[i]} e {arr[j]}"})
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        trace.append({"alg": "Quick", "low": low, "high": high, "pivot_idx": i + 1, "i": i, "curr": high, "action": "partition_done", "array": list(arr), "desc": f"Pivô {pivot} colocado na posição final {i+1}"})
        return i + 1

    def quick_sort_recursive(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quick_sort_recursive(arr, low, pi - 1)
            quick_sort_recursive(arr, pi + 1, high)

    trace.append({"alg": "Quick", "low": 0, "high": len(v)-1, "pivot_idx": -1, "i": -1, "curr": -1, "action": "start", "array": list(v), "desc": "Início"})
    quick_sort_recursive(v, 0, len(v) - 1)
    trace.append({"alg": "Quick", "low": -1, "high": -1, "pivot_idx": -1, "i": -1, "curr": -1, "action": "finished", "array": list(v), "desc": "Ordenação Concluída"})
    
    return save_trace_to_json(trace, filename)


# Gerar rastro de execução para Merge Sort
def gen_merge_sort(v, filename=LOG_FILE_NAME):
    trace = []
    
    def merge(arr, l, m, r):
        n1 = m - l + 1
        n2 = r - m
        L = arr[l:m+1]
        R = arr[m+1:r+1]
        
        trace.append({"alg": "Merge", "l": l, "m": m, "r": r, "action": "split", "array": list(arr), "desc": f"Intercalando sub-vetores: {L} e {R}"})

        i = j = 0
        k = l
        
        while i < n1 and j < n2:
            trace.append({"alg": "Merge", "l": l, "m": m, "r": r, "curr_k": k, "action": "compare", "array": list(arr), "desc": f"Compara {L[i]} e {R[j]}"})
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            trace.append({"alg": "Merge", "l": l, "m": m, "r": r, "curr_k": k-1, "action": "merge_step", "array": list(arr), "desc": f"Copia valor para posição {k-1}"})

        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1
            trace.append({"alg": "Merge", "l": l, "m": m, "r": r, "curr_k": k-1, "action": "merge_step", "array": list(arr), "desc": "Copia restante da esquerda"})

        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1
            trace.append({"alg": "Merge", "l": l, "m": m, "r": r, "curr_k": k-1, "action": "merge_step", "array": list(arr), "desc": "Copia restante da direita"})

    def merge_sort_recursive(arr, l, r):
        if l < r:
            m = l + (r - l) // 2
            merge_sort_recursive(arr, l, m)
            merge_sort_recursive(arr, m + 1, r)
            merge(arr, l, m, r)

    trace.append({"alg": "Merge", "l": 0, "r": len(v)-1, "action": "start", "array": list(v), "desc": "Início"})
    merge_sort_recursive(v, 0, len(v) - 1)
    trace.append({"alg": "Merge", "l": -1, "r": -1, "action": "finished", "array": list(v), "desc": "Ordenação Concluída"})
    
    return save_trace_to_json(trace, filename)