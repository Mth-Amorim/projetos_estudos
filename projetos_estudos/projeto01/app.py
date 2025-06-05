# todo_app.py
import customtkinter as ctk
from projetos_estudos.projeto01.funcoes import GerenciadorTarefas  
from tinydb import TinyDB, Query
from tkinter import messagebox
from uuid import uuid4


GERENCIADOR = GerenciadorTarefas()

class EntradaTarefaFrame(ctk.CTkFrame):
    def __init__(self, master, adicionar_callback):
        super().__init__(master)

        self.adicionar_callback = adicionar_callback
        self.columnconfigure(0, weight=1)

        self.entrada = ctk.CTkEntry(self, placeholder_text="Nova tarefa")
        self.entrada.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="ew")

        self.botao_add = ctk.CTkButton(self, text="+", width=40, command=self.adicionar_tarefa)
        self.botao_add.grid(row=0, column=1, pady=5)

    def adicionar_tarefa(self):
        nome = self.entrada.get().strip()
        if nome:
            self.adicionar_callback(nome)
            self.entrada.delete(0, "end")
        else:
            messagebox.showwarning("Aviso", "Digite uma tarefa válida.")


class FiltrosTarefa(ctk.CTkFrame):
    def __init__(self, master, callback_reload):
        super().__init__(master)

        self.callback_reload = callback_reload

        self.filtro_concluido = ctk.CTkCheckBox(self, text="Concluído", command=self.callback_reload)
        self.filtro_concluido.grid(row=0, column=0, padx=5, sticky="w")

        self.filtro_pendente = ctk.CTkCheckBox(self, text="Pendente", command=self.callback_reload)
        self.filtro_pendente.grid(row=0, column=1, padx=5, sticky="w")

    def is_concluido_ativo(self):
        return self.filtro_concluido.get()

    def is_pendente_ativo(self):
        return self.filtro_pendente.get()


class TarefaFrame(ctk.CTkFrame):
    def __init__(self, master, tarefa, db, callback_reload):
        super().__init__(master)

        self.tarefa = tarefa
        self.db = db
        self.callback_reload = callback_reload

        self.columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self, text=tarefa["nome"], anchor="w")
        self.label.grid(row=0, column=0, padx=10, sticky="ew")

        self.select_status = ctk.CTkOptionMenu(self, values=["Pendente", "Concluído"], command=self.atualizar_status)
        self.select_status.set(tarefa["status"])
        self.select_status.grid(row=0, column=1, padx=5)

        self.botao_excluir = ctk.CTkButton(self, text="🗑️", width=40, command=self.excluir)
        self.botao_excluir.grid(row=0, column=2, padx=5)

    def atualizar_status(self, novo_status):
        GERENCIADOR.atualizar_status(self.tarefa["id"], novo_status)
        self.callback_reload()

    def excluir(self):
        GERENCIADOR.remover(self.tarefa["id"])
        self.callback_reload()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gerenciador de Tarefas")
        self.geometry("500x600")
        self.resizable(False, False)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # Frame de entrada
        self.frame_input = EntradaTarefaFrame(self, self.adicionar_tarefa)
        self.frame_input.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.columnconfigure(0, weight=1)

        # Frame de filtros
        self.frame_filtros = FiltrosTarefa(self, self.recarregar_tarefas)
        self.frame_filtros.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Frame scrollable para tarefas
        self.frame_lista = ctk.CTkScrollableFrame(self)
        self.frame_lista.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.frame_lista.columnconfigure(0, weight=1)

        self.recarregar_tarefas()


    def adicionar_tarefa(self, nome):
        GERENCIADOR.adicionar(nome)
        self.recarregar_tarefas()

    def recarregar_tarefas(self):
        # Limpar tarefas anteriores
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        tarefas = GERENCIADOR.buscar_todas()
        if self.frame_filtros.is_concluido_ativo() and self.frame_filtros.is_pendente_ativo():
            pass
        elif self.frame_filtros.is_concluido_ativo():
            tarefas = [t for t in tarefas if t["status"] == "Concluído"]
        elif self.frame_filtros.is_pendente_ativo():
            tarefas = [t for t in tarefas if t["status"] == "Pendente"]

        for i, tarefa in enumerate(tarefas):
            tarefa_frame = TarefaFrame(self.frame_lista, tarefa, GERENCIADOR.db, self.recarregar_tarefas)
            tarefa_frame.grid(row=i, column=0, pady=5, sticky="ew")


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    App().mainloop()
