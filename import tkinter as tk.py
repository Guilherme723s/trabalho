import tkinter as tk
from tkinter import messagebox
import json
import os

# Classe Tarefa
class Tarefa:
    def __init__(self, titulo, status="Pendente"):
        self.titulo = titulo
        self.status = status

    def para_dict(self):
        return {"titulo": self.titulo, "status": self.status}

    def __str__(self):
        return f"{self.titulo} - {self.status}"

# Classe Gerenciador de Tarefas
class GerenciadorTarefas:
    def __init__(self, caminho_arquivo="tarefas.json"):
        self.caminho_arquivo = caminho_arquivo
        self.tarefas = self.carregar_tarefas()

    def carregar_tarefas(self):
        """Carregar tarefas do arquivo JSON"""
        if os.path.exists(self.caminho_arquivo):
            with open(self.caminho_arquivo, 'r') as arquivo:
                return [Tarefa(**tarefa) for tarefa in json.load(arquivo)]
        return []

    def salvar_tarefas(self):
        """Salvar tarefas no arquivo JSON"""
        with open(self.caminho_arquivo, 'w') as arquivo:
            json.dump([tarefa.para_dict() for tarefa in self.tarefas], arquivo, indent=4)

    def adicionar_tarefa(self, titulo, status="Pendente"):
        tarefa = Tarefa(titulo, status)
        self.tarefas.append(tarefa)
        self.salvar_tarefas()

    def atualizar_tarefa(self, titulo, novo_status):
        for tarefa in self.tarefas:
            if tarefa.titulo == titulo:
                tarefa.status = novo_status
                self.salvar_tarefas()
                return True
        return False

    def excluir_tarefa(self, titulo):
        self.tarefas = [tarefa for tarefa in self.tarefas if tarefa.titulo != titulo]
        self.salvar_tarefas()

    def listar_tarefas(self):
        return [str(tarefa) for tarefa in self.tarefas]

# Interface Gráfica com Tkinter
class GerenciadorTarefasGUI:
    def __init__(self, root, gerenciador_tarefas):
        self.root = root
        self.gerenciador_tarefas = gerenciador_tarefas
        self.root.title("Gerenciador de Tarefas")

        # Criar elementos da interface gráfica
        self.criar_widgets()

    def criar_widgets(self):
        # Rótulo do título da tarefa
        self.label_titulo = tk.Label(self.root, text="Título da Tarefa:")
        self.label_titulo.pack()

        # Campo de texto para o título
        self.entrada_titulo = tk.Entry(self.root)
        self.entrada_titulo.pack()

        # Rótulo do status da tarefa
        self.label_status = tk.Label(self.root, text="Status da Tarefa:")
        self.label_status.pack()

        # Menu suspenso para o status
        self.status_var = tk.StringVar(value="Pendente")
        self.menu_status = tk.OptionMenu(self.root, self.status_var, "Pendente", "Em Andamento", "Concluída")
        self.menu_status.pack()

        # Botão para adicionar tarefa
        self.botao_adicionar = tk.Button(self.root, text="Adicionar Tarefa", command=self.adicionar_tarefa)
        self.botao_adicionar.pack()

        # Botão para listar tarefas
        self.botao_listar = tk.Button(self.root, text="Listar Tarefas", command=self.listar_tarefas)
        self.botao_listar.pack()

        # Lista de tarefas
        self.lista_tarefas = tk.Listbox(self.root, width=50, height=10)
        self.lista_tarefas.pack()

        # Botão para atualizar o status da tarefa
        self.botao_atualizar = tk.Button(self.root, text="Atualizar Status da Tarefa", command=self.atualizar_tarefa)
        self.botao_atualizar.pack()

        # Botão para excluir tarefa
        self.botao_excluir = tk.Button(self.root, text="Excluir Tarefa", command=self.excluir_tarefa)
        self.botao_excluir.pack()

    def adicionar_tarefa(self):
        titulo = self.entrada_titulo.get()
        status = self.status_var.get()
        if titulo:
            self.gerenciador_tarefas.adicionar_tarefa(titulo, status)
            messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")
            self.entrada_titulo.delete(0, tk.END)
        else:
            messagebox.showwarning("Erro de Entrada", "Por favor, insira um título para a tarefa.")

    def listar_tarefas(self):
        # Limpar a lista de tarefas
        self.lista_tarefas.delete(0, tk.END)

        tarefas = self.gerenciador_tarefas.listar_tarefas()
        if tarefas:
            for tarefa in tarefas:
                self.lista_tarefas.insert(tk.END, tarefa)
        else:
            self.lista_tarefas.insert(tk.END, "Nenhuma tarefa disponível.")

    def atualizar_tarefa(self):
        indice_tarefa_selecionada = self.lista_tarefas.curselection()
        if indice_tarefa_selecionada:
            tarefa_str = self.lista_tarefas.get(indice_tarefa_selecionada)
            titulo_tarefa = tarefa_str.split(" - ")[0]
            novo_status = self.status_var.get()
            if self.gerenciador_tarefas.atualizar_tarefa(titulo_tarefa, novo_status):
                messagebox.showinfo("Sucesso", "Status da tarefa atualizado!")
                self.listar_tarefas()
            else:
                messagebox.showwarning("Erro de Atualização", "Tarefa não encontrada.")
        else:
            messagebox.showwarning("Erro de Seleção", "Por favor, selecione uma tarefa para atualizar.")

    def excluir_tarefa(self):
        indice_tarefa_selecionada = self.lista_tarefas.curselection()
        if indice_tarefa_selecionada:
            tarefa_str = self.lista_tarefas.get(indice_tarefa_selecionada)
            titulo_tarefa = tarefa_str.split(" - ")[0]
            self.gerenciador_tarefas.excluir_tarefa(titulo_tarefa)
            messagebox.showinfo("Sucesso", "Tarefa excluída!")
            self.listar_tarefas()
        else:
            messagebox.showwarning("Erro de Seleção", "Por favor, selecione uma tarefa para excluir.")

if __name__ == "__main__":
    # Inicializar o Gerenciador de Tarefas e a Interface Gráfica
    gerenciador_tarefas = GerenciadorTarefas()
    root = tk.Tk()
    app = GerenciadorTarefasGUI(root, gerenciador_tarefas)
    root.mainloop()
