import streamlit as st
import algorithms as alg
import config

# --- 1. INICIALIZAÇÃO DO ESTADO ---
if "page" not in st.session_state:
    st.session_state.page = config.FRAME_MENU

if "trace" not in st.session_state:
    st.session_state.trace = None

if "step_index" not in st.session_state:
    st.session_state.step_index = 0

def set_page(page_name):
    st.session_state.page = page_name
    st.session_state.trace = None
    st.session_state.step_index = 0
    st.rerun()

# --- 2. LÓGICA DE NAVEGAÇÃO ---

if st.session_state.page == config.FRAME_MENU:
    st.title(f"🚀 {config.APP_NAME}")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔍 Busca", use_container_width=True): set_page(config.FRAME_SEARCH_ALGORITHMS)
    with col2:
        if st.button("📊 Ordenação", use_container_width=True): set_page(config.FRAME_SORTING_ALGORITHMS)
    with col3:
        if st.button("🧠 Quiz", use_container_width=True): set_page(config.FRAME_QUIZ)

elif st.session_state.page == config.FRAME_SEARCH_ALGORITHMS:
    st.title("🔍 Algoritmos de Busca")
    
    if st.button(config.BUTTON_RETURN_TEXT):
        set_page(config.FRAME_MENU)

    # Painel de controle - Ajustado proporção das colunas para [2, 3, 1, 1.5]
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns([2, 3, 1, 1.5])
        with c1:
            selecao = st.selectbox("Algoritmo", config.ALGORITHM_SEARCH_ALG_LIST)
        with c2:
            entrada = st.text_input("Vetor (Números separados por vírgula)", "10, 25, 42, 55, 70, 88, 99")
        with c3:
            alvo = st.number_input("Alvo", value=55, min_value=1, max_value=100)
        with c4:
            st.write(" ")
            if st.button("EXECUTAR", use_container_width=True):
                raw_items = [x.strip() for x in entrada.split(",") if x.strip()]
                vetor = [alg.valid_input(i, min_range=1, max_range=100) for i in raw_items]
                
                if selecao == config.BINARY_SEARCH_NAME:
                    vetor.sort()
                    st.session_state.trace = alg.gen_binary_search(vetor, alvo)
                else:
                    st.session_state.trace = alg.gen_linear_search(vetor, alvo)
                
                st.session_state.step_index = 0
                st.rerun()

    # --- 3. RENDERIZAÇÃO DO VETOR (BUSCA) ---
    if st.session_state.trace:
        passo = st.session_state.trace[st.session_state.step_index]
        st.subheader(f"Comparações: {passo.get('comparações', 0)}")

        n_elementos = len(passo["array"])
        cols = st.columns(n_elementos)
        
        for i, val in enumerate(passo["array"]):
            bg = config.COLOR_FILL_ARRAY_UNVISITED
            border = config.COLOR_BORDER_ARRAY_DEFAULT
            b_width = "2px"

            if selecao == config.LINEAR_SEARCH_NAME:
                if i == passo["idx"]:
                    border = config.COLOR_BORDER_POINTER_LINEAR_ITERATOR
                    b_width = "4px"
                    if passo["encontrado"]: bg = config.COLOR_FILL_ARRAY_FOUND
                elif i < passo["idx"] and passo["idx"] != -1:
                    bg = config.COLOR_FILL_ARRAY_VISITED

            elif selecao == config.BINARY_SEARCH_NAME:
                l, r, m = passo["l"], passo["r"], passo["m"]
                if l <= i <= r and passo["m"] != -1:
                    bg = config.COLOR_FILL_ARRAY_VISITED
                if i == m:
                    border = config.COLOR_BORDER_POINTER_BINARY_MID
                    b_width = "4px"
                    if passo["encontrado"]: bg = config.COLOR_FILL_ARRAY_FOUND
                elif i == l:
                    border = config.COLOR_BORDER_POINTER_BINARY_LEFT
                    b_width = "4px"
                elif i == r:
                    border = config.COLOR_BORDER_POINTER_BINARY_RIGHT
                    b_width = "4px"

            if passo["finalizado"] and not passo["encontrado"]:
                bg = config.COLOR_FILL_ARRAY_NOT_FOUND

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
            if st.button(config.BUTTON_ANTERIOR_TEXT, disabled=(st.session_state.step_index == 0), use_container_width=True, key="btn_prev_search"):
                st.session_state.step_index -= 1
                st.rerun()
        with ctrl_col2:
            if st.button(config.BUTTON_PROXIMO_TEXT, disabled=(st.session_state.step_index >= len(st.session_state.trace)-1), use_container_width=True, key="btn_next_search"):
                st.session_state.step_index += 1
                st.rerun()
        with ctrl_col3:
            if st.button(config.BUTTON_RESET_TEXT, use_container_width=True, key="btn_reset_search"):
                st.session_state.step_index = 0
                st.rerun()

