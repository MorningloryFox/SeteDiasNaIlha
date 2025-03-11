import time
import random
import pygame
import sys
from collections import defaultdict
from narrativa import Narrativa

class Jogo:
    def __init__(self):
        try:
            pygame.mixer.init()
        except:
            print("Audio system not available. Game will run without sound.")
        self.sons = {}
        self.ascii_art = {}  # Initialize ascii_art dictionary
        self.dia = 1
        self.jogador = {
            'nome': '',
            'aparencia': {},
            'personalidade': {},
            'habilidades': defaultdict(int),
            'arquetipo': '',
            'fome': 100,
            'sede': 100,
            'energia': 100,
            'sanidade': 100,
            'ferimentos': 0,
            'moralidade': 0,
            'inventario': defaultdict(int),
            'relacionamentos': defaultdict(int),
            'decisoes': []
        }
        self.npcs = []
        self.locais = ['praia', 'floresta', 'caverna', 'montanha']
        self.eventos = []
        self.finais = []
        self.narrativa = Narrativa(self)  # Initialize Narrativa here
        self.carregar_recursos()

    def carregar_recursos(self):
        # Initialize empty dictionaries
        self.sons = {}
        self.ascii_art = {}
        
        # Try to load sounds but continue if they fail
        try:
            self.sons = {
                'onda': pygame.mixer.Sound('sons/onda.wav'),
                'floresta': pygame.mixer.Sound('sons/floresta.wav'),
                'perigo': pygame.mixer.Sound('sons/perigo.wav'),
                'suspense': pygame.mixer.Sound('sons/suspense.wav')
            }
        except Exception as e:
            print(f"Erro ao carregar sons: {e}")
        
        # Load ASCII art from files with error handling
        art_files = {
            'praia': 'arte/praia.txt',
            'floresta': 'arte/floresta.txt',
            'caverna': 'arte/caverna.txt'
        }
        
        for art_name, file_path in art_files.items():
            try:
                with open(file_path, 'r') as f:
                    self.ascii_art[art_name] = f.read()
            except Exception as e:
                print(f"Erro ao carregar {art_name}: {e}")
                self.ascii_art[art_name] = f"{art_name.title()} não encontrada"
        
        # Add built-in ASCII art
        built_in_art = {
            'naufragio': r"""
              .-""-.
             / .--. \
            / /    \ \
            | |    | |
            | |.-""-.|
            ///`.::::.`\
            ||| ::/  \:: ;
            ||; ::\__/:: ;
            \ '::::'--' /
             `=':-..-'`
            """,
            'sombras': r"""
⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣤⣶⣶⣶⣶⣦⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣀⣤⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⣀⠀⠀⠀
⢀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠛⠻⢿⣿⣿⣿⣿⣿⣿⣷⣦⡀
⣴⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡟⠁⠀⣠⣴⣶⣿⣿⣷⣶⣄⣀⣀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿
⣿⣿⣿⣿⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⢻⣿⣿⣿
⣿⣿⣿⡇⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⢸⣿⣿⣿
⣿⣿⣿⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⢸⣿⣿⣿
⣿⣿⣿⣧⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⣼⣿⣿⣿
            """,
            'sobreviventes': r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣴⣶⣾⣿⣿⣿⣿⣿⣿⣿⣶⣦⣄⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀
⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀
⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀
⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠛⠛⠛⠛⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄
⢀⣿⣿⣿⣿⡿⠟⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠻⣿⣿⣿⣿⣿⣿⡄
⣾⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣧
⢸⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿
⣿⣿⣿⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿
⣿⣿⣿⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿
            """
        }
        self.ascii_art.update(built_in_art)

    def introducao(self):
        if 'onda' in self.sons:
            try:
                self.sons['onda'].play(-1)
            except:
                pass
        self.imprimir_lento("\n\n█▓▒­░⡷⠂༒༙   S O B R E V I V E N T E S   D A   I L H A  ⠐༒༙⠐⢾░▒▓█\n")
        
        self.imprimir_lento("Sua garganta queima. O gosto metálico do sangue se mistura com o salitre. ", 0.05)
        self.imprimir_lento("Cada respiração traz areia quente e o cheiro acre de algas em decomposição. ", 0.05)
        self.imprimir_lento("Seus dedos enterram-se na areia áspera enquanto tenta se levantar...\n", 0.06)
        
        input("\n[Pressione Enter para continuar]")
        
        self.mostrar_arte('naufragio')
        self.imprimir_lento("\n\nMemórias fragmentadas invadem sua mente:", 0.04)
        self.imprimir_lento("▸ O navio cortando ondas revoltas sob um céu de chumbo", 0.03)
        self.imprimir_lento("▸ Gritos sendo engolidos pelo rugido do vento", 0.03)
        self.imprimir_lento("▸ Seus dedos escorregando da corda molhada", 0.03)
        self.imprimir_lento("▸ A escuridão. Sempre a escuridão...\n", 0.05)
        
        if 'perigo' in self.sons:
            try:
                self.sons['perigo'].play()
            except:
                pass
        self.imprimir_lento("\nAlgo se move entre as palmeiras. Você não está sozinho.", 0.05)
        self.mostrar_arte('sombras')
        
        escolha = input("\n1-Investigar  2-Fingir que não viu  3-Gritar\n-> ")
        if escolha == '1':
            self.jogador['sanidade'] -= 10
            self.imprimir_lento("\nNada além de galhos quebrados... mas as pegadas são grandes demais.", 0.04)
        elif escolha == '3':
            self.jogador['moralidade'] -= 5
            self.imprimir_lento("\nSeu eco se perde no mar. Ninguém responde.", 0.04)
        
        if 'floresta' in self.sons:
            try:
                self.sons['floresta'].play()
            except:
                pass
        self.imprimir_lento("\n\nA floresta sussurra:", 0.05)
        self.imprimir_lento("▸ Insetos zumbem em padrões dissonantes", 0.04)
        self.imprimir_lento("▸ Folhas secas crepitam sob passos invisíveis", 0.04)
        self.imprimir_lento("▸ O ar pesa como um cobertor úmido\n", 0.05)
        
        self.mostrar_arte('sobreviventes')
        self.imprimir_lento("\nTrês figuras emergem da vegetação:", 0.05)
        self.imprimir_lento("▸ Um homem musculoso com cicatrizes recentes (Tom)", 0.03)
        self.imprimir_lento("▸ Uma mulher de óculos quebrados segurando um caderno (Rina)", 0.03)
        self.imprimir_lento("▸ Um aventureiro sorridente com facão ensanguentado (Alex)\n", 0.03)
        
        input("\n[Pressione Enter para enfrentar seu novo mundo]")
        
        if 'floresta' in self.sons:
            try:
                self.sons['floresta'].fadeout(2000)
            except:
                pass
        if 'onda' in self.sons:
            try:
                self.sons['onda'].fadeout(2000)
            except:
                pass
        self.imprimir_lento("\n\nA ilha respira. E observa.", 0.07)
        self.imprimir_lento("Sete dias. Sete testes. Sete chances.", 0.07)
        self.imprimir_lento("O que você fará para sobreviver?\n\n", 0.07)

    def criar_personagem(self):
        self.imprimir_lento("\nEntre as sombras do passado, quem emerge?")
        
        # Nome com verificação
        while True:
            nome = input("\nQual é o seu nome? ").strip()
            if 2 <= len(nome) <= 12:
                self.jogador['nome'] = nome
                break
            print("Nome deve ter entre 2-12 caracteres")

        # Aparência com descrições
        print("\nEscolha sua aparência:")
        opcoes_cabelo = {
            1: ("Preto", "Herança indígena/mestiça, prático para sobrevivência"),
            2: ("Loiro", "Cabelos queimados pelo sol, lembranças de outro clima"),
            3: ("Ruivo", "Herança maldita? Os olhares seguem você"),
            4: ("Castanho", "Comum, ajuda a passar despercebido")
        }
        self.mostrar_opcoes_detalhadas(opcoes_cabelo)
        self.jogador['aparencia']['cabelo'] = self.selecionar_opcao(opcoes_cabelo)

        # Cor dos olhos com descrições
        print("\nEscolha a cor dos seus olhos:")
        opcoes_olhos = {
            1: ("Azul", "Olhos que refletem o céu e o mar, profundos e misteriosos"),
            2: ("Verde", "Olhos que lembram a floresta, atentos e vigilantes"),
            3: ("Castanho", "Olhos comuns, mas cheios de determinação"),
            4: ("Cinza", "Olhos que parecem ver além, frios e calculistas")
        }
        self.mostrar_opcoes_detalhadas(opcoes_olhos)
        self.jogador['aparencia']['olhos'] = self.selecionar_opcao(opcoes_olhos)

        # Físico do corpo com descrições
        print("\nEscolha seu físico:")
        opcoes_fisico = {
            1: ("Atlético", "Corpo treinado, pronto para qualquer desafio físico"),
            2: ("Magro", "Ágil e rápido, mas menos resistente"),
            3: ("Forte", "Músculos poderosos, mas menos ágil"),
            4: ("Normal", "Equilíbrio entre força e agilidade")
        }
        self.mostrar_opcoes_detalhadas(opcoes_fisico)
        self.jogador['aparencia']['fisico'] = self.selecionar_opcao(opcoes_fisico)

        # Personalidade com impacto narrativo
        print("\nDefina sua essência:")
        self.jogador['personalidade'] = self.selecionar_multiplas({
            1: ("Impulsivo", "+20% chance de ataques críticos, -30% percepção de perigo"),
            2: ("Analítico", "+1 slot de inventário, -10% velocidade de ação"),
            3: ("Empático", "+25% eficiência em diálogos, vulnerável a manipulação"),
            4: ("Cauteloso", "+15% defesa, -20% recursos encontrados"),
            5: ("Ambicioso", "Desbloqueia finais especiais, -40% confiança do grupo")
        }, 3)
        
        # Habilidades com árvores de progressão
        print("\nEscolha 2 habilidades iniciais:")
        habilidades_escolhidas = self.selecionar_multiplas({
            1: ("Caça", "Rastrear animais | Armadilhas improvisadas"),
            2: ("Construção", "Abrigos reforçados | Armadilhas defensivas"),
            3: ("Cura", "Remédios naturais | Primeiros socorros"),
            4: ("Persuasão", "Negociação | Intimidação"),
            5: ("Exploração", "Navegação | Detectar perigos")
        }, 2)
        
        for hab in habilidades_escolhidas:
            self.jogador['habilidades'][hab] = 1
        
        self.definir_arquetipo()

    def definir_arquetipo(self):
        tracos = self.jogador['personalidade']
        if 'Analítico' in tracos and 'Cauteloso' in tracos:
            self.jogador['arquetipo'] = 'Pesquisador'
        elif 'Impulsivo' in tracos and 'Ambicioso' in tracos:
            self.jogador['arquetipo'] = 'Aventureiro'
        elif 'Empático' in tracos:
            self.jogador['arquetipo'] = 'Líder'
        else:
            self.jogador['arquetipo'] = 'Sobrevivente'

    def criar_npcs(self):
        npcs = [
            {
                'nome': 'Alex',
                'arquetipo': 'Aventureiro',
                'personalidade': ['Confidente', 'Arrogante'],
                'afinidade': 50,
                'vivo': True
            },
            {
                'nome': 'Rina',
                'arquetipo': 'Pesquisador',
                'personalidade': ['Analítica', 'Hesitante'],
                'afinidade': 50,
                'vivo': True
            },
            {
                'nome': 'Tom',
                'arquetipo': 'Bruto',
                'personalidade': ['Protetor', 'Impulsivo'],
                'afinidade': 50,
                'vivo': True
            }
        ]
        self.npcs = npcs

    def loop_principal(self):
        while self.dia <= 7 and self.jogador_vivo():
            self.iniciar_dia()
            if self.dia == 1:
                self.evento_introducao_npcs()
            self.processar_acoes()
            self.avancar_tempo()
            self.dia += 1
        self.finalizar_jogo()
        
    def status_jogador(self):
        print(f"\n=== {self.jogador['nome'].upper()} ===")
        print(f"Arquétipo: {self.jogador['arquetipo']}")
        print("⚡ Energia: \t" + self.barra_status(self.jogador['energia']))
        print("🍖 Fome: \t" + self.barra_status(self.jogador['fome']))
        print("💧 Sede: \t" + self.barra_status(self.jogador['sede']))
        print("🧠 Sanidade: \t" + self.barra_status(self.jogador['sanidade']))
        print(f"💼 Inventário: {dict(self.jogador['inventario'])}")

    def barra_status(self, valor):
        return '█' * (valor // 10) + '░' * (10 - valor // 10) + f' {valor}%'

    def iniciar_dia(self):
        print(f"\n=== DIA {self.dia} ===")
        self.status_jogador()
        self.narrativa.verificar_eventos_dia()
        self.atualizar_estados()
        
    def evento_introducao_npcs(self):
        self.imprimir_lento("\n🎭 Conheça os sobreviventes:")
        for npc in self.npcs:
            dialogo = random.choice(self.narrativa.dialogos_npcs[npc['nome']])
            self.imprimir_lento(f"{npc['nome']}: {dialogo}")

    def processar_acoes(self):
        print("\nAções disponíveis:")
        print("1. Explorar a ilha")
        print("2. Coletar recursos")
        print("3. Construir abrigo")
        print("4. Interagir com NPCs")
        print("5. Descansar")
        escolha = input("Escolha: ")
        
        if escolha == '1':
            self.explorar()
        elif escolha == '2':
            self.coletar_recursos()
        elif escolha == '3':
            self.construir_abrigo()
        elif escolha == '4':
            self.interagir_npc()
        elif escolha == '5':
            self.descansar()
        else:
            print("Ação inválida!")

    def explorar(self):
        local = random.choice(self.locais)
        self.imprimir_lento(f"\nVocê explora {local.upper()}...")
        self.mostrar_arte(local)
        
        evento = random.choice([
            self.encontrar_recursos,
            self.enfrentar_perigo,
            self.descobrir_segredo
        ])
        evento()
        
        self.jogador['energia'] -= 30
        self.jogador['fome'] -= 20
        self.jogador['sede'] -= 20

    def encontrar_recursos(self):
        recursos = ['madeira', 'pedra', 'fruta', 'erva']
        recurso = random.choice(recursos)
        quantidade = random.randint(1, 3)
        self.jogador['inventario'][recurso] += quantidade
        self.imprimir_lento(f"Você encontrou {quantidade}x {recurso}!")

    def enfrentar_perigo(self):
        dano = random.randint(10, 30)
        self.jogador['energia'] -= dano
        self.imprimir_lento(f"Você sofreu {dano} de dano!")

    def descobrir_segredo(self):
        self.imprimir_lento("Você encontrou um local secreto!")
        self.jogador['sanidade'] += 10

    def coletar_recursos(self):
        self.imprimir_lento("Coletando recursos...")
        recursos = ['madeira', 'pedra', 'fruta', 'erva']
        recurso = random.choice(recursos)
        quantidade = random.randint(1, 3)
        self.jogador['inventario'][recurso] += quantidade
        self.imprimir_lento(f"Você coletou {quantidade}x {recurso}!")
        self.jogador['energia'] -= 10

    def construir_abrigo(self):
        madeira_atual = self.jogador['inventario'].get('madeira', 0)
        if madeira_atual >= 3:
            self.jogador['inventario']['madeira'] -= 3
            self.jogador['energia'] += 20
            self.imprimir_lento("Você construiu um abrigo e descansou!")
        else:
            self.imprimir_lento(f"Você precisa de 3 madeiras para construir um abrigo! (Tem {madeira_atual})")

    def descansar(self):
        self.jogador['energia'] = min(100, self.jogador['energia'] + 30)
        self.imprimir_lento("Você descansou e recuperou energia!")

    def avancar_tempo(self):
        self.jogador['energia'] = min(100, self.jogador['energia'] + 20)
        self.imprimir_lento("O dia termina...")

    def trocar_recursos(self, npc):
        if len(self.jogador['inventario']) == 0:
            self.imprimir_lento("Você não tem recursos para trocar!")
            return
            
        print("\nSeus recursos:")
        for item, qtd in self.jogador['inventario'].items():
            if qtd > 0:
                print(f"{item}: {qtd}")
                
        item = input("Qual item deseja trocar? ")
        if item not in self.jogador['inventario'] or self.jogador['inventario'][item] <= 0:
            self.imprimir_lento("Você não possui esse item!")
            return
            
        self.jogador['inventario'][item] -= 1
        novo_item = random.choice(['comida', 'água', 'medicamento'])
        self.jogador['inventario'][novo_item] = self.jogador['inventario'].get(novo_item, 0) + 1
        self.imprimir_lento(f"Você trocou 1x {item} por 1x {novo_item}")
        npc['afinidade'] += 5

    def confrontar(self, npc):
        self.imprimir_lento(f"Você confronta {npc['nome']}!")
        npc['afinidade'] -= 20
        self.jogador['moralidade'] -= 10

    def interagir_npc(self):
        print("\nNPCs disponíveis:")
        for i, npc in enumerate(self.npcs):
            if npc['vivo']:
                print(f"{i+1}. {npc['nome']} ({npc['arquetipo']})")
                
        try:
            escolha = int(input("Escolha um NPC: ")) - 1
            if 0 <= escolha < len(self.npcs):
                npc = self.npcs[escolha]
            else:
                print("NPC inválido!")
                return
        except ValueError:
            print("Por favor, digite um número.")
            return
        
        print(f"\nInteragindo com {npc['nome']}:")
        print("1. Conversar")
        print("2. Trocar recursos")
        print("3. Confrontar")
        acao = input("Escolha: ")
        
        if acao == '1':
            self.conversar(npc)
        elif acao == '2':
            self.trocar_recursos(npc)
        elif acao == '3':
            self.confrontar(npc)
        else:
            print("Ação inválida!")

    def conversar(self, npc):
        temas = {
            'Aventureiro': ['Exploração', 'Perigos'],
            'Pesquisador': ['Descobertas', 'Tecnologia'],
            'Bruto': ['Segurança', 'Recursos']
        }
        
        tema = random.choice(temas[npc['arquetipo']])
        print(f"\nConversa sobre {tema}:")
        
        if self.jogador['habilidades']['Persuasão'] > 0:
            print("1. Concordar")
            print("2. Discordar")
            print("3. Mudar de assunto")
            escolha = input("Escolha: ")
            
            if escolha == '1':
                npc['afinidade'] += 10
            elif escolha == '2':
                npc['afinidade'] -= 15
        else:
            print("Sua falta de persuasão limita a conversa")
        npc['afinidade'] += 5  # Ajuste para aumentar afinidade mesmo sem persuasão

    def atualizar_estados(self):
        for stat in ['fome', 'sede', 'energia']:
            if self.jogador[stat] <= 0:
                self.jogador['sanidade'] -= 20
                
        if self.jogador['sanidade'] <= 30:
            self.evento_sanidade()

    def evento_sanidade(self):
        eventos = [
            "Você começa a ouvir vozes...",
            "Sombras parecem se mover na periferia da sua visão",
            "Seus pensamentos ficam confusos e fragmentados"
        ]
        self.imprimir_lento("\n💀 SANIDADE BAIXA: " + random.choice(eventos))
        self.jogador['moralidade'] -= 10

    def finalizar_jogo(self):
        print("\n=== FIM DO JOGO ===")
        print(f"Dias sobrevividos: {self.dia-1}")
        print(f"Arquétipo final: {self.jogador['arquetipo']}")
        print("\nRelacionamentos:")
        for npc in self.npcs:
            status = "Vivo" if npc['vivo'] else "Morto"
            print(f"{npc['nome']}: {npc['afinidade']} ({status})")
        
        self.determinar_final()

    def determinar_final(self):
        final = self.narrativa.determinar_final()
        finais = {
            'HERÓICO': "🎉 Você liderou o grupo para segurança encontrando um meio de escapar!",
            'TRAGICO': "💀 A ilha cobrou seu preço em sangue...",
            'MÍSTICO': "🔮 Você desvendou os segredos ancestrais, mas a ilha nunca mais te libertará",
            'NEUTRO': "🌴 Você sobreviveu, mas a ilha guarda seus segredos para sempre"
        }
        self.imprimir_lento(f"\nFINAL {final}: {finais[final]}")

    def imprimir_lento(self, texto, delay=0.03):
        for letra in texto:
            sys.stdout.write(letra)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def mostrar_arte(self, nome):
        try:
            if nome in self.ascii_art:
                print(self.ascii_art[nome])
            else:
                print(f"Arte '{nome}' não encontrada")
        except Exception as e:
            print(f"Erro ao mostrar arte: {e}")

    def mostrar_opcoes_detalhadas(self, opcoes):
        for i, (nome, desc) in opcoes.items():
            print(f"{i}. {nome} - {desc}")

    def selecionar_opcao(self, opcoes):
        while True:
            try:
                escolha = int(input("Escolha: "))
                if escolha in opcoes:
                    return opcoes[escolha][0]
                print("Opção inválida!")
            except ValueError:
                print("Por favor, digite um número.")

    def selecionar_multiplas(self, opcoes, max_escolhas):
        escolhas = []
        while len(escolhas) < max_escolhas:
            self.mostrar_opcoes_detalhadas(opcoes)
            try:
                escolha = int(input(f"Escolha {len(escolhas)+1}/{max_escolhas}: "))
                if escolha in opcoes and opcoes[escolha][0] not in escolhas:
                    escolhas.append(opcoes[escolha][0])
                else:
                    print("Opção inválida ou já escolhida!")
            except ValueError:
                print("Por favor, digite um número.")
        return escolhas

    def jogador_vivo(self):
        return all([
            self.jogador['fome'] > 0,
            self.jogador['sede'] > 0,
            self.jogador['energia'] > 0,
            self.jogador['sanidade'] > 0
        ])

if __name__ == "__main__":
    jogo = Jogo()
    jogo.introducao()
    jogo.criar_personagem()
    jogo.criar_npcs()
    jogo.loop_principal()
