import tkinter as tk
from tkinter import messagebox
import random
import string


#aci e omuletu de la spanzurat
class AsciiArt:
    STADII = [
        "\n   +---+\n   |   |\n       |\n       |\n       |\n       |\n=========",
        "\n   +---+\n   |   |\n   O   |\n       |\n       |\n       |\n=========",
        "\n   +---+\n   |   |\n   O   |\n   |   |\n       |\n       |\n=========",
        "\n   +---+\n   |   |\n   O   |\n  /|   |\n       |\n       |\n=========",
        "\n   +---+\n   |   |\n   O   |\n  /|\\  |\n       |\n       |\n=========",
        "\n   +---+\n   |   |\n   O   |\n  /|\\  |\n  /    |\n       |\n=========",
        "\n   +---+\n   |   |\n   O   |\n  /|\\  |\n  / \\  |\n       |\n========="
    ]


class HangmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Spanzuratoare: Python101")
        self.root.geometry("600x820")  #rezolutie ecran
        self.root.configure(bg="#121213")

        #culori
        self.CULOARE_VERDE = "#538d4e"
        self.CULOARE_ROSU = "#e23636"
        self.CULOARE_GRI = "#3a3a3c"
        self.CULOARE_TEXT = "#ffffff"

        #cuvinte random
        self.lista_cuvinte = [
            "PROGRAMARE", "INTERFATA", "PYTHON", "TASTATURA", "ALGORITM",
            "SESIUNE", "RESTANTA", "EXAMEN", "LABORATOR", "PROIECT",
            "EROARE", "TERMINAL",
            "ABSENTE", "CAMIN", "ENERGIZANT", "SHAORMA",
            "VECTOR", "MATRICE", "POINTER", "STRUCTURA", "CLASA",
            "OBIECT", "VARIABILA", "FUNCTIE", "SINTAXA", "COMPILATOR",
            "SERVER", "RETEA", "LAPTOP", "PLICTISEALA", "CAFEA",
            "CAFEINA", "FACULTATE", "LICENTA", "DIPLOMA", "SEMESTRU",
            "MEMORIE", "PROCESOR", "MOUSE", "ECRAN", "CABLU",
            "INTERNET", "COD", "STUDENT", "LIBRARIE", "MODUL"
        ]

        #variabile folosite
        self.cuvant_secret = random.choice(self.lista_cuvinte)
        self.incercari_gresite = 0
        self.incercari_maxime = len(AsciiArt.STADII) - 1
        self.litere_ghicite = set()

        # contoare pt scor
        self.scor_victorii = 0
        self.scor_infrangeri = 0

        #butoane ecran

        # titlu
        self.lbl_titlu = tk.Label(root, text="SPÂNZURĂTOAREA", font=("Arial", 28, "bold"),
                                  bg="#121213", fg=self.CULOARE_VERDE)
        self.lbl_titlu.pack(pady=(20, 5))

        #scor
        self.lbl_scor = tk.Label(root, text=f"Trecute: {self.scor_victorii} | Pierdute: {self.scor_infrangeri}",
                                 font=("Arial", 12, "bold"), bg="#121213", fg="#aaaaaa")
        self.lbl_scor.pack(pady=(0, 10))

        #spanzuratoarea om(fara om momentan)
        self.lbl_ascii = tk.Label(root, text=AsciiArt.STADII[0], font=("Courier", 16, "bold"),
                                  bg="#121213", fg=self.CULOARE_TEXT, justify="left")
        self.lbl_ascii.pack(pady=5)

        #bara cuvantului
        self.frame_cuvant = tk.Frame(root, bg="#121213")
        self.frame_cuvant.pack(pady=10)

        self.etichete_litere = []
        self.genereaza_liniute()

        #iarasi da pentru tastatura
        self.frame_tastatura = tk.Frame(root, bg="#121213")
        self.frame_tastatura.pack(pady=15)

        self.creaza_tastatura()  #fct pt tastatura

        #bara buton restart si alt cuvant
        self.frame_controale = tk.Frame(root, bg="#121213")
        self.frame_controale.pack(pady=10)

        self.btn_restart = tk.Button(self.frame_controale, text="Alt cuvânt (Play Again)", font=("Arial", 12, "bold"),
                                     bg=self.CULOARE_GRI, fg=self.CULOARE_TEXT, command=self.reseteaza_joc)
        self.btn_restart.pack(side="left", padx=10)

        self.btn_exit = tk.Button(self.frame_controale, text="Exit", font=("Arial", 12, "bold"),
                                  bg=self.CULOARE_ROSU, fg=self.CULOARE_TEXT, command=self.root.quit)
        self.btn_exit.pack(side="left", padx=10)

        #nume eu si raf
        self.lbl_autori = tk.Label(root, text="Proiect realizat de:\nComanici Vlad Ștefan & Oprica Manta Rafael",
                                   font=("Arial", 10, "italic"), bg="#121213", fg=self.CULOARE_GRI, justify="right")
        self.lbl_autori.pack(side="bottom", anchor="e", padx=15, pady=15)

        #tastatura(sa mi ia tastatele)
        self.root.bind("<Key>", self.apasare_tastatura_fizica)

    def genereaza_liniute(self):
        """generam linii pt litere"""
        self.etichete_litere = []
        for _ in self.cuvant_secret:
            lbl = tk.Label(self.frame_cuvant, text="_", font=("Arial", 24, "bold"),
                           bg=self.CULOARE_GRI, fg=self.CULOARE_TEXT, width=2, height=1)
            lbl.pack(side="left", padx=5)
            self.etichete_litere.append(lbl)

    def creaza_tastatura(self):
        """punem litere peste bara de care am zis mai sus"""
        alfabet = string.ascii_uppercase
        rand = 0
        coloana = 0

        for litera in alfabet:
            #gandeste daca litera e in cuvant
            btn = tk.Button(self.frame_tastatura, text=litera, font=("Arial", 14, "bold"),
                            bg=self.CULOARE_GRI, fg=self.CULOARE_TEXT, width=4, height=2,
                            command=lambda l=litera: self.click_litera(l))
            btn.grid(row=rand, column=coloana, padx=3, pady=3)

            coloana += 1
            if coloana > 6:  #pozitionare
                coloana = 0
                rand += 1

        #butoanele de la tastatura salvate face lista
        self.butoane_tastatura = {btn['text']: btn for btn in self.frame_tastatura.winfo_children()}

    def apasare_tastatura_fizica(self, event):
        """fct sa mearga apasate butoanele"""
        litera = event.char.upper()  #totu caps lok

        #verificam daca e litera
        if litera in self.butoane_tastatura:
            buton = self.butoane_tastatura[litera]
            #verificam daca butonu a fost apasat
            if buton['state'] == "normal":
                self.click_litera(litera)

    def click_litera(self, litera):
        """aici merge si cu click apasat"""
        buton = self.butoane_tastatura[litera]
        buton.config(state="disabled")  #il face gri sa nu mai apesi pe el
        self.litere_ghicite.add(litera)

        if litera in self.cuvant_secret:
            # a nimerit o litera
            buton.config(bg=self.CULOARE_VERDE, disabledforeground=self.CULOARE_TEXT)
            self.actualizeaza_cuvant()
            self.verifica_victorie()
        else:
            # n-a nimerit
            buton.config(bg=self.CULOARE_ROSU, disabledforeground=self.CULOARE_TEXT)
            self.incercari_gresite += 1
            self.lbl_ascii.config(text=AsciiArt.STADII[self.incercari_gresite])
            self.verifica_infrangere()

    def actualizeaza_cuvant(self):
        """schimba liniutele "_" cu litera gasita, daca o gaseste"""
        for i, litera in enumerate(self.cuvant_secret):
            if litera in self.litere_ghicite:
                self.etichete_litere[i].config(text=litera, bg=self.CULOARE_VERDE)

    def blocheaza_tastatura(self):
        """ingheata tot gridu cand se termina runda"""
        for btn in self.butoane_tastatura.values():
            btn.config(state="disabled")

    def reseteaza_joc(self):
        """butonul de restart"""
        # alegem alt cuvant
        self.cuvant_secret = random.choice(self.lista_cuvinte)
        self.incercari_gresite = 0
        self.litere_ghicite.clear()

        # resetam omuletu
        self.lbl_ascii.config(text=AsciiArt.STADII[0])

        # distrugem liniutele vechi de pe ecran ca altfel se pun unele langa altele
        for widget in self.frame_cuvant.winfo_children():
            widget.destroy()

        # facem linii noi
        self.genereaza_liniute()

        # de inghetam butoanele si le facem iar gri
        for btn in self.butoane_tastatura.values():
            btn.config(state="normal", bg=self.CULOARE_GRI, disabledforeground=self.CULOARE_TEXT)

    def verifica_victorie(self):
        # daca a castigat iti da mesaj
        if all(litera in self.litere_ghicite for litera in self.cuvant_secret):
            self.scor_victorii += 1
            self.lbl_scor.config(text=f"Trecute: {self.scor_victorii} | Pierdute: {self.scor_infrangeri}")
            self.blocheaza_tastatura()
            messagebox.showinfo("Gata",
                                f"Ai trecut de cuvantul: {self.cuvant_secret}\nDă pe 'Alt cuvânt' sa continui.")

    def verifica_infrangere(self):
        # daca te-ai spanzurat iti zice cuvantu
        if self.incercari_gresite >= self.incercari_maxime:
            self.scor_infrangeri += 1
            self.lbl_scor.config(text=f"Trecute: {self.scor_victorii} | Pierdute: {self.scor_infrangeri}")
            self.blocheaza_tastatura()
            messagebox.showerror("Rip", f"Ai pierdut.\nCuvântul era: {self.cuvant_secret}\nMai incearcă.")


#aici imi da run la tot ce e mai sus
if __name__ == "__main__":
    fereastra_principala = tk.Tk()  #apare fereastra
    aplicatie = HangmanGUI(fereastra_principala)
    fereastra_principala.mainloop()  # un fel de while True de la tkinter