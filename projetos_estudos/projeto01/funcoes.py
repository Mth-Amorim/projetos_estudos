from tinydb import TinyDB, Query
# aplicativo para controle de tareffas criar o crud 

# [ ] - Identificar o arquivo do banco 
# [ ] - Conectar no banco 
# [ ] - Criar as tabelas
# [ ] - CRUD - Creat 
# [ ] - CRUD - Read
# [ ] - CRUD - Update
# [ ] - CRUD - Delete


def conectar_banco(file_path='db.json'):
    """
    Função para conectar ao banco de dados TinyDB.
    Cria o banco se não existir.
    """
    return TinyDB(file_path)

def criar_tabela(db):
    """
    Função para criar uma tabela no banco de dados.
    """
    # No TinyDB, as tabelas são criadas automaticamente ao inserir dados.
    pass

def inserir_tarefa(db, registro):
    """
    Função para inserir um registro no banco de dados.
    """
    db.insert(registro)

def listar_tarefas(db):
    """
    Função para listar todas as tarefas no banco de dados.
    """
    return db.all()

def atualizar_tarefa(db, query, updates):
    """
    Função para atualizar uma tarefa no banco de dados.
    """
    db.update(updates, query)   

def remover_tarefa(db, query):
    """
    Função para remover uma tarefa do banco de dados.
    """
    db.remove(query)

