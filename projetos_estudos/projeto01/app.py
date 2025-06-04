# todo_app.py
import customtkinter
import customtkinter as ctk
from tinydb import TinyDB, Query
from tkinter import messagebox

ARQUIVO_DB = "tarefas.json"      # arquivo onde o TinyDB grava os dados

class ListaTarefas(ctk.CTkFrame):
    """Frame que exibe a lista; recebe o TinyDB injetado pelo App."""
    def __init__(self, master, db: TinyDB):
        super().__init__(master)
        self.db = db

        self.label = ctk.CTkLabel(self, text="Lista de Tarefas")
        self.label.pack(pady=(10, 4))

        # Listbox moderno do CustomTkinter (>= 5.x).  Para versões 4.x use ctk.CTkTextbox.
        self.listbox = customtkinter.CTkTextbox(self, width=280, height=230)
        self.listbox.configure(state="disabled")


        self.atualizar()           # carrega tarefas quando o frame nasce

    def atualizar(self):
        """Recarrega a lista a partir do banco."""
        self.listbox.delete(0, ctk.END)
        for doc in self.db.table("tarefas").all():
            self.listbox.insert(ctk.END, f"- {doc['nome']}")


class MenuPrincipal(ctk.CTkFrame):
    """Frame com o formulário para adicionar tarefa."""
    def __init__(self, master, on_add_callback):
        super().__init__(master)

        self.label = ctk.CTkLabel(self, text="Nova tarefa")
        self.entrada = ctk.CTkEntry(self, width=250, placeholder_text="Digite a tarefa…")
        self.botao_add = ctk.CTkButton(self, text="Adicionar", command=self._clicou_adicionar)

        self.entrada.grid(row=0, column=0, padx=10, pady=10)
        self.botao_add.grid(row=0, column=1, padx=10, pady=10)
        # função fornecida pelo App que realmente grava no banco
        self.on_add = on_add_callback

    def _clicou_adicionar(self):
        tarefa = self.entrada.get().strip()
        if not tarefa:
            messagebox.showwarning("Aviso", "Digite uma tarefa válida!")
            return
        self.on_add(tarefa)          # grava no banco e atualiza lista
        self.entrada.delete(0, ctk.END)


class App(ctk.CTk):
    """Janela principal; coordena banco, frames e callbacks."""
    def __init__(self):
        super().__init__()

        # ---------- janela ----------
        self.title("Gerenciador de Tarefas")
        self.geometry("450x450")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        # ---------- banco ----------
        self.db = TinyDB(ARQUIVO_DB)
        self.tabela = self.db.table("tarefas")

        # ---------- frames ----------
        self.menu_principal = MenuPrincipal(self, self.adicionar_tarefa)
        self.menu_principal.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.lista_tarefas = ListaTarefas(self, self.db)
        self.lista_tarefas.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    # ---------- callbacks ----------
    def adicionar_tarefa(self, nome: str):
        """Insere no TinyDB e avisa o frame da lista para recarregar."""
        self.tabela.insert({"nome": nome})
        self.lista_tarefas.atualizar()


if __name__ == "__main__":
    # tema escuro / claro; mude se quiser
    ctk.set_appearance_mode("dark")            # "light" ou "dark"
    ctk.set_default_color_theme("blue")        # "blue", "dark-blue", "green"...
    App().mainloop()
