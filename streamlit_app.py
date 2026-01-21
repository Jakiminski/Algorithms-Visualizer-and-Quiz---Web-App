import streamlit as st
import algorithms as alg
from config import *
#from quiz import QuizEngine

# Tentativa de importação da QuizEngine com tratamento de erro
try:
    from quiz import QuizEngine
except ImportError:
    QuizEngine = None
    
# --- 1. INICIALIZAÇÃO DO ESTADO ---
# --- 1. INICIALIZAÇÃO DO ESTADO ---
def init_session_state():
    if "page" not in st.session_state:
        st.session_state.page = FRAME_MENU
    if "trace" not in st.session_state:
        st.session_state.trace = None
    if "step_index" not in st.session_state:
        st.session_state.step_index = 0
    if "quiz_finished" not in st.session_state:
        st.session_state.quiz_finished = False
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []
    if "quiz_active" not in st.session_state:
        st.session_state.quiz_active = False
    if "quiz_current_index" not in st.session_state:
        st.session_state.quiz_current_index = 0
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    if "quiz_score_details" not in st.session_state:
        st.session_state.quiz_score_details = {}
    
    # Inicializa engine apenas uma vez
    if "quiz_engine" not in st.session_state and QuizEngine is not None:
        st.session_state.quiz_engine = QuizEngine()

init_session_state()

# --- FUNÇÕES AUXILIARES ---

def set_page(page_name):
    st.session_state.page = page_name
    st.session_state.trace = None
    st.session_state.step_index = 0
    st.rerun()

def reset_quiz():
    """Reseta o estado do quiz para permitir novo jogo."""
    st.session_state.quiz_finished = False
    st.session_state.quiz_questions = []
    st.session_state.quiz_active = False
    st.session_state.quiz_current_index = 0
    st.session_state.quiz_answers = {}
    st.session_state.quiz_score_details = {}
    st.rerun()


def render_quiz_visual(prob):
    """Renderiza a visualização do array para uma questão do quiz."""
    if not prob or "trace" not in prob or "step_to_show" not in prob:
        st.warning("Visualização não disponível para esta questão.")
        return

    step_idx = prob["step_to_show"]
    trace = prob["trace"]
    algo_name = prob.get("algo", "")
    
    if not trace: return
    
    if step_idx >= len(trace):
        step_idx = len(trace) - 1
        
    passo = trace[step_idx]
    
    if "array" in passo:
        n_elementos = len(passo["array"])
        cols = st.columns(n_elementos)
        
        for i, val in enumerate(passo["array"]):
            bg = COLOR_FILL_ARRAY_UNVISITED
            border = COLOR_BORDER_ARRAY_DEFAULT
            b_width = "2px"

            # Lógica de cores baseada no algoritmo do problema do quiz
            if algo_name == LINEAR_SEARCH_NAME:
                if i == passo.get("idx"):
                    border = COLOR_BORDER_POINTER_LINEAR_ITERATOR
                    b_width = "4px"
                    if passo.get("encontrado"): bg = COLOR_FILL_ARRAY_FOUND
                elif i < passo.get("idx", -1):
                    bg = COLOR_FILL_ARRAY_VISITED

            elif algo_name == BINARY_SEARCH_NAME:
                l, r, m = passo.get("l", -1), passo.get("r", -1), passo.get("m", -1)
                if l != -1 and r != -1 and l <= i <= r:
                    bg = COLOR_FILL_ARRAY_VISITED
                if i == m:
                    border = COLOR_BORDER_POINTER_BINARY_MID
                    b_width = "4px"
                    if passo.get("encontrado"): bg = COLOR_FILL_ARRAY_FOUND
                elif i == l:
                    border = COLOR_BORDER_POINTER_BINARY_LEFT
                elif i == r:
                    border = COLOR_BORDER_POINTER_BINARY_RIGHT

            elif algo_name == INSERTION_SORT_NAME:
                if i == passo.get("target_key_idx"):
                    border = COLOR_BORDER_INSERTION_SORT_ITERATOR_I
                    b_width = "4px"
                if i == passo.get("curr_j"):
                    border = COLOR_BORDER_INSERTION_SORT_ITERATOR_J
                    b_width = "4px"
                    bg = COLOR_FILL_ARRAY_VISITED

            cols[i].markdown(
                f"""
                <div style="background-color: {bg}; border: {b_width} solid {border}; padding: 10px 2px; text-align: center; border-radius: 5px; font-size: 14px; font-family: sans-serif; font-weight: bold; color: black; min-width: 30px;">
                    {val}
                </div>
                """, unsafe_allow_html=True
            )

# --- 2. LÓGICA DE NAVEGAÇÃO ---

if st.session_state.page == FRAME_MENU:
    st.title(f"🚀 {APP_NAME}")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔍 Busca", use_container_width=True): set_page(FRAME_SEARCH_ALGORITHMS)
    with col2:
        if st.button("📊 Ordenação", use_container_width=True): set_page(FRAME_SORTING_ALGORITHMS)
    with col3:
        if st.button("🧠 Quiz", use_container_width=True): set_page(FRAME_QUIZ)

