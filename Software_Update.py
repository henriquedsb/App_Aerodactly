import os
import fnmatch
import requests
import urllib.request
import tkinter as tk
from tkinter import messagebox

class Update():
    def __init__(self, usuario, repositorio, arquivo, extensao):
        self.usuario = usuario
        self.repositorio = repositorio
        self.arquivo = arquivo
        self.extensao = extensao

    def procurar_arquivo(self):
        resultado = []
        for raiz, diretorios, arquivos in os.walk('/'):
            for arquivo in fnmatch.filter(arquivos, f'{self.arquivo}.{self.extensao}'):
                resultado.append(os.path.join(raiz, arquivo))
        return resultado

    def obter_data_modificacao_local(self, caminho_arquivo):
        try:
            data_modificacao = os.path.getmtime(caminho_arquivo)
            return data_modificacao
        except FileNotFoundError:
            return None

    def obter_data_modificacao_github(self):
        url = f'https://api.github.com/repos/{self.usuario}/{self.repositorio}/commits/master'
        resposta = requests.get(url)
        if resposta.status_code == 200:
            commit = resposta.json()
            arquivo_no_commit = next((arquivo for arquivo in commit['files'] if arquivo['filename'] == f'{self.arquivo}.{self.extensao}'), None)
            if arquivo_no_commit:
                return arquivo_no_commit['raw_url'], arquivo_no_commit['patch']
        return None, None

    def baixar_arquivo(self, url, destino):
        urllib.request.urlretrieve(url, destino)

    def verificar_e_notificar_atualizacao(self):
        resultados = self.procurar_arquivo()

        if resultados:
            caminho_arquivo_local = resultados[0]
            data_modificacao_local = self.obter_data_modificacao_local(caminho_arquivo_local)
            url_arquivo_github, patch_arquivo_github = self.obter_data_modificacao_github()

            if data_modificacao_local and url_arquivo_github:
                if data_modificacao_local < patch_arquivo_github['new_file']['timestamp']:
                    resposta = messagebox.askyesno("Atualização Disponível", "Há uma nova atualização disponível. Deseja atualizar o arquivo?")
                    if resposta:
                        self.baixar_arquivo(url_arquivo_github, caminho_arquivo_local)
                        messagebox.showinfo("Atualização Concluída", f'Arquivo {self.arquivo}.{self.extensao} foi atualizado com sucesso!')
                        os.system(f'python {caminho_arquivo_local}')  # Executa o arquivo atualizado
                else:
                    messagebox.showinfo("Sem Atualizações", f'O arquivo local está mais atualizado do que o arquivo no GitHub.')
            else:
                messagebox.showwarning("Erro", f'Não foi possível obter informações sobre o arquivo no GitHub ou o arquivo local não existe.')
        else:
            messagebox.showinfo("Arquivo Não Encontrado", f'O arquivo {self.arquivo}.{self.extensao} não foi encontrado em nenhum diretório.')

def verificar_atualizacao():
        usuario = 'henriquedsb'
        repositorio = 'App_Aerodactly'
        arquivo = 'aerodactly'
        extensao = 'exe'
        update_checker = Update(usuario, repositorio, arquivo, extensao)
        update_checker.verificar_e_notificar_atualizacao()