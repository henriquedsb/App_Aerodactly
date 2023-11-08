import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import re
import phonenumbers

class Banco_de_dados():
    def conectar_banco(self):
        try:
            self.conexao = mysql.connector.connect(
                host='aws.connect.psdb.cloud',
                user='*******',
                password ='********',
                database='database',
            )
            self.cursor = self.conexao.cursor()
        except:
            messagebox.showerror('Erro','Conecte há uma rede de internet!')

    def desconectar_banco(self):
        self.conexao.close()

    def cadastrar_usuario(self):
        self.tipo_usuario = 'Membro'
        self.nome = self.nome_cadastro.get()
        self.email= self.email_cadastro.get()
        self.senha = self.senha_cadastro.get()
        self.confirmar_senha = self.confirmar_senha_cadastro.get()
        self.telefone = self.telefone_cadastro.get()
        self.telefone_formatado = self.validar_telefone(self.telefone)
        padrao_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        self.conectar_banco()
        inserir = "INSERT INTO usuarios (nome, email, senha, telefone, tipo) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(inserir,(self.nome,self.email,self.senha,self.telefone_formatado,self.tipo_usuario))
        
        try:
            if self.nome == '' or self.email =='' or self.senha == '' or self.confirmar_senha == '' or self.telefone == '':
                messagebox.showerror('Erro de Cadastro', 'Por favor, preencha todos os campos!')
            
            elif self.telefone_formatado == False:
                messagebox.showerror("Erro de Cadastro", "Número de telefone inválido. Por favor, insira um número válido.")
            
            elif not re.match(padrao_email, self.email):
                messagebox.showerror("Erro de Cadastro", "E-mail inválido. Por favor, insira um e-mail válido.")

            elif len(self.senha) < 4:
                messagebox.showerror("Erro de Cadastro", "Senha deve conter mais de 4 caracteres")
            
            elif self.senha != self.confirmar_senha:
                messagebox.showerror("Erro de Cadastro", "As senhas não são iguais. Tente novamente.")
        
            else:
                self.conexao.commit()
                messagebox.showinfo("Cadastro", "Cadastro realizado com sucesso!")
                self.tela_de_login()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar: {str(e)}")

        finally:
            self.desconectar_banco()
    
    def validar_telefone(self, telefone):
        try:
            numero_telefone = phonenumbers.parse(telefone)
            if phonenumbers.is_valid_number(numero_telefone):
                telefone_formatado = phonenumbers.format_number(numero_telefone, phonenumbers.PhoneNumberFormat.NATIONAL)
                return telefone_formatado
            else:
                return False  
        except phonenumbers.NumberParseException:
            return False
        
    def verificar_login(self):
        self.email = self.email_login.get()
        self.senha = self.senha_login.get()
        self.tipo = None

        self.conectar_banco()
        verificar = "SELECT * FROM usuarios WHERE email = %s AND senha = %s"
        self.cursor.execute(verificar, (self.email, self.senha))
        user_data = self.cursor.fetchone()
        self.desconectar_banco()

        if user_data:
            self.usuario_atual = user_data[1]
            self.tipo_usuario = user_data[5]
            if user_data[5] == 'Admin':
                self.mainpage_Admin()
            else:
                self.mainpage()
        else:
            messagebox.showerror("Erro de Login", "Credenciais inválidas")

    def autenticacao_usuario(self):
        self.usuario_atual
        self.tipo_usuario
        if self.tipo_usuario == 'Admin':
            self.mainpage_Admin()
        else:
            self.mainpage()
        
    def atualizar_membro(self):
        pass

    def buscar_membros(self):
        self.conectar_banco()
        buscar_membros = "SELECT nome,email,telefone,cargo FROM usuarios"
        self.cursor.execute(buscar_membros)
        membros= self.cursor.fetchall()
        self.desconectar_banco()

        return membros
