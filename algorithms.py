import json
import sys
import os
from datetime import datetime
from config import *


class InputValidator:
    """Classe responsável por validação e conversão de entrada de usuário."""
    
    @staticmethod
    def validate_number(value: str, min_range: int = ARRAY_VALUE_MIN_RANGE, max_range: int = ARRAY_VALUE_MAX_RANGE) -> bool:
        """Validar se a entrada é um número inteiro dentro do intervalo permitido."""
        is_negative = False
        value = value.strip()
        
        if value.startswith('-'):
            value = value[1:]
            is_negative = True
        elif value.startswith('+'):
            value = value[1:]

        is_valid = value.isdigit()
        x = int(value) if is_valid else 0            
        x = -x if is_negative else x
        is_valid = min_range <= x <= max_range
        
        return is_valid

    @staticmethod
    def convert_to_int(value: str) -> int:
        """Converter a entrada para inteiro, retornando 0 se inválido."""
        value = value.strip()
        is_negative = False
        
        if value.startswith('-'):
            value = value[1:]
            is_negative = True
        elif value.startswith('+'):
            value = value[1:]

        is_valid = value.isdigit()
        x = int(value) if is_valid else 0            
        x = -x if is_negative else x
        
        return x

    @staticmethod
    def valid_input(value: str, min_range: int = ARRAY_VALUE_MIN_RANGE, max_range: int = ARRAY_VALUE_MAX_RANGE) -> int:
        """Validar e converter a entrada para inteiro dentro do intervalo permitido."""
        value = value.strip()
        if InputValidator.validate_number(value, min_range, max_range):
            return InputValidator.convert_to_int(value)
        return 0


class TraceManager:
    """Classe responsável pelo gerenciamento de rastros de execução."""
    
    @staticmethod
    def get_resource_path(relative_path: str) -> str:
        """Obter o caminho absoluto do recurso, útil para PyInstaller."""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    @staticmethod
    def save_trace_to_json(trace: list, filename: str = LOG_FILE_NAME) -> list:
        """Salvar o rastro de execução em um arquivo JSON."""
        full_path = TraceManager.get_resource_path(filename)

        execution_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "algoritmo": trace[0]["alg"] if trace else "Desconhecido",
            "tamanho_array": len(trace[0]["array"]) if trace else 0,
            "passos": trace
        }

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

        history.append(execution_data)
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4, ensure_ascii=False)
            
        return trace

    @staticmethod
    def clear_execution_log(filename: str = LOG_FILE_NAME) -> None:
        """Remover o arquivo de log de execução, se existir."""
        if os.path.exists(filename):
            os.remove(filename)
            print(f"Log de execução {filename} removido.")



# Remover o arquivo de log de execução, se existir
def clear_execution_log():
    file_path = LOG_FILE_NAME
    if os.path.exists(file_path):
        os.remove(file_path)
        print("Log de execução removido.")


class SearchAlgorithms:
    """Classe responsável por algoritmos de busca."""
    
    @staticmethod
    def linear_search(v: list, target_key: int, filename: str = LOG_FILE_NAME) -> list:
        """Gerar rastro de execução para Busca Linear."""
        trace = []
        count_comparisons = 0
        found = False
        for i in range(len(v)):
            count_comparisons += 1
            found = (v[i] == target_key)
            state = {"alg": "Busca Linear", "idx": i, "encontrado": found, "finalizado": False, "array": list(v), "target_key": target_key, "comparações": count_comparisons}
            trace.append(state)
            if found: 
                break
        
        if not found:
            trace.append({"alg": "Busca Linear", "idx": -1, "encontrado": False, "finalizado": True, "array": list(v), "target_key": target_key, "comparações": count_comparisons})
        return TraceManager.save_trace_to_json(trace, filename)

    @staticmethod
    def binary_search(v: list, target_key: int, filename: str = LOG_FILE_NAME) -> list:
        """Gerar rastro de execução para Busca Binária."""
        trace = []
        l, r = 0, len(v) - 1
        count_comparisons = 0
        found = False
        while l <= r:
            m = (l + r) // 2
            count_comparisons += 1
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
        return TraceManager.save_trace_to_json(trace, filename)


