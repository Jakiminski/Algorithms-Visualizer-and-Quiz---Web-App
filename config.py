import os
import sys

APP_NAME = "Algorithms Visualizer & Quiz"

# Frames
FRAME_MENU = "Menu"
FRAME_SEARCH_ALGORITHMS = "SearchAlgorithms"
FRAME_SORTING_ALGORITHMS = "SortingAlgorithms"
FRAME_QUIZ = "Quiz"

# FIles
LOG_FILE_NAME = "execution_trace.json"
QUIZ_LOG_FILE_NAME = "quiz_trace.json"

# UI SETTINGS

## Menu Buttons

BUTTON_RETURN_TEXT = "VOLTAR"

BUTTON_EXIT_TEXT = "SAIR"

BUTTON_APLICAR_SETUP_ALG = "APLICAR"
BUTTON_ANTERIOR_TEXT = "ANTERIOR"
BUTTON_PROXIMO_TEXT = "PRÓXIMO"
BUTTON_RESET_TEXT = "RESET"

## ARRAY SETTINGS
ARRAY_SIZE_DFT_RANGE = 5
ARRAY_SIZE_MIN_RANGE = 4
ARRAY_SIZE_MAX_RANGE = 10

ARRAY_VALUE_MIN_RANGE = 0
ARRAY_VALUE_MAX_RANGE = 100

COLOR_BORDER_ARRAY_DEFAULT = "#000000"  # Borda Preto - elementos do array
COLOR_FILL_ARRAY_DEFAULT = "#B0BEC5" # Cinza - elementos do array

# ALGORITHM SETTINGS

LINEAR_SEARCH_NAME = "Busca Linear"
BINARY_SEARCH_NAME = "Busca Binária"
ALGORITHM_SEARCH_ALG_LIST = [LINEAR_SEARCH_NAME, BINARY_SEARCH_NAME]

INSERTION_SORT_NAME = "Insertion Sort"
BUBBLE_SORT_NAME = "Bubble Sort"       
SELECTION_SORT_NAME = "Selection Sort" 
QUICK_SORT_NAME = "Quick Sort"
MERGE_SORT_NAME = "Merge Sort"

# Lista atualizada com todos os algoritmos
ALGORITHM_SORTING_ALG_LIST = [
    INSERTION_SORT_NAME, 
    BUBBLE_SORT_NAME, 
    SELECTION_SORT_NAME, 
    QUICK_SORT_NAME, 
    MERGE_SORT_NAME
]

# Search Algorithms
COLOR_FILL_ARRAY_UNVISITED = "#B0BEC5" # Cinza - estado padrão
COLOR_FILL_ARRAY_VISITED = "#FFEA00"    # Amarelo - estado visitado
COLOR_FILL_ARRAY_FOUND = "#00E229"   # Verde - elemento encontrado
COLOR_FILL_ARRAY_NOT_FOUND = "#FF0000" # Vermelho - elemento não encontrado

POINTER_LIN_FONT_SIZE = 14
POINTER_BIN_FONT_SIZE = 12

# Busca linear
COLOR_BORDER_POINTER_LINEAR_ITERATOR = "#182C4A"  # Borda Azul - ponteiro iterador (busca linear)
# Busca binária
COLOR_BORDER_POINTER_BINARY_MID = "#182C4A"      # Borda Azul Escuro - ponteiro meio (busca binária)
COLOR_BORDER_POINTER_BINARY_LEFT = "#FF3C00"     # Borda Laranja - ponteiro esquerdo (busca binária)
COLOR_BORDER_POINTER_BINARY_RIGHT = "#FFE600"    # Borda Amarelo - ponteiro direito (busca binária)

# Sorting Algorithms
# Insertion Sort
COLOR_BORDER_INSERTION_SORT_ITERATOR_I = "#FF3C00"  # Borda Laranja - ponteiro target_key_idx
COLOR_BORDER_INSERTION_SORT_ITERATOR_J = "#FF0000"  # Borda Vermelha - ponteiro curr_j
COLOR_FILL_INSERTION_SORT_SORTED = "#00E229"        # Verde - parte ordenada

# Bubble Sort
COLOR_BORDER_BUBBLE_SORT_POINTER_I = "#FF3C00"      # Borda Laranja - ponteiro i
COLOR_BORDER_BUBBLE_SORT_POINTER_J = "#FF0000"      # Borda Vermelha - ponteiro j
COLOR_FILL_BUBBLE_SORT_SORTED = "#00E229"           # Verde - parte ordenada

# Selection Sort
COLOR_BORDER_SELECTION_SORT_POINTER_I = "#FF3C00"       # Borda Laranja - ponteiro i
COLOR_BORDER_SELECTION_SORT_POINTER_J = "#FF0000"       # Borda Vermelha - ponteiro j
COLOR_BORDER_SELECTION_SORT_POINTER_MIN_IDX = "#0000FF" # Borda Azul - ponteiro min_idx
COLOR_FILL_SELECTION_SORT_SORTED = "#00E229"            # Verde - parte ordenada

# Quick Sort
COLOR_BORDER_QUICK_SORT_POINTER_LOW = "#FF3C00"   # Borda Laranja - ponteiro low
COLOR_BORDER_QUICK_SORT_POINTER_HIGH = "#FF0000"  # Borda Vermelha - ponteiro high
COLOR_BORDER_QUICK_SORT_PIVOT = "#0000FF"         # Borda Azul - pivô
COLOR_FILL_QUICK_SORT_SORTED = "#00E229"          # Verde - parte ordenada

# Merge Sort
COLOR_BORDER_MERGE_SORT_RANGE = "#0000FF"    # Borda Azul - intervalo sendo mesclado
COLOR_FILL_MERGE_SORT_ACTIVE = "#FFF59D"     # Amarelo Claro - área ativa
COLOR_FILL_MERGE_SORT_SORTED = "#00E229"     # Verde - parte ordenada

# QUIZ SETTINGS
QUIZ_MAX_QUESTIONS = 10
BUTTON_QUIZ_REINICIAR_QUIZ_TEXT = "REINICIAR QUIZ"
BUTTON_QUIZ_INICIAR_QUIZ_TEXT = "INICIAR QUIZ"
BUTTON_QUIZ_CONFIRMAR_RESPOSTA_TEXT = "CONFIRMAR RESPOSTA"
BUTTON_QUIZ_ANTERIOR_TEXT = "ANTERIOR"
BUTTON_QUIZ_PROXIMO_TEXT = "PRÓXIMO"
BUTTON_QUIZ_FINALIZAR_TEXT = "FINALIZAR"
