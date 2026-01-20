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

## UI Style 
DFT_STYLE = "flatly"

## Font Settings
DFT_FONT_NAME = "Helvetica"
DFT_FONT_SIZE = 12
DFT_FONT_COLOR = "black"

TITLE_FONT_NAME = "Helvetica"
TITLE_FONT_SIZE = 16
TITLE_FONT_COLOR = "black"

## Menu Buttons

BUTTON_RETURN_TEXT = "VOLTAR"

BUTTON_EXIT_TEXT = "SAIR"

BUTTON_APLICAR_SETUP_ALG = "APLICAR SETUP"
BUTTON_ANTERIOR_TEXT = "<< ANTERIOR"
BUTTON_PROXIMO_TEXT = "PRÓXIMO >>"
BUTTON_RESET_TEXT = "RESET"

## ARRAY SETTINGS
ARRAY_SIZE_DFT_RANGE = 5
ARRAY_SIZE_MIN_RANGE = 4
ARRAY_SIZE_MAX_RANGE = 10

ARRAY_VALUE_MIN_RANGE = 0
ARRAY_VALUE_MAX_RANGE = 100

ARRAY_ELEMENT_FONT_NAME = "Arial"
ARRAY_ELEMENT_FONT_SIZE = 10

COLOR_BORDER_ARRAY_DEFAULT = "#000000"  # Borda Preto - elementos do array
COLOR_FILL_ARRAY_DEFAULT = "#B0BEC5" # Cinza - elementos do array
COLOR_FILL_ARRAY_UNVISITED = "#B0BEC5" # Cinza - estado padrão
COLOR_FILL_ARRAY_VISITED = "#FFEA00"    # Amarelo - estado visitado

# ALGORITHM SETTINGS

LINEAR_SEARCH_NAME = "Busca Linear"
BINARY_SEARCH_NAME = "Busca Binária"
ALGORITHM_SEARCH_ALG_LIST = [LINEAR_SEARCH_NAME, BINARY_SEARCH_NAME]

INSERTION_SORT_NAME = "Insertion Sort"
BUBBLE_SORT_NAME = "Bubble Sort"       # Placeholder
SELECTION_SORT_NAME = "Selection Sort" # Placeholder
ALGORITHM_SORTING_ALG_LIST = [INSERTION_SORT_NAME, BUBBLE_SORT_NAME, SELECTION_SORT_NAME]

# Search Algorithms
COLOR_FILL_ARRAY_FOUND = "#00E229"   # Verde - elemento encontrado
COLOR_FILL_ARRAY_NOT_FOUND = "#FF0000" # Vermelho - elemento não encontrado

POINTER_FONT_NAME = "Arial"
POINTER_LIN_FONT_SIZE = 14
POINTER_BIN_FONT_SIZE = 12
POINTER_LIN_FONT = (POINTER_FONT_NAME, POINTER_LIN_FONT_SIZE, "bold")
POINTER_BIN_FONT = (POINTER_FONT_NAME, POINTER_BIN_FONT_SIZE, "bold")

COLOR_BORDER_POINTER_LINEAR_ITERATOR = "#182C4A"  # Borda Azul - ponteiro iterador (busca linear)
COLOR_BORDER_POINTER_BINARY_MID = "#182C4A"      # Borda Azul Escuro - ponteiro meio
COLOR_BORDER_POINTER_BINARY_LEFT = "#FF3C00"     # Borda Laranja - ponteiro esquerdo
COLOR_BORDER_POINTER_BINARY_RIGHT = "#FFE600"    # Borda Amarelo - ponteiro direito

# Sorting Algorithms
COLOR_BORDER_INSERTION_SORT_ITERATOR = "#FF3C00"  # Borda Laranja - ponteiro iterador (insertion sort)
# QUIZ SETTINGS
QUIZ_MAX_QUESTIONS = 10
