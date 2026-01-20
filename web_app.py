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

    # Painel de controle ajustado para inputs de 1 a 100
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns([2, 3, 1, 1])
        with c1:
            selecao = st.selectbox("Algoritmo", config.ALGORITHM_SEARCH_ALG_LIST)
        with c2:
            entrada = st.text_input("Vetor (Números entre 1 e 100 separados por vírgula)", "10, 25, 42, 55, 70, 88, 99")
        with c3:
            alvo = st.number_input("Alvo", value=55, min_value=1, max_value=100)
        with c4:
            st.write(" ")
            if st.button("EXECUTAR", use_container_width=True):
                # CORREÇÃO: Filtramos espaços e forçamos o range 1-100 na validação
                raw_items = [x.strip() for x in entrada.split(",") if x.strip()]
                # Chamamos valid_input garantindo que valores > 10 não virem 0
                vetor = [alg.valid_input(i, min_range=1, max_range=100) for i in raw_items]
                
                if selecao == config.BINARY_SEARCH_NAME:
                    vetor.sort()
                    st.session_state.trace = alg.gen_binary_search(vetor, alvo)
                else:
                    st.session_state.trace = alg.gen_linear_search(vetor, alvo)
                
                st.session_state.step_index = 0
                st.rerun()

    # --- 3. RENDERIZAÇÃO DO VETOR ---
    if st.session_state.trace:
        passo = st.session_state.trace[st.session_state.step_index]
        
        st.subheader(f"Comparações: {passo['comparações']}")

        # Ajuste de layout: se o vetor for grande, as colunas ficam muito estreitas.
        # Criamos colunas dinâmicas para os elementos.
        n_elementos = len(passo["array"])
        cols = st.columns(n_elementos)
        
        for i, val in enumerate(passo["array"]):
            bg = config.COLOR_FILL_ARRAY_UNVISITED
            border = config.COLOR_BORDER_ARRAY_DEFAULT
            b_width = "2px"

            # Lógica de Cores para Busca Linear
            if selecao == config.LINEAR_SEARCH_NAME:
                if i == passo["idx"]:
                    border = config.COLOR_BORDER_POINTER_LINEAR_ITERATOR
                    b_width = "4px"
                    if passo["encontrado"]: bg = config.COLOR_FILL_ARRAY_FOUND
                elif i < passo["idx"] and passo["idx"] != -1:
                    bg = config.COLOR_FILL_ARRAY_VISITED

            # Lógica de Cores para Busca Binária
            elif selecao == config.BINARY_SEARCH_NAME:
                l, r, m = passo["l"], passo["r"], passo["m"]
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
                
                if l <= i <= r and i != m:
                    bg = config.COLOR_FILL_ARRAY_VISITED

            if passo["finalizado"] and not passo["encontrado"]:
                bg = config.COLOR_FILL_ARRAY_NOT_FOUND

            # Renderização com CSS para garantir que o número caiba e o box seja proporcional
            cols[i].markdown(
                f"""
                <div style="
                    background-color: {bg};
                    border: {b_width} solid {border};
                    padding: 10px 2px;
                    text-align: center;
                    border-radius: 5px;
                    font-size: 14px;
                    font-family: sans-serif;
                    font-weight: bold;
                    color: black;
                    min-width: 30px;
                ">
                    {val}
                </div>
                """, unsafe_allow_html=True
            )

        # --- 4. CONTROLES ---
        st.write("---")
        ctrl_col1, ctrl_col2, ctrl_col3, _ = st.columns([1, 1, 1, 4])
        with ctrl_col1:
            if st.button(config.BUTTON_ANTERIOR_TEXT, disabled=(st.session_state.step_index == 0), use_container_width=True):
                st.session_state.step_index -= 1
                st.rerun()
        with ctrl_col2:
            if st.button(config.BUTTON_PROXIMO_TEXT, disabled=(st.session_state.step_index >= len(st.session_state.trace)-1), use_container_width=True):
                st.session_state.step_index += 1
                st.rerun()
        with ctrl_col3:
            if st.button(config.BUTTON_RESET_TEXT, use_container_width=True):
                st.session_state.step_index = 0
                st.rerun()

elif st.session_state.page == config.FRAME_SORTING_ALGORITHMS:
    st.title("📊 Algoritmos de Ordenação")
    if st.button(config.BUTTON_RETURN_TEXT): set_page(config.FRAME_MENU)
    st.info("Módulo de Insertion Sort.")

elif st.session_state.page == config.FRAME_QUIZ:
    st.title("🧠 Quiz")
    if st.button(config.BUTTON_RETURN_TEXT): set_page(config.FRAME_MENU)
    st.info("Módulo de perguntas e respostas.")