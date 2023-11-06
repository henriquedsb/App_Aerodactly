import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from Software_Banco_de_dados import Banco_de_dados
from Software_Backend import Backend

class App(ctk.CTk, Banco_de_dados, Backend):
    def __init__(self):
        super().__init__()
        self.configurar_tela()
        self.usuario_atual = None
        self.tela_de_login()

    def configurar_tela(self):
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')
        self.title('Aerodactyl UFG Aerodesign')
        self.geometry('770x500')
        self.resizable(True, True)

    def tela_de_login(self):
        self.limpar_tela()
        self.frame_login = ctk.CTkFrame(self, corner_radius=10, border_width=1)
        self.frame_login.pack(expand=True)

        self.texto_login = ctk.CTkLabel(self.frame_login, text='Login')
        self.texto_login.pack(padx=10, pady=10)

        self.email_login = ctk.CTkEntry(self.frame_login, placeholder_text='Seu e-mail')
        self.email_login.pack(padx=10, pady= 10)

        self.senha_login = ctk.CTkEntry(self.frame_login, placeholder_text='Sua senha', show='*')
        self.senha_login.pack(padx=10, pady= 10)

        self.button_login = ctk.CTkButton(self.frame_login, text='Login', command=self.verificar_login)
        self.button_login.pack(padx=5, pady=10, side=ctk.LEFT)

        self.button_cadastrar = ctk.CTkButton(self.frame_login, text='Cadastrar', command=self.tela_de_cadastro)
        self.button_cadastrar.pack(padx=5, pady=10, side=ctk.RIGHT)

    def tela_de_cadastro(self):
        self.limpar_tela()
        self.frame_cadastro = ctk.CTkFrame(self, corner_radius=10, border_width=1)
        self.frame_cadastro.pack(expand=True, padx=10, pady=10)

        self.texto_cadastro = ctk.CTkLabel(self.frame_cadastro, text='Cadastrar')
        self.texto_cadastro .pack(padx=5, pady=5)

        self.texto_nome = ctk.CTkLabel(self.frame_cadastro, text='Insira seu nome completo')
        self.texto_nome .pack(padx=5, pady=5)

        self.nome_cadastro = ctk.CTkEntry(self.frame_cadastro)
        self.nome_cadastro.pack(padx=5, pady=5)

        self.texto_email = ctk.CTkLabel(self.frame_cadastro, text='Insira seu endereço de e-mail')
        self.texto_email .pack(padx=5, pady=5)

        self.email_cadastro = ctk.CTkEntry(self.frame_cadastro, placeholder_text='exemplo@gmail.com')
        self.email_cadastro.pack(padx=5, pady=5)

        self.texto_senha = ctk.CTkLabel(self.frame_cadastro, text='Insira sua senha')
        self.texto_senha .pack(padx=5, pady=5)

        self.senha_cadastro = ctk.CTkEntry(self.frame_cadastro, placeholder_text='Senha', show='*')
        self.senha_cadastro.pack(padx=5, pady=5)

        self.texto_confirmar_senha = ctk.CTkLabel(self.frame_cadastro, text='Confirme sua senha')
        self.texto_confirmar_senha.pack(padx=5, pady=5)

        self.confirmar_senha_cadastro = ctk.CTkEntry(self.frame_cadastro, placeholder_text='Confirme a senha', show='*')
        self.confirmar_senha_cadastro.pack(padx=5, pady=5)

        self.texto_telefone = ctk.CTkLabel(self.frame_cadastro, text='Insira seu telefone')
        self.texto_telefone.pack(padx=5, pady=5)

        self.telefone_cadastro= ctk.CTkEntry(self.frame_cadastro, placeholder_text='(DDD) 99999-9999')
        self.telefone_cadastro.pack(padx=5, pady=5)

        self.button_cadastrar = ctk.CTkButton(self.frame_cadastro, text='Cadastrar', command=self.cadastrar_usuario)
        self.button_cadastrar.pack(padx=5, pady=10, side=ctk.LEFT)

        self.button_cadastro_voltar = ctk.CTkButton(self.frame_cadastro,text='Voltar', command=self.tela_de_login)
        self.button_cadastro_voltar.pack(padx=5, pady=10, side=ctk.RIGHT)

    def mainpage(self):
        self.limpar_tela()

        self.frame_barra = ctk.CTkFrame(self)
        self.frame_barra.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.1)

        self.frame_01 = ctk.CTkFrame(self)
        self.frame_01.place(relx=0.02, rely=0.15, relwidth=0.96, relheight=0.82)

        self.button_01 = ctk.CTkButton(self.frame_barra, text='Calculadora Atmosfera',command=self.calculadora)
        self.button_01.pack(side=ctk.LEFT, padx=5, pady=5)

        self.button_02 = ctk.CTkButton(self.frame_barra, text='Recursos da equipe')
        self.button_02.pack(side=ctk.LEFT, padx=5, pady=5)

        self.button_03 = ctk.CTkButton(self.frame_barra, text='Membros', command=self.membros)
        self.button_03.pack(side=ctk.LEFT, padx=5, pady=5)

        self.button_04 = ctk.CTkButton(self.frame_barra, text='Logout', command=self.logout)
        self.button_04.pack(side=ctk.LEFT, padx=5, pady=5)

        self.texto_01_mainpage = ctk.CTkLabel(self.frame_01, text=f'Bem vindo, {self.usuario_atual}')
        self.texto_01_mainpage.pack(padx=10, pady=10)

    def calculadora(self):
        self.limpar_tela()

        self.texto_01= ctk.CTkLabel(self, text='Insira a Altitude (metros)')
        self.texto_01.pack(padx=10, pady=10)

        self.entrada_altitude = ctk.CTkEntry(self)
        self.entrada_altitude.pack(padx=10, pady=10)

        self.botao_calcular = ctk.CTkButton(self, text='Calcular', command=self.calcular_atmosfera)
        self.botao_calcular.pack(padx=10, pady=10)

        self.botao_voltar = ctk.CTkButton(self, text='Retornar', command=self.mainpage)
        self.botao_voltar.pack(padx=10, pady=10)

        self.texto_resultado = ctk.StringVar()
        self.texto_02 = ctk.CTkLabel(self, textvariable=self.texto_resultado)
        self.texto_02.pack(padx=10, pady=10)

    def mainpage_Admin(self):
        self.limpar_tela()
        self.mainpage()

        self.botao_admin = ctk.CTkButton(self.frame_barra, text='Admin')
        self.botao_admin.pack(padx=10, pady=10)

    def membros(self):
        self.limpar_tela()
        self.frame_membros = ctk.CTkFrame(self, corner_radius=10, border_width=1)
        self.frame_membros.pack(expand=True)

        self.tree = ttk.Treeview(self.frame_membros, columns=("nome", "email", "telefone", "cargo"), show="headings")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("email", text="E-mail")
        self.tree.heading("telefone", text="Telefone")
        self.tree.heading("cargo", text="Cargo")

        self.tree.column("nome", width=200)
        self.tree.column("email", width=200)
        self.tree.column("telefone", width=200)
        self.tree.column("cargo", width=200)

        for row in self.buscar_membros():
            self.tree.insert("", "end", values=row)

        self.tree.pack(padx=10, pady=10)

        self.botao_voltar = ctk.CTkButton(self, text='Retornar', command=self.mainpage)
        self.botao_voltar.pack(padx=10, pady=10)

    def logout(self):
        self.limpar_tela()
        self.tela_de_login()

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == '__main__':
    app = App()
    app.mainloop()
