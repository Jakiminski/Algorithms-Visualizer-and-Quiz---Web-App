import random
import algorithms as alg
from config import *

class QuizEngine:
    def __init__(self):
        # Mapeamento de algoritmos para tópicos internos
        self.algo_topic_map = {
            LINEAR_SEARCH_NAME: ["busca_linear_contagem", "busca_linear_prox_comp"],
            BINARY_SEARCH_NAME: ["busca_binaria_indice", "busca_binaria_prox_comp"],
            INSERTION_SORT_NAME: ["insertion_sort_pivo", "insertion_sort_prox_comp"]
        }
        # Tópicos ativos (padrão: todos)
        self.active_topics = []
        for topics in self.algo_topic_map.values():
            self.active_topics.extend(topics)

    def set_topics(self, selected_algos):
        """Configura os tópicos com base nos algoritmos selecionados pelo usuário."""
        self.active_topics = []
        for algo in selected_algos:
            if algo in self.algo_topic_map:
                self.active_topics.extend(self.algo_topic_map[algo])
        
        # Fallback: Se nada for selecionado ou erro, ativa tudo
        if not self.active_topics:
            for topics in self.algo_topic_map.values():
                self.active_topics.extend(topics)

    def generate_problem(self):
        # Loop de segurança
        for _ in range(5): 
            try:
                if not self.active_topics:
                    topic = "busca_linear_contagem" # Fallback extremo
                else:
                    topic = random.choice(self.active_topics)
                
                prob = None

                if topic == "busca_linear_contagem":
                    prob = self._gen_linear_search_count()
                elif topic == "busca_linear_prox_comp":
                    prob = self._gen_linear_search_next_comparison()
                elif topic == "busca_binaria_indice":
                    prob = self._gen_binary_search_index()
                elif topic == "busca_binaria_prox_comp":
                    prob = self._gen_binary_search_next_comparison()
                elif topic == "insertion_sort_pivo":
                    prob = self._gen_insertion_sort_pivot()
                elif topic == "insertion_sort_prox_comp":
                    prob = self._gen_insertion_sort_next_comparison()
                
                if prob:
                    return self._process_options(prob)
            
            except (ValueError, IndexError):
                continue
        
        # Fallback de emergência
        return self._process_options(self._gen_linear_search_count())

    def _process_options(self, prob):
        options = prob["options"]
        correct_val = str(prob["correct"])
        
        # Converte tudo para string e remove duplicatas
        options = list(set([str(o) for o in options]))
        
        if correct_val not in options:
            options.append(correct_val)
        
        # Completa opções
        while len(options) < 4:
            fake_option = "Encontra o valor " + str(random.randint(0, max(1, int(correct_val)*2))) + "."
            if fake_option not in options:
                options.append(fake_option)

        random.shuffle(options)
        final_options = options[:4]
        
        # Segurança final: garante que a resposta correta está nas 4 finais
        if correct_val not in final_options:
            final_options[0] = correct_val
            random.shuffle(final_options)

        letters = ["A", "B", "C", "D"]
        correct_letter = letters[final_options.index(correct_val)]
        
        prob["choices"] = dict(zip(letters, final_options))
        prob["correct_letter"] = correct_letter
        return prob

    # --- BUSCA LINEAR ---
    def _gen_linear_search_count(self):
        array_size = 7
        data = [random.randint(1, 20) for _ in range(array_size)]
        target = random.choice(data)
        trace = alg.gen_linear_search(data, target, filename=QUIZ_LOG_FILE_NAME)
        
        if not trace: raise ValueError("Trace vazio")
        
        step = random.randint(0, len(trace)-1)
        correct = trace[step]["comparações"]
        options = [str(correct), str(correct+1), str(correct-1), "0"]
        random.shuffle(options)

        return {
            "type": "search", "algo": LINEAR_SEARCH_NAME, "array": data, "target": target,
            "step_to_show": step, "trace": trace, 
            "question": f"Busca Linear: Sabendo que a chave é {target}, quantas comparações foram feitas até o momento mostrado?",
            "correct": correct, 
            "options": options
        }

    def _gen_linear_search_next_comparison(self):
        array_size = 8
        data = [random.randint(1, 30) for _ in range(array_size)]
        target = random.choice(data) if random.random() > 0.3 else 99
        trace = alg.gen_linear_search(data, target, filename=QUIZ_LOG_FILE_NAME)
        
        if len(trace) < 2: raise ValueError("Trace muito curto")
        
        step = random.randint(0, len(trace)-2)
        next_state = trace[step+1]
        
        if next_state.get("finalizado", False):
            correct = "Algoritmo Encerrará"
        elif next_state.get("encontrado", False):
             correct = "Elemento encontrado"
        else:
            idx = next_state["idx"]
            val = next_state["array"][idx]
            correct = f"Comparar {val} com {target}"

        fake_idx = (trace[step]["idx"] + 2) % len(data)
        aux = len(data)-1
        fake_idx2 = aux if fake_idx != aux and aux > 0 else fake_idx+1

        options = [
            f"Comparar {data[fake_idx]} com {target}", 
            f"Comparar {data[fake_idx2]} com {target}",
            "Continuar busca",
            "Fim da busca"
        ]
        random.shuffle(options)
        options = options[0:3]
        options.append(correct)
        random.shuffle(options)
        
        return {
            "type": "search", "algo": LINEAR_SEARCH_NAME, "array": data, "target": target,
            "step_to_show": step, "trace": trace, 
            "question": f"Busca Linear: Sabendo que a chave é {target}, o que acontecerá na PRÓXIMA iteração (Passo {step+2})?",
            "correct": correct, 
            "options": options
        }

    # --- BUSCA BINARIA ---
    def _gen_binary_search_index(self):
        data = sorted(random.sample(range(1, 50), 10))
        target = random.choice(data)
        trace = alg.gen_binary_search(data, target, filename=QUIZ_LOG_FILE_NAME)
        
        valid_steps = [i for i, s in enumerate(trace) if s.get("m", -1) != -1]
        if not valid_steps: raise ValueError("Sem passos válidos")
        
        step = random.choice(valid_steps)
        correct = trace[step]["m"]
        l, r = trace[step]["l"], trace[step]["r"]

        options = [str(correct), str(correct+1), str(correct-1 if correct>0 else 2), str(len(data)-1)]
        random.shuffle(options)

        return {
            "type": "search", "algo": BINARY_SEARCH_NAME, "array": data, "target": target,
            "step_to_show": step, "trace": trace,
            "question": f"Busca Binária: Sabendo que a chave é {target}, qual o índice do elemento 'meio' (m) neste passo?",
            "correct": correct, 
            "options": options
        }

    def _gen_binary_search_next_comparison(self):
        data = sorted(random.sample(range(1, 50), 12))
        target = random.choice(data)
        trace = alg.gen_binary_search(data, target, filename=QUIZ_LOG_FILE_NAME)
        
        if len(trace) < 2: raise ValueError("Trace muito curto")
        
        step = random.randint(0, len(trace)-2)
        next_state = trace[step+1]
        
        if next_state.get("finalizado"):
            correct = "Encerrar busca (não achou)"
        elif next_state.get("encontrado"):
            val = next_state["array"][next_state["m"]]
            correct = f"Encontrar {val} no índice {next_state['m']}"
        else:
            m = next_state["m"]
            val = next_state["array"][m]
            correct = f"Comparar {val} com {target}"

        l, r = trace[step]["l"], trace[step]["r"]
        
        options = [f"Comparar {data[0]} com {target}", f"Comparar {data[l]} com {data[r]}", "Encerrar busca", "Continuar busca"]
        random.shuffle(options)
        options = options[0:3]
        options.append(correct)
        random.shuffle(options)

        return {
            "type": "search", "algo": BINARY_SEARCH_NAME, "array": data, "target": target,
            "step_to_show": step, "trace": trace,
            "question": f"Busca Binária: Sabendo que a chave é {target}, baseado no estado atual (l={l}, r={r}) qual a ação do PRÓXIMO passo?",
            "correct": correct,
            "options": options
        }

    # --- INSERTION SORT ---
    def _gen_insertion_sort_pivot(self):
        data = [random.randint(1, 20) for _ in range(6)]
        trace = alg.gen_insertion_sort(list(data), filename=QUIZ_LOG_FILE_NAME)
        
        if not trace: raise ValueError("Trace vazio")
        step = random.randint(0, len(trace)-1)
        
        correct = trace[step].get("target_key_val", data[0])
        options = [str(correct)] + [str(x) for x in random.sample(data, 3)]
        random.shuffle(options)
        return {
            "type": "sort", "algo": INSERTION_SORT_NAME, "array": data,
            "step_to_show": step, "trace": trace,
            "question": "Insertion Sort: Qual o valor da chave (pivô) que está sendo posicionada?",
            "correct": correct, 
            "options": options
        }

    def _gen_insertion_sort_next_comparison(self):
        data = [random.randint(1, 30) for _ in range(6)]
        trace = alg.gen_insertion_sort(list(data), filename=QUIZ_LOG_FILE_NAME)
        
        if len(trace) < 2: raise ValueError("Trace muito curto")
        
        step = random.randint(0, len(trace)-2)
        
        curr_state = trace[step]
        next_state = trace[step+1]
        
        if next_state["target_key_idx"] != curr_state["target_key_idx"]:
            correct = f"Novo pivô: selecionar {next_state['target_key_val']}"
        else:
            idx_comp = next_state["curr_j"]
            if idx_comp >= 0:
                val_comp = next_state["array"][idx_comp]
                correct = f"Comparar {val_comp} com Chave {curr_state['target_key_val']}"
            else:
                correct = f"Inserir Chave na posição 0"

        return {
            "type": "sort", "algo": INSERTION_SORT_NAME, "array": data,
            "step_to_show": step, "trace": trace,
            "question": "Insertion Sort: Qual a ação lógica imediata na PRÓXIMA iteração?",
            "correct": correct,
            "options": [correct, "Trocar primeiros elementos", "Ordernar array completo", "Comparar com índice -1"]
        }