elif st.session_state.page == FRAME_SEARCH_ALGORITHMS:
    st.title("🔍 Algoritmos de Busca")
    if st.button(BUTTON_RETURN_TEXT): set_page(FRAME_MENU)

    with st.container(border=True):
        c1, c2, c3, c4 = st.columns([2, 3, 1, 1.5])
        with c1:
            selecao = st.selectbox("Algoritmo", ALGORITHM_SEARCH_ALG_LIST)
        with c2:
            entrada = st.text_input("Vetor (Números separados por vírgula)", "10, 25, 42, 55, 70, 88, 99")
        with c3:
            alvo = st.number_input("Alvo", value=55, min_value=1, max_value=100)
        with c4:
            st.write(" ")
            if st.button("EXECUTAR", use_container_width=True):
                raw_items = [x.strip() for x in entrada.split(",") if x.strip()]
                vetor = [alg.valid_input(i, min_range=1, max_range=100) for i in raw_items]
                if selecao == BINARY_SEARCH_NAME:
                    vetor.sort()
                    st.session_state.trace = alg.gen_binary_search(vetor, alvo)
                else:
                    st.session_state.trace = alg.gen_linear_search(vetor, alvo)
                st.session_state.step_index = 0
                st.rerun()

    if st.session_state.trace:
        passo = st.session_state.trace[st.session_state.step_index]
        st.subheader(f"Comparações: {passo.get('comparações', 0)}")
        n_elementos = len(passo["array"])
        cols = st.columns(n_elementos)
        for i, val in enumerate(passo["array"]):
            bg, border, b_width = COLOR_FILL_ARRAY_UNVISITED, COLOR_BORDER_ARRAY_DEFAULT, "2px"
            if selecao == LINEAR_SEARCH_NAME:
                if i == passo["idx"]:
                    border, b_width = COLOR_BORDER_POINTER_LINEAR_ITERATOR, "4px"
                    if passo["encontrado"]: bg = COLOR_FILL_ARRAY_FOUND
                elif i < passo["idx"] and passo["idx"] != -1: bg = COLOR_FILL_ARRAY_VISITED
            elif selecao == BINARY_SEARCH_NAME:
                l, r, m = passo["l"], passo["r"], passo["m"]
                if l <= i <= r and passo["m"] != -1: bg = COLOR_FILL_ARRAY_VISITED
                if i == m:
                    border, b_width = COLOR_BORDER_POINTER_BINARY_MID, "4px"
                    if passo["encontrado"]: bg = COLOR_FILL_ARRAY_FOUND
                elif i == l: border, b_width = COLOR_BORDER_POINTER_BINARY_LEFT, "4px"
                elif i == r: border, b_width = COLOR_BORDER_POINTER_BINARY_RIGHT, "4px"
            if passo["finalizado"] and not passo["encontrado"]: bg = COLOR_FILL_ARRAY_NOT_FOUND
            cols[i].markdown(f'<div style="background-color: {bg}; border: {b_width} solid {border}; padding: 10px 2px; text-align: center; border-radius: 5px; font-size: 14px; font-weight: bold; color: black;">{val}</div>', unsafe_allow_html=True)
        
        st.write("---")
        ctrl1, ctrl2, ctrl3, _ = st.columns([1, 1, 1, 4])
        with ctrl1:
            if st.button(BUTTON_ANTERIOR_TEXT, disabled=(st.session_state.step_index == 0), key="s_prev"):
                st.session_state.step_index -= 1
                st.rerun()
        with ctrl2:
            if st.button(BUTTON_PROXIMO_TEXT, disabled=(st.session_state.step_index >= len(st.session_state.trace)-1), key="s_next"):
                st.session_state.step_index += 1
                st.rerun()
        with ctrl3:
            if st.button(BUTTON_RESET_TEXT, key="s_reset"):
                st.session_state.step_index = 0
                st.rerun()

elif st.session_state.page == FRAME_SORTING_ALGORITHMS:
    st.title("📊 Algoritmos de Ordenação")
    if st.button(BUTTON_RETURN_TEXT): set_page(FRAME_MENU)
    
    with st.container(border=True):
        c1, c2, c3 = st.columns([2, 4, 1.5])
        with c1: selecao_sort = st.selectbox("Algoritmo", ALGORITHM_SORTING_ALG_LIST)
        with c2: entrada_sort = st.text_input("Vetor", "40, 10, 30, 20, 50")
        with c3:
            st.write(" ")
            if st.button("ORDENAR", use_container_width=True):
                raw = [x.strip() for x in entrada_sort.split(",") if x.strip()]
                vetor = [alg.valid_input(i) for i in raw]
                if selecao_sort == INSERTION_SORT_NAME: st.session_state.trace = alg.gen_insertion_sort(vetor)
                elif selecao_sort == BUBBLE_SORT_NAME: st.session_state.trace = alg.gen_bubble_sort(vetor)
                elif selecao_sort == SELECTION_SORT_NAME: st.session_state.trace = alg.gen_selection_sort(vetor)
                elif selecao_sort == QUICK_SORT_NAME: st.session_state.trace = alg.gen_quick_sort(vetor)
                elif selecao_sort == MERGE_SORT_NAME: st.session_state.trace = alg.gen_merge_sort(vetor)
                st.session_state.step_index = 0
                st.rerun()

    if st.session_state.trace:
        passo = st.session_state.trace[st.session_state.step_index]
        st.info(f"Passo {st.session_state.step_index + 1}/{len(st.session_state.trace)}: {passo.get('desc', '')}")
        n_elementos = len(passo["array"])
        cols = st.columns(n_elementos)
        for i, val in enumerate(passo["array"]):
            bg, border, b_width = COLOR_FILL_ARRAY_UNVISITED, COLOR_BORDER_ARRAY_DEFAULT, "2px"
            if passo.get("action") == "finished": bg = COLOR_FILL_ARRAY_FOUND
            cols[i].markdown(f'<div style="background-color: {bg}; border: {b_width} solid {border}; padding: 10px 2px; text-align: center; border-radius: 5px; font-weight: bold; color: black;">{val}</div>', unsafe_allow_html=True)

