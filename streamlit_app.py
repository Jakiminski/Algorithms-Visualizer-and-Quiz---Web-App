import streamlit as st
import algorithms as alg
from config import *
from quiz import QuizEngine


class WebApp:
    """Classe principal para gerenciar a aplicação web Streamlit."""
    
    def __init__(self):
        """Inicializa a aplicação web com estado padrão."""
        self.init_session_state()
    
    @staticmethod
    def init_session_state():
        """Inicializa todas as variáveis de estado da sessão."""
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
        if "quiz_engine" not in st.session_state:
            st.session_state.quiz_engine = QuizEngine()

    @staticmethod
    def set_page(page_name):
        """Alterna para uma página diferente."""
        st.session_state.page = page_name
        st.session_state.trace = None
        st.session_state.step_index = 0
        st.rerun()

    @staticmethod
    def reset_quiz():
        """Reseta o estado do quiz para permitir novo jogo."""
        st.session_state.quiz_finished = False
        st.session_state.quiz_questions = []
        st.session_state.quiz_active = False
        st.session_state.quiz_current_index = 0
        st.session_state.quiz_answers = {}
        st.session_state.quiz_score_details = {}
        st.rerun()

    @staticmethod
    def render_quiz_visual(prob):
        """Renderiza a visualização do array para uma questão do quiz."""
        if "trace" not in prob or "step_to_show" not in prob:
            st.warning("Visualização não disponível.")
            return

        step_idx = prob["step_to_show"]
        trace = prob["trace"]
        algo_name = prob.get("algo", "")
        
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

    def render_search_page(self):
        """Renderiza a página de algoritmos de busca."""
        st.title("🔍 Algoritmos de Busca")
        
        if st.button(BUTTON_RETURN_TEXT):
            self.set_page(FRAME_MENU)

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
                bg = COLOR_FILL_ARRAY_UNVISITED
                border = COLOR_BORDER_ARRAY_DEFAULT
                b_width = "2px"

                if selecao == LINEAR_SEARCH_NAME:
                    if i == passo["idx"]:
                        border = COLOR_BORDER_POINTER_LINEAR_ITERATOR
                        b_width = "4px"
                        if passo["encontrado"]: bg = COLOR_FILL_ARRAY_FOUND
                    elif i < passo["idx"] and passo["idx"] != -1:
                        bg = COLOR_FILL_ARRAY_VISITED

                elif selecao == BINARY_SEARCH_NAME:
                    l, r, m = passo["l"], passo["r"], passo["m"]
                    if l <= i <= r and passo["m"] != -1:
                        bg = COLOR_FILL_ARRAY_VISITED
                    if i == m:
                        border = COLOR_BORDER_POINTER_BINARY_MID
                        b_width = "4px"
                        if passo["encontrado"]: bg = COLOR_FILL_ARRAY_FOUND
                    elif i == l:
                        border = COLOR_BORDER_POINTER_BINARY_LEFT
                        b_width = "4px"
                    elif i == r:
                        border = COLOR_BORDER_POINTER_BINARY_RIGHT
                        b_width = "4px"

                if passo["finalizado"] and not passo["encontrado"]:
                    bg = COLOR_FILL_ARRAY_NOT_FOUND

                cols[i].markdown(
                    f"""
                    <div style="background-color: {bg}; border: {b_width} solid {border}; padding: 10px 2px; text-align: center; border-radius: 5px; font-size: 14px; font-family: sans-serif; font-weight: bold; color: black; min-width: 30px;">
                        {val}
                    </div>
                    """, unsafe_allow_html=True
                )

            st.write("---")
            ctrl_col1, ctrl_col2, ctrl_col3, _ = st.columns([1, 1, 1, 4])
            with ctrl_col1:
                if st.button(BUTTON_ANTERIOR_TEXT, disabled=(st.session_state.step_index == 0), use_container_width=True, key="btn_prev_search"):
                    st.session_state.step_index -= 1
                    st.rerun()
            with ctrl_col2:
                if st.button(BUTTON_PROXIMO_TEXT, disabled=(st.session_state.step_index >= len(st.session_state.trace)-1), use_container_width=True, key="btn_next_search"):
                    st.session_state.step_index += 1
                    st.rerun()
            with ctrl_col3:
                if st.button(BUTTON_RESET_TEXT, use_container_width=True, key="btn_reset_search"):
                    st.session_state.step_index = 0
                    st.rerun()

    def render_sorting_page(self):
        """Renderiza a página de algoritmos de ordenação."""
        st.title("📊 Algoritmos de Ordenação")
        if st.button(BUTTON_RETURN_TEXT): 
            self.set_page(FRAME_MENU)
        
        with st.container(border=True):
            c1, c2, c3 = st.columns([2, 4, 1.5])
            with c1:
                selecao_sort = st.selectbox("Algoritmo", ALGORITHM_SORTING_ALG_LIST)
            with c2:
                entrada_sort = st.text_input("Vetor (Números separados por vírgula)", "40, 10, 30, 20, 50")
            with c3:
                st.write(" ")
                if st.button("ORDENAR", use_container_width=True):
                    raw_items = [x.strip() for x in entrada_sort.split(",") if x.strip()]
                    vetor = [alg.valid_input(i, min_range=1, max_range=100) for i in raw_items]
                     
                    if selecao_sort == INSERTION_SORT_NAME:
                        st.session_state.trace = alg.gen_insertion_sort(vetor)
                    elif selecao_sort == BUBBLE_SORT_NAME:
                        st.session_state.trace = alg.gen_bubble_sort(vetor)
                    elif selecao_sort == SELECTION_SORT_NAME:
                        st.session_state.trace = alg.gen_selection_sort(vetor)
                    elif selecao_sort == QUICK_SORT_NAME:
                        st.session_state.trace = alg.gen_quick_sort(vetor)
                    elif selecao_sort == MERGE_SORT_NAME:
                        st.session_state.trace = alg.gen_merge_sort(vetor)
                     
                    st.session_state.step_index = 0
                    st.rerun()

        if st.session_state.trace:
            passo = st.session_state.trace[st.session_state.step_index]
            if "desc" in passo:
                st.info(f"Passo {st.session_state.step_index + 1}/{len(st.session_state.trace)}: {passo['desc']}")
            else:
                st.info(f"Passo {st.session_state.step_index + 1}/{len(st.session_state.trace)}")

            n_elementos = len(passo["array"])
            cols = st.columns(n_elementos)
            
            for i, val in enumerate(passo["array"]):
                bg = COLOR_FILL_ARRAY_UNVISITED
                border = COLOR_BORDER_ARRAY_DEFAULT
                b_width = "2px"

                if passo["alg"] == "Insertion":
                    if i == passo["target_key_idx"]:
                        border = COLOR_BORDER_INSERTION_SORT_ITERATOR_I 
                        b_width = "4px"
                    if i == passo["curr_j"]:
                        border = COLOR_BORDER_INSERTION_SORT_ITERATOR_J
                        b_width = "4px"
                        bg = COLOR_FILL_ARRAY_VISITED

                elif passo["alg"] == "Bubble":
                    if passo["action"] != "start" and passo["action"] != "finished":
                        sorted_start_index = len(passo["array"]) - passo.get("i", 0)
                        if i >= sorted_start_index:
                            bg = COLOR_FILL_BUBBLE_SORT_SORTED
                    if i == passo.get("j") or i == passo.get("j_next"):
                        if passo["action"] == "swap": bg = COLOR_FILL_ARRAY_VISITED
                        if i == passo.get("j"): border = COLOR_BORDER_BUBBLE_SORT_POINTER_J
                        else: border = COLOR_BORDER_BUBBLE_SORT_POINTER_I
                        b_width = "3px"

                elif passo["alg"] == "Selection":
                    if i < passo.get("i", 0): bg = COLOR_FILL_SELECTION_SORT_SORTED
                    if i == passo.get("min_idx"):
                        border = COLOR_BORDER_SELECTION_SORT_POINTER_MIN_IDX
                        b_width = "4px"
                    elif i == passo.get("curr"):
                        border = COLOR_BORDER_SELECTION_SORT_POINTER_J
                        b_width = "3px"
                        bg = COLOR_FILL_ARRAY_VISITED

                elif passo["alg"] == "Quick":
                    low, high, pivot_idx = passo.get("low", -1), passo.get("high", -1), passo.get("pivot_idx", -1)
                    curr_i, curr_j = passo.get("i", -2), passo.get("curr", -2)
                    if low != -1 and high != -1 and low <= i <= high: bg = "#E3F2FD"
                    if i == pivot_idx and pivot_idx != -1:
                        border = COLOR_BORDER_QUICK_SORT_PIVOT
                        b_width = "4px"
                        bg = "#BBDEFB"
                    if i == curr_i:
                        border = COLOR_BORDER_QUICK_SORT_POINTER_LOW
                        b_width = "3px"
                    elif i == curr_j:
                        border = COLOR_BORDER_QUICK_SORT_POINTER_HIGH
                        b_width = "3px"
                
                elif passo["alg"] == "Merge":
                    l, r, k = passo.get("l", -1), passo.get("r", -1), passo.get("curr_k", -1)
                    if l != -1 and r != -1 and l <= i <= r:
                        bg = COLOR_FILL_MERGE_SORT_ACTIVE
                        border = COLOR_BORDER_MERGE_SORT_RANGE
                    if i == k:
                        border = "#000000"
                        b_width = "4px"
                        bg = COLOR_FILL_ARRAY_VISITED

                if passo.get("action") == "finished": bg = COLOR_FILL_ARRAY_FOUND

                cols[i].markdown(
                    f"""
                    <div style="background-color: {bg}; border: {b_width} solid {border}; padding: 10px 2px; text-align: center; border-radius: 5px; font-size: 14px; font-family: sans-serif; font-weight: bold; color: black; min-width: 30px;">
                        {val}
                    </div>
                    """, unsafe_allow_html=True
                )

            st.write("---")
            ctrl_col1, ctrl_col2, ctrl_col3, _ = st.columns([1, 1, 1, 4])
            with ctrl_col1:
                if st.button(BUTTON_ANTERIOR_TEXT, disabled=(st.session_state.step_index == 0), use_container_width=True, key="btn_prev_sort"):
                    st.session_state.step_index -= 1
                    st.rerun()
            with ctrl_col2:
                if st.button(BUTTON_PROXIMO_TEXT, disabled=(st.session_state.step_index >= len(st.session_state.trace)-1), use_container_width=True, key="btn_next_sort"):
                    st.session_state.step_index += 1
                    st.rerun()
            with ctrl_col3:
                if st.button(BUTTON_RESET_TEXT, use_container_width=True, key="btn_reset_sort"):
                    st.session_state.step_index = 0
                    st.rerun()

    def render_quiz_page(self):
        """Renderiza a página de quiz."""
        st.title("🧠 Quiz")
        if st.button(BUTTON_RETURN_TEXT): 
            self.set_page(FRAME_MENU)

        if st.session_state.quiz_finished:
            self._render_quiz_results()
        elif not st.session_state.quiz_active:
            self._render_quiz_setup()
        else:
            self._render_quiz_game()

    def _render_quiz_results(self):
        """Renderiza os resultados do quiz."""
        score = sum(1 for v in st.session_state.quiz_score_details.values() if v)
        total = len(st.session_state.quiz_questions)
        
        st.success(f"🎉 Quiz Finalizado! Sua pontuação: {score}/{total}")
        
        st.subheader("Detalhes das Respostas")
        for i, q in enumerate(st.session_state.quiz_questions):
            is_correct = st.session_state.quiz_score_details.get(i, False)
            icon = "✅" if is_correct else "❌"
            user_ans = st.session_state.quiz_answers.get(i, "N/A")
            correct_ans = q["correct_letter"]
            
            with st.expander(f"Questão {i+1} - {icon}"):
                st.write(f"**Pergunta:** {q['question']}")
                st.write(f"**Sua resposta:** {user_ans}")
                if not is_correct:
                    st.write(f"**Correta:** {correct_ans} ({q['choices'][correct_ans]})")
                
                self.render_quiz_visual(q)

        if st.button(BUTTON_QUIZ_REINICIAR_QUIZ_TEXT):
            self.reset_quiz()

    def _render_quiz_setup(self):
        """Renderiza a tela de configuração do quiz."""
        st.info("Escolha os assuntos do seu Quiz antes de começar.")
        
        opcoes_algoritmos = [
            LINEAR_SEARCH_NAME, 
            BINARY_SEARCH_NAME, 
            INSERTION_SORT_NAME
        ]
        
        selected = st.multiselect(
            "Escolha os assuntos:",
            opcoes_algoritmos,
            default=opcoes_algoritmos
        )
        
        col_start, _ = st.columns([1, 3])
        with col_start:
            if st.button(BUTTON_QUIZ_INICIAR_QUIZ_TEXT, use_container_width=True):
                if not selected:
                    st.warning("Selecione pelo menos um assunto!")
                else:
                    st.session_state.quiz_engine.set_topics(selected)
                    questions = []
                    with st.spinner("Gerando perguntas..."):
                        for _ in range(QUIZ_MAX_QUESTIONS):
                            questions.append(st.session_state.quiz_engine.generate_problem())
                    
                    st.session_state.quiz_questions = questions
                    st.session_state.quiz_active = True
                    st.session_state.quiz_current_index = 0
                    st.rerun()

    def _render_quiz_game(self):
        """Renderiza a tela de jogo do quiz."""
        current_idx = st.session_state.quiz_current_index
        total_q = len(st.session_state.quiz_questions)
        question_data = st.session_state.quiz_questions[current_idx]
        
        progress = (current_idx + 1) / total_q
        st.progress(progress, text=f"Questão {current_idx + 1} de {total_q}")
        
        st.markdown(f"### {question_data['question']}")
        
        with st.container(border=True):
            self.render_quiz_visual(question_data)

        choices = question_data["choices"]
        options_list = [f"{k}) {v}" for k, v in choices.items()]
        
        ja_respondeu = current_idx in st.session_state.quiz_answers
        
        radio_key = f"radio_q_{current_idx}"
        
        user_choice_full = st.radio(
            "Selecione a resposta:", 
            options_list, 
            key=radio_key,
            disabled=ja_respondeu
        )
        
        if ja_respondeu:
            user_letter = st.session_state.quiz_answers[current_idx]
            correct_letter = question_data["correct_letter"]
            if st.session_state.quiz_score_details[current_idx]:
                st.success(f"Correto! Resposta: {user_letter}")
            else:
                st.error(f"Incorreto. Você marcou {user_letter}, mas a correta era {correct_letter}.")

        st.write("---")
        
        c1, c2, c3 = st.columns([1, 1, 1])
        
        with c1:
            if not ja_respondeu:
                if st.button(BUTTON_QUIZ_CONFIRMAR_RESPOSTA_TEXT, use_container_width=True):
                    selected_letter = user_choice_full.split(")")[0]
                    st.session_state.quiz_answers[current_idx] = selected_letter
                    
                    is_correct = (selected_letter == question_data["correct_letter"])
                    st.session_state.quiz_score_details[current_idx] = is_correct
                    st.rerun()
            else:
                st.button(BUTTON_QUIZ_CONFIRMAR_RESPOSTA_TEXT, disabled=True, use_container_width=True)

        with c2:
            if st.button(BUTTON_QUIZ_ANTERIOR_TEXT, disabled=(current_idx == 0), use_container_width=True):
                st.session_state.quiz_current_index -= 1
                st.rerun()
        
        with c3:
            if current_idx == total_q - 1:
                if st.button(BUTTON_QUIZ_FINALIZAR_TEXT, disabled=not ja_respondeu, use_container_width=True):
                    st.session_state.quiz_finished = True
                    st.rerun()
            else:
                if st.button(BUTTON_QUIZ_PROXIMO_TEXT, use_container_width=True):
                    st.session_state.quiz_current_index += 1
                    st.rerun()

    def render(self):
        """Renderiza a página apropriada baseado no estado."""
        if st.session_state.page == FRAME_MENU:
            st.title(f"🚀 {APP_NAME}")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🔍 Algoritmos de Busca", use_container_width=True): 
                    self.set_page(FRAME_SEARCH_ALGORITHMS)
            with col2:
                if st.button("📊 Algoritmos de Ordenação", use_container_width=True): 
                    self.set_page(FRAME_SORTING_ALGORITHMS)
            with col3:
                if st.button("🧠 Quiz", use_container_width=True): 
                    self.set_page(FRAME_QUIZ)

        elif st.session_state.page == FRAME_SEARCH_ALGORITHMS:
            self.render_search_page()
        elif st.session_state.page == FRAME_SORTING_ALGORITHMS:
            self.render_sorting_page()
        elif st.session_state.page == FRAME_QUIZ:
            self.render_quiz_page()


# --- INICIALIZAÇÃO E EXECUÇÃO ---
app = WebApp()
app.render()