elif st.session_state.page == config.FRAME_SORTING_ALGORITHMS:
    st.title("📊 Algoritmos de Ordenação")
    if st.button(config.BUTTON_RETURN_TEXT): set_page(config.FRAME_MENU)
    
    # Painel de Controle de Ordenação
    with st.container(border=True):
        c1, c2, c3 = st.columns([2, 4, 1.5])
        with c1:
            selecao_sort = st.selectbox("Algoritmo", config.ALGORITHM_SORTING_ALG_LIST)
        with c2:
            entrada_sort = st.text_input("Vetor (Números separados por vírgula)", "40, 10, 30, 20, 50")
        with c3:
            st.write(" ")
            if st.button("ORDENAR", use_container_width=True):
                raw_items = [x.strip() for x in entrada_sort.split(",") if x.strip()]
                vetor = [alg.valid_input(i, min_range=1, max_range=100) for i in raw_items]
                 
                if selecao_sort == config.INSERTION_SORT_NAME:
                    st.session_state.trace = alg.gen_insertion_sort(vetor)
                elif selecao_sort == config.BUBBLE_SORT_NAME:
                    st.session_state.trace = alg.gen_bubble_sort(vetor)
                elif selecao_sort == config.SELECTION_SORT_NAME:
                    st.session_state.trace = alg.gen_selection_sort(vetor)
                elif selecao_sort == config.QUICK_SORT_NAME:
                    st.session_state.trace = alg.gen_quick_sort(vetor)
                elif selecao_sort == config.MERGE_SORT_NAME:
                    st.session_state.trace = alg.gen_merge_sort(vetor)
                 
                st.session_state.step_index = 0
                st.rerun()

    # Visualização da Ordenação
    if st.session_state.trace:
        passo = st.session_state.trace[st.session_state.step_index]
        if "desc" in passo:
            st.info(f"Passo {st.session_state.step_index + 1}/{len(st.session_state.trace)}: {passo['desc']}")
        else:
            st.info(f"Passo {st.session_state.step_index + 1}/{len(st.session_state.trace)}")

        n_elementos = len(passo["array"])
        cols = st.columns(n_elementos)
        
        for i, val in enumerate(passo["array"]):
            bg = config.COLOR_FILL_ARRAY_UNVISITED
            border = config.COLOR_BORDER_ARRAY_DEFAULT
            b_width = "2px"

            if passo["alg"] == "Insertion":
                if i == passo["target_key_idx"]:
                    border = config.COLOR_BORDER_INSERTION_SORT_ITERATOR_I 
                    b_width = "4px"
                if i == passo["curr_j"]:
                    border = config.COLOR_BORDER_INSERTION_SORT_ITERATOR_J
                    b_width = "4px"
                    bg = config.COLOR_FILL_ARRAY_VISITED

            elif passo["alg"] == "Bubble":
                if passo["action"] != "start" and passo["action"] != "finished":
                    sorted_start_index = len(passo["array"]) - passo.get("i", 0)
                    if i >= sorted_start_index:
                        bg = config.COLOR_FILL_BUBBLE_SORT_SORTED
                if i == passo.get("j") or i == passo.get("j_next"):
                    if passo["action"] == "swap": bg = config.COLOR_FILL_ARRAY_VISITED
                    if i == passo.get("j"): border = config.COLOR_BORDER_BUBBLE_SORT_POINTER_J
                    else: border = config.COLOR_BORDER_BUBBLE_SORT_POINTER_I
                    b_width = "3px"

            elif passo["alg"] == "Selection":
                if i < passo.get("i", 0): bg = config.COLOR_FILL_SELECTION_SORT_SORTED
                if i == passo.get("min_idx"):
                    border = config.COLOR_BORDER_SELECTION_SORT_POINTER_MIN_IDX
                    b_width = "4px"
                elif i == passo.get("curr"):
                    border = config.COLOR_BORDER_SELECTION_SORT_POINTER_J
                    b_width = "3px"
                    bg = config.COLOR_FILL_ARRAY_VISITED

            elif passo["alg"] == "Quick":
                low, high, pivot_idx = passo.get("low", -1), passo.get("high", -1), passo.get("pivot_idx", -1)
                curr_i, curr_j = passo.get("i", -2), passo.get("curr", -2)
                if low != -1 and high != -1 and low <= i <= high: bg = "#E3F2FD"
                if i == pivot_idx and pivot_idx != -1:
                    border = config.COLOR_BORDER_QUICK_SORT_PIVOT
                    b_width = "4px"
                    bg = "#BBDEFB"
                if i == curr_i:
                    border = config.COLOR_BORDER_QUICK_SORT_POINTER_LOW
                    b_width = "3px"
                elif i == curr_j:
                    border = config.COLOR_BORDER_QUICK_SORT_POINTER_HIGH
                    b_width = "3px"
            
            elif passo["alg"] == "Merge":
                l, r, k = passo.get("l", -1), passo.get("r", -1), passo.get("curr_k", -1)
                if l != -1 and r != -1 and l <= i <= r:
                    bg = config.COLOR_FILL_MERGE_SORT_ACTIVE
                    border = config.COLOR_BORDER_MERGE_SORT_RANGE
                if i == k:
                    border = "#000000"
                    b_width = "4px"
                    bg = config.COLOR_FILL_ARRAY_VISITED

            if passo.get("action") == "finished": bg = config.COLOR_FILL_ARRAY_FOUND

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
            if st.button(config.BUTTON_ANTERIOR_TEXT, disabled=(st.session_state.step_index == 0), use_container_width=True, key="btn_prev_sort"):
                st.session_state.step_index -= 1
                st.rerun()
        with ctrl_col2:
            if st.button(config.BUTTON_PROXIMO_TEXT, disabled=(st.session_state.step_index >= len(st.session_state.trace)-1), use_container_width=True, key="btn_next_sort"):
                st.session_state.step_index += 1
                st.rerun()
        with ctrl_col3:
            if st.button(config.BUTTON_RESET_TEXT, use_container_width=True, key="btn_reset_sort"):
                st.session_state.step_index = 0
                st.rerun()

elif st.session_state.page == config.FRAME_QUIZ:
    st.title("🧠 Quiz de Algoritmos")
    if st.button(config.BUTTON_RETURN_TEXT): set_page(config.FRAME_MENU)
    
    st.write("Analise o estado do vetor abaixo e responda à pergunta:")
    
    # Exemplo de renderização de vetor no Quiz com cores corrigidas
    exemplo_vetor = [15, 30, 45, 60, 75]
    cols = st.columns(len(exemplo_vetor))
    
    for i, val in enumerate(exemplo_vetor):
        # Usando cinza padrão com números em PRETO para legibilidade
        bg = config.COLOR_FILL_ARRAY_DEFAULT
        border = config.COLOR_BORDER_ARRAY_DEFAULT
        
        cols[i].markdown(
            f"""
            <div style="
                background-color: {bg}; 
                border: 2px solid {border}; 
                padding: 10px 2px; 
                text-align: center; 
                border-radius: 5px; 
                font-size: 16px; 
                font-family: sans-serif; 
                font-weight: bold; 
                color: black; 
                min-width: 40px;
            ">
                {val}
            </div>
            """, unsafe_allow_html=True
        )
    
    st.write("---")
    st.info("O Quiz está sendo preparado com base nos rastros de execução.")