elif st.session_state.page == FRAME_QUIZ:
    st.title("🧠 Quiz de Algoritmos")
    if st.button(BUTTON_RETURN_TEXT): set_page(FRAME_MENU)

    if QuizEngine is None:
        st.error("Erro: arquivo quiz.py não pôde ser carregado.")
    
    # 1. TELA DE RESULTADOS
    elif st.session_state.quiz_finished:
        score = sum(1 for v in st.session_state.quiz_score_details.values() if v)
        total = len(st.session_state.quiz_questions)
        st.success(f"🎉 Pontuação: {score}/{total}")
        txt_reiniciar = globals().get("BUTTON_QUIZ_REINICIAR_QUIZ_TEXT", "REINICIAR QUIZ")
        if st.button(txt_reiniciar): reset_quiz()

    # 2. TELA DE CONFIGURAÇÃO
    elif not st.session_state.quiz_active:
        st.markdown("#### Configure o seu Quiz")
        opcoes = [LINEAR_SEARCH_NAME, BINARY_SEARCH_NAME, INSERTION_SORT_NAME]
        selected = st.multiselect("Tópicos:", opcoes, default=opcoes)
        
        # Fallback de texto caso a constante do config.py falhe no servidor
        txt_iniciar = globals().get("BUTTON_QUIZ_INICIAR_QUIZ_TEXT", "INICIAR QUIZ")
        
        st.write("") # Espaçador
        
        # Botão em destaque
        if st.button(txt_iniciar, use_container_width=True, type="primary"):
            if not selected:
                st.warning("Selecione pelo menos um tópico.")
            else:
                try:
                    st.session_state.quiz_engine.set_topics(selected)
                    with st.spinner("Gerando questões..."):
                        # Gerando questões de forma segura
                        limit = globals().get("QUIZ_MAX_QUESTIONS", 5)
                        st.session_state.quiz_questions = [st.session_state.quiz_engine.generate_problem() for _ in range(limit)]
                    
                    st.session_state.quiz_active = True
                    st.session_state.quiz_current_index = 0
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao gerar o quiz: {e}")

    # 3. TELA DE JOGO
    else:
        idx = st.session_state.quiz_current_index
        q = st.session_state.quiz_questions[idx]
        
        st.progress((idx + 1) / len(st.session_state.quiz_questions))
        st.markdown(f"**Questão {idx+1}:** {q['question']}")
        
        render_quiz_visual(q)
        
        respondeu = idx in st.session_state.quiz_answers
        opcoes_lista = [f"{k}) {v}" for k, v in q["choices"].items()]
        
        escolha = st.radio("Sua resposta:", opcoes_lista, disabled=respondeu, key=f"q_{idx}")
        
        st.write("---")
        col_c, col_a, col_p = st.columns(3)
        
        with col_c:
            txt_conf = globals().get("BUTTON_QUIZ_CONFIRMAR_RESPOSTA_TEXT", "CONFIRMAR")
            if not respondeu:
                if st.button(txt_conf, use_container_width=True):
                    letra = escolha.split(")")[0]
                    st.session_state.quiz_answers[idx] = letra
                    st.session_state.quiz_score_details[idx] = (letra == q["correct_letter"])
                    st.rerun()
            else:
                st.button(txt_conf, disabled=True, use_container_width=True)
                
        with col_a:
            txt_ant = globals().get("BUTTON_QUIZ_ANTERIOR_TEXT", "ANTERIOR")
            if st.button(txt_ant, disabled=(idx == 0), use_container_width=True):
                st.session_state.quiz_current_index -= 1
                st.rerun()
                
        with col_p:
            if idx == len(st.session_state.quiz_questions) - 1:
                txt_fin = globals().get("BUTTON_QUIZ_FINALIZAR_TEXT", "FINALIZAR")
                if st.button(txt_fin, disabled=not respondeu, use_container_width=True):
                    st.session_state.quiz_finished = True
                    st.rerun()
            else:
                txt_prox = globals().get("BUTTON_QUIZ_PROXIMO_TEXT", "PRÓXIMO")
                if st.button(txt_prox, use_container_width=True):
                    st.session_state.quiz_current_index += 1
                    st.rerun()
