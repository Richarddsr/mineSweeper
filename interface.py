import tkinter as tk
from tkinter import messagebox
import random

# Variável global para armazenar a instância de CampoMinado
campo = None

def credits():
    messagebox.showinfo("Créditos", "Jogo 100% criado por mim")

def start():
    global campo  # Faz referência à variável global
    # Cria uma nova janela (Toplevel) a partir da janela principal (root)
    janela_start = tk.Toplevel(root)
    janela_start.configure(bg="lightgreen")
    janela_start.title("MineSweeper!")
    janela_start.attributes("-fullscreen", True)

    label = tk.Label(janela_start, text="🔥💣MineSweeper💣🔥", font=("Cardinal", 16), bg="black", fg="Red")
    label.pack(pady=20)  # Empacota a label com um espaçamento de 20

    # Botão para sair do modo tela cheia
    def sair_tela_cheia():
        janela_start.attributes("-fullscreen", False)

    # Adiciona um botão para sair do modo tela cheia
    botao_sair = tk.Button(janela_start, text="Home", command=janela_start.destroy)
    botao_sair.pack(side="bottom", pady=20)  # Empacota o botão "Home" no fundo da tela

    # Instancia o jogo na janela criada e atribui à variável global
    campo = CampoMinado(janela_start)

class CampoMinado:
    def __init__(self, root, linhas=9, colunas=9, minas=10):
        self.root = root
        self.linhas = linhas
        self.colunas = colunas
        self.minas = minas
        self.matriz = [[None for _ in range(colunas)] for _ in range(linhas)]
        self.celulas = [[{"estado": "escondida", "valor": 0} for _ in range(colunas)] for _ in range(linhas)]
        self.setup()

    def setup(self):
        # Cria a grade 9x9 com os botões
        for i in range(self.linhas):
            # Cria um Frame para cada linha de botões
            frame = tk.Frame(self.root)
            frame.pack(pady=2)  # Empacota o Frame com um pequeno espaçamento vertical

            for j in range(self.colunas):
                # Cria os botões para a grade
                btn = tk.Button(frame, text="", width=4, height=2, command=lambda i=i, j=j: self.revelar(i, j))
                btn.pack(side="left", padx=2)  # Empacota os botões da linha com um pequeno espaçamento horizontal
                self.matriz[i][j] = btn  # Armazena o botão na matriz

                # Adiciona o evento para marcar a célula com bandeira
                btn.bind("<Button-3>", lambda event, i=i, j=j: self.marcar_bandeira(i, j))  # Clique com botão direito

        # Coloca as minas e calcula os números das células
        self.colocar_minas()
        self.calcular_minas_adjacentes()

    def colocar_minas(self):
        minas_colocadas = 0
        while minas_colocadas < self.minas:
            i = random.randint(0, self.linhas - 1)
            j = random.randint(0, self.colunas - 1)
            if self.celulas[i][j]["valor"] != "mina":  # Garante que não coloque a mina no mesmo lugar
                self.celulas[i][j]["valor"] = "mina"
                minas_colocadas += 1

    def calcular_minas_adjacentes(self):
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.celulas[i][j]["valor"] == "mina":
                    continue
                # Conta as minas adjacentes
                contagem = 0
                for x in range(i-1, i+2):
                    for y in range(j-1, j+2):
                        if 0 <= x < self.linhas and 0 <= y < self.colunas and (x != i or y != j):
                            if self.celulas[x][y]["valor"] == "mina":
                                contagem += 1
                self.celulas[i][j]["valor"] = contagem if contagem > 0 else ""

    def revelar(self, i, j):
        if self.celulas[i][j]["estado"] == "revelada":
            return  # Célula já revelada, não faz nada

        if self.celulas[i][j]["valor"] == "mina":
            self.matriz[i][j].config(text="M", bg="red")  # Mostra "M" para mina
            self.celulas[i][j]["estado"] = "revelada"
            self.game_over()  # Chama a função de "Game Over"
        else:
            self.matriz[i][j].config(text=self.celulas[i][j]["valor"], bg="lightgray")
            self.celulas[i][j]["estado"] = "revelada"
            self.matriz[i][j].config(state="disabled")
            if self.celulas[i][j]["valor"] == "":
                # Se a célula não tem minas adjacentes, revela as células vizinhas
                self.revelar_vizinhas(i, j)

    def revelar_vizinhas(self, i, j):
        for x in range(i-1, i+2):
            for y in range(j-1, j+2):
                if 0 <= x < self.linhas and 0 <= y < self.colunas:
                    if self.celulas[x][y]["estado"] == "escondida":
                        self.revelar(x, y)

    def game_over(self):
        messagebox.showinfo("Game Over", "Você perdeu! HAAHGSAHGASJDGASHJAHAHAHAHAHAH")
        self.reiniciar_jogo()

    def reiniciar_jogo(self):
        # Reinicia o jogo, limpando a grade e as células
        for i in range(self.linhas):
            for j in range(self.colunas):
                self.celulas[i][j] = {"estado": "escondida", "valor": 0}
                self.matriz[i][j].config(text="", state="normal", bg="SystemButtonFace")
        self.root.destroy()  # Destrói a janela do jogo após a derrota

    def marcar_bandeira(self, i, j):
        # Marca a célula com uma bandeira ao clicar com o botão direito
        if self.celulas[i][j]["estado"] == "escondida":
            if "🚩" in self.matriz[i][j]["text"]:
                self.matriz[i][j].config(text="", bg="SystemButtonFace")  # Remove a bandeira
            else:
                self.matriz[i][j].config(text="🚩", bg="yellow")  # Marca com bandeira
        elif self.celulas[i][j]["estado"] == "revelada":
            return  # Não faz nada se a célula já foi revelada


# Cria a janela principal
root = tk.Tk()
root.title("MineSweeper Home")
root.geometry("500x400")
root.configure(bg="orange")

label1 = tk.Label(root, text="MineSweeper Home 💣", font=("Cardinal", 16), bg="black", fg="Red")
label1.pack(pady=10, fill=tk.X)  # Centraliza a label

# Botão para abrir a nova janela e iniciar o jogo
start_button = tk.Button(root, text="Start", font=('Cardinal', 10, 'bold'), command=start)
start_button.pack(pady=10)  # Empacota o botão "Start" centralizado

credits_button = tk.Button(root, text="Credits", font=('Cardinal', 10, 'bold'), command=credits)
credits_button.pack(pady=10)  # Empacota o botão "Credits" centralizado

label2 = tk.Label(root, text="Version 1.0", font=("Cardinal", 13), bg="orange", fg="white")
label2.pack(side="bottom", pady=10)  # Posiciona o label de versão na parte inferior da janela

# Inicia o loop principal
root.mainloop()
