class Narrativa:
    def __init__(self, jogo):
        self.jogo = jogo
        self.segredos = {
            'ciclo': {'pistas': 0, 'revelado': False, 'desc': "A ilha está presa em um ciclo temporal eterno"},
            'entidade': {'pistas': 0, 'revelado': False, 'desc': "Uma entidade ancestral controla os eventos"},
            'sacrificio': {'pistas': 0, 'revelado': False, 'desc': "Rituais de sacrifício mantêm a ilha ativa"}
        }
        self.eventos_scriptados = {
            1: self.evento_dia1,
            2: self.evento_dia2,
            3: self.evento_dia3,
            4: self.evento_dia4,
            5: self.evento_dia5,
            6: self.evento_dia6,
            7: self.evento_dia7
        }
        self.dilemas = [
            {
                'condicao': lambda: self.jogo.jogador['fome'] > 70,
                'texto': "Você encontra comida suficiente apenas para 1 pessoa:",
                'opcoes': {
                    '1': {'texto': "Comer sozinho", 'moral': -20, 'fome': 100, 'sanidade': -10},
                    '2': {'texto': "Dividir", 'moral': 10, 'fome': 60, 'relacionamentos': +15},
                    '3': {'texto': "Dar para o grupo", 'moral': 30, 'fome': 30, 'relacionamentos': +30}
                }
            },
            {
                'condicao': lambda: self.jogo.jogador['ferimentos'] >= 2,
                'texto': "Você encontra um kit médico abandonado:",
                'opcoes': {
                    '1': {'texto': "Usar em si mesmo", 'moral': -10, 'ferimentos': -2},
                    '2': {'texto': "Dividir com o grupo", 'moral': +20, 'ferimentos': -1}
                }
            }
        ]
        self.dialogos_npcs = {
            'Alex': [
                "Ouvi rumores de uma caverna sagrada... deveríamos investigar?",
                "Se não arriscarmos, nunca escaparemos desta ilha!"
            ],
            'Rina': [
                "Estes símbolos... eles não são de nenhuma cultura conhecida!",
                "Precisamos documentar tudo, isso é extraordinário!"
            ],
            'Tom': [
                "Pare de fuçar nessas coisas e ajude a proteger o acampamento!",
                "Confie em mim, força bruta resolve qualquer problema!"
            ]
        }

    def verificar_eventos_dia(self):
        # Evento do dia atual
        if self.jogo.dia in self.eventos_scriptados:
            self.eventos_scriptados[self.jogo.dia]()
            
        # Eventos aleatórios
        if random.random() < 0.4:
            self.evento_aleatorio()
            
        # Dilemas morais
        for dilema in self.dilemas:
            if dilema['condicao']():
                self.apresentar_dilema(dilema)
                
        # Eventos de sanidade
        if self.jogo.jogador['sanidade'] < 40:
            self.evento_sanidade()

    def evento_dia1(self):
        self.jogo.imprimir_lento("\n🌴 Dia 1 - O Despertar")
        self.jogo.mostrar_arte('praia')
        self.jogo.imprimir_lento("Ao abrir os olhos, a realidade se impõe: areia quente, sol implacável e... silêncio.")
        self.jogo.imprimir_lento("Seu primeiro desafio: encontrar água potável e avaliar os recursos.")

    def evento_dia2(self):
        self.jogo.imprimir_lento("\n🔦 Dia 2 - Primeiras Descobertas")
        self.jogo.mostrar_arte('floresta')
        self.jogo.imprimir_lento("Marcas nas árvores sugerem que você não é o primeiro aqui.")
        if 'Exploração' in self.jogo.jogador['habilidades']:
            self.jogo.imprimir_lento("Sua habilidade de exploração revela uma trilha escondida!")
            self.adicionar_pista('sacrificio')

    def evento_dia3(self):
        self.jogo.imprimir_lento("\n🌩️ Dia 3 - A Provação")
        self.jogo.mostrar_arte('tempestade')
        self.jogo.imprimir_lento("O clima se volta contra vocês. Ventos uivantes carregam vozes sussurrantes.")
        if 'abrigo' in self.jogo.jogador['inventario']:
            self.jogo.imprimir_lento("Seu abrigo resiste, mas os sons perturbadores persistem...")
            self.jogo.jogador['sanidade'] -= 15
        else:
            self.jogo.imprimir_lento("Exposto aos elementos, você questiona sua sanidade...")
            self.jogo.jogador['sanidade'] -= 30

    def evento_dia4(self):
        self.jogo.imprimir_lento("\n💀 Dia 4 - O Preço da Sobrevivência")
        self.jogo.mostrar_arte('caverna')
        self.jogo.imprimir_lento("Você encontra restos mortais com um diário manchado:")
        escolha = input("Ler o diário? (1-Sim/2-Não) ")
        if escolha == '1':
            self.jogo.imprimir_lento("'Eles exigem sacrifícios... o ciclo nunca termina' - última entrada")
            self.adicionar_pista('ciclo')
            self.jogo.jogador['sanidade'] -= 25

    def evento_dia5(self):
        self.jogo.imprimir_lento("\n🌀 Dia 5 - O Véu se Abre")
        self.jogo.mostrar_arte('simbolos')
        self.jogo.imprimir_lento("Padrões geométricos nas rochas pulsam com energia estranha.")
        if 'Pesquisador' in self.jogo.jogador['arquetipo']:
            self.jogo.imprimir_lento("Sua mente analítica decifra parte dos símbolos!")
            self.adicionar_pista('entidade')
        else:
            self.jogo.imprimir_lento("Há uma lógica aqui, mas ela escapa à sua compreensão...")

    def evento_dia6(self):
        self.jogo.imprimir_lento("\n⚖️ Dia 6 - A Encruzilhada")
        self.jogo.mostrar_arte('trilha')
        self.jogo.imprimir_lento("Duas trilhas se revelam: uma para o vulcão, outra para as cavernas.")
        escolha = input("Seguir para (1-Vulcão/2-Cavernas) ")
        if escolha == '1':
            self.jogo.imprimir_lento("Fumaça tóxica testa sua resistência física!")
            self.jogo.jogador['energia'] -= 40
            self.adicionar_pista('ciclo')
        else:
            self.jogo.imprimir_lento("Sombras movem-se nas profundezas...")
            self.jogo.jogador['sanidade'] -= 25
            self.adicionar_pista('entidade')

    def evento_dia7(self):
        self.jogo.imprimir_lento("\n🔥 Dia 7 - O Ritual Final")
        self.jogo.mostrar_arte('vulcao')
        self.jogo.imprimir_lento("A ilha treme enquanto forças antigas despertam. Suas escolhas ecoam:")
        
        if self.segredos['ciclo']['revelado']:
            self.jogo.imprimir_lento("\nVocê compreende o ciclo - pode quebrá-lo ou perpetuá-lo!")
            escolha = input("(1-Quebrar ciclo/2-Usar poder) ")
            if escolha == '1':
                self.jogo.jogador['moralidade'] += 50
            else:
                self.jogo.jogador['moralidade'] -= 50
                
        elif self.segredos['entidade']['revelado']:
            self.jogo.imprimir_lento("\nA entidade exige um sacrifício para libertá-los!")
            escolha = input("(1-Oferecer a si mesmo/2-Oferecer NPC) ")
            if escolha == '1':
                self.jogo.jogador['sanidade'] = 0
            else:
                npc = random.choice([n for n in self.jogo.npcs if n['vivo']])
                npc['vivo'] = False

    def evento_aleatorio(self):
        eventos = [
            ("Um animal ferido precisa de ajuda", self.dilema_animal),
            ("Você encontra um artefato estranho", self.descobrir_artefato),
            ("Um NPC pede ajuda para uma tarefa perigosa", self.missao_perigosa)
        ]
        evento = random.choice(eventos)
        self.jogo.imprimir_lento(f"\n⚡ EVENTO: {evento[0]}")
        evento[1]()

    def dilema_animal(self):
        print("1. Matar para comida")
        print("2. Cuidar do animal")
        print("3. Ignorar")
        escolha = input("Escolha: ")
        
        efeitos = {
            '1': {'moral': -15, 'fome': +30},
            '2': {'moral': +10, 'energia': -20},
            '3': {'sanidade': -5}
        }
        self.aplicar_efeitos(efeitos.get(escolha, {}))

    def descobrir_artefato(self):
        self.jogo.imprimir_lento("O artefato emite uma energia perturbadora...")
        escolha = input("1-Tocar/2-Enterrar/3-Levar ao acampamento ")
        efeitos = {
            '1': {'sanidade': -20, 'pista': 'entidade'},
            '2': {'moral': +10},
            '3': {'relacionamentos': -15, 'pista': 'sacrificio'}
        }
        if escolha in efeitos:
            if 'pista' in efeitos[escollha]:
                self.adicionar_pista(efeitos[escolha]['pista'])

    def aplicar_efeitos(self, efeitos):
        for attr, valor in efeitos.items():
            if attr in self.jogo.jogador:
                self.jogo.jogador[attr] += valor
            elif attr == 'pista':
                self.adicionar_pista(valor)

    def determinar_final(self):
        pontos = {
            'moral': self.jogo.jogador['moralidade'],
            'segredos': sum(1 for s in self.segredos.values() if s['revelado']),
            'relacionamentos': sum(n['afinidade'] for n in self.jogo.npcs if n['vivo']),
            'sanidade': self.jogo.jogador['sanidade']
        }

        if pontos['segredos'] >= 3 and pontos['sanidade'] > 20:
            return ("MESTRE DOS MISTÉRIOS", "Você desvendou todos segredos, mas a ilha jamais te libertará")
            
        elif pontos['moral'] >= 80 and pontos['relacionamentos'] >= 150:
            return ("LÍDER BENEVOLENTE", "Seu grupo escapa unido, levando os segredos da ilha")
            
        elif pontos['moral'] <= -50:
            return ("TIRANO DA ILHA", "Você governa através do medo, tornando-se parte do ciclo")
            
        elif pontos['sanidade'] <= 0:
            return ("VISIONÁRIO LOUCO", "As vozes guiam você para uma existência além da compreensão")
            
        else:
            return ("SOBREVIVENTE", "Você persiste, mas os mistérios permanecem intocados")