class SortingAlgorithms:
    """Classe responsável por algoritmos de ordenação."""
    
    @staticmethod
    def insertion_sort(v: list, filename: str = LOG_FILE_NAME) -> list:
        """Gerar rastro de execução para Insertion Sort."""
        trace = []
        n = len(v)
        trace.append({"alg": "Insertion", "target_key_idx": 0, "target_key_val": v[0], "curr_j": -1, "array": list(v), "desc": "Início"})

        count = 0
        for i in range(1, len(v)):
            target_key = v[i]
            j = i - 1
            trace.append({"alg": "Insertion", "target_key_idx": i, "target_key_val": target_key, "curr_j": j, "array": list(v), "desc": f"Seleciona {target_key}"})
            
            while j >= 0 and v[j] > target_key:
                count += 1
                v[j + 1] = v[j]
                trace.append({"alg": "Insertion", "target_key_idx": i, "target_key_val": target_key, "curr_j": j, "array": list(v), "desc": f"Move {v[j]} para a direita"})
                j -= 1

            if j >= 0: count += 1 # Última comparação que falhou no while
            v[j + 1] = target_key
            is_last = (i == n - 1) # Se for o último elemento (i == n-1), marcamos como finalizado
            trace.append({"alg": "Insertion", "target_key_idx": i, "target_key_val": target_key, "curr_j": j + 1, "array": list(v), "finalizado":is_last, "desc": f"Insere {target_key} na posição {j+1}"})
        
        # Opcional: Adicionar um passo extra garantindo que todos estão verdes
        if trace:
            trace[-1]["finalizado"] = True     
        return TraceManager.save_trace_to_json(trace, filename)

    @staticmethod
    def bubble_sort(v: list, filename: str = LOG_FILE_NAME) -> list:
        """Gerar rastro de execução para Bubble Sort."""
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
        return TraceManager.save_trace_to_json(trace, filename)

    @staticmethod
    def selection_sort(v: list, filename: str = LOG_FILE_NAME) -> list:
        """Gerar rastro de execução para Selection Sort."""
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
        return TraceManager.save_trace_to_json(trace, filename)

    @staticmethod
    def quick_sort(v: list, filename: str = LOG_FILE_NAME) -> list:
        """Gerar rastro de execução para Quick Sort."""
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
        
        return TraceManager.save_trace_to_json(trace, filename)

    @staticmethod
    def merge_sort(v: list, filename: str = LOG_FILE_NAME) -> list:
        """Gerar rastro de execução para Merge Sort."""
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
        
        return TraceManager.save_trace_to_json(trace, filename)


# ============================================================================
# BACKWARD COMPATIBILITY FUNCTIONS
# These functions maintain backward compatibility with existing code
# ============================================================================

def valid_input(value: str, min_range: int = ARRAY_VALUE_MIN_RANGE, max_range: int = ARRAY_VALUE_MAX_RANGE) -> int:
    """Backward compatibility wrapper for InputValidator.valid_input()"""
    return InputValidator.valid_input(value, min_range, max_range)

def gen_linear_search(v: list, target_key: int, filename: str = LOG_FILE_NAME) -> list:
    """Backward compatibility wrapper for SearchAlgorithms.linear_search()"""
    return SearchAlgorithms.linear_search(v, target_key, filename)

def gen_binary_search(v: list, target_key: int, filename: str = LOG_FILE_NAME) -> list:
    """Backward compatibility wrapper for SearchAlgorithms.binary_search()"""
    return SearchAlgorithms.binary_search(v, target_key, filename)

def gen_insertion_sort(v: list, filename: str = LOG_FILE_NAME) -> list:
    """Backward compatibility wrapper for SortingAlgorithms.insertion_sort()"""
    return SortingAlgorithms.insertion_sort(v, filename)

def gen_bubble_sort(v: list, filename: str = LOG_FILE_NAME) -> list:
    """Backward compatibility wrapper for SortingAlgorithms.bubble_sort()"""
    return SortingAlgorithms.bubble_sort(v, filename)

def gen_selection_sort(v: list, filename: str = LOG_FILE_NAME) -> list:
    """Backward compatibility wrapper for SortingAlgorithms.selection_sort()"""
    return SortingAlgorithms.selection_sort(v, filename)

def gen_quick_sort(v: list, filename: str = LOG_FILE_NAME) -> list:
    """Backward compatibility wrapper for SortingAlgorithms.quick_sort()"""
    return SortingAlgorithms.quick_sort(v, filename)

def gen_merge_sort(v: list, filename: str = LOG_FILE_NAME) -> list:
    """Backward compatibility wrapper for SortingAlgorithms.merge_sort()"""

    return SortingAlgorithms.merge_sort(v, filename)
