from tinydb import TinyDB, Query
from uuid import uuid4
import os
# aplicativo para controle de tareffas criar o crud 

# [ ] - Identificar o arquivo do banco 
# [ ] - Conectar no banco 
# [ ] - Criar as tabelas
# [ ] - CRUD - Creat 
# [ ] - CRUD - Read
# [ ] - CRUD - Update
# [ ] - CRUD - Delete

BASE_DIR = os.path.dirname(__file__)
FILE_DB = os.path.join(BASE_DIR, "tarefas.json")

class GerenciadorTarefas:
    def __init__(self, caminho_db=FILE_DB):
        self.db = TinyDB(caminho_db)
        self.tabela = self.db.table("tarefas")

    def adicionar(self, nome):
        nova_tarefa = {
            "id": str(uuid4()),
            "nome": nome,
            "status": "Pendente"
        }
        self.tabela.insert(nova_tarefa)

    def remover(self, id_tarefa):
        Tarefa = Query()
        self.tabela.remove(Tarefa.id == id_tarefa)

    def atualizar_status(self, id_tarefa, novo_status):
        Tarefa = Query()
        self.tabela.update({"status": novo_status}, Tarefa.id == id_tarefa)

    def buscar_todas(self):
        return self.tabela.all()


