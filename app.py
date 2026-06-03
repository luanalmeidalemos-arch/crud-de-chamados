from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
from config import Config
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

STATUS_VALIDOS = ['aberto', 'em_andamento', 'concluido']
PRIORIDADES_VALIDAS = ['alta', 'media', 'baixa']


def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados MySQL"""
    try:
        connection = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB'],
            port=app.config['MYSQL_PORT']
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None


def init_db():
    """Inicializa o banco de dados e cria as tabelas"""
    connection = None
    cursor = None

    try:
        # Conecta sem escolher DB
        connection = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            port=app.config['MYSQL_PORT']
        )
        cursor = connection.cursor()

        # Cria DB
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {app.config['MYSQL_DB']}")
        cursor.execute(f"USE {app.config['MYSQL_DB']}")

        # Cria tabela de usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL
            )
        """)

        # Cria tabela de setores
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS setores (
                id_setor INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) UNIQUE NOT NULL
            )
        """)

        # Cria tabela de chamados
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chamados (
                id_chamado INT AUTO_INCREMENT PRIMARY KEY,
                titulo VARCHAR(100) NOT NULL,
                descricao VARCHAR(255),
                id_usuario INT NOT NULL,
                id_setor INT NOT NULL,
                prioridade ENUM('alta', 'media', 'baixa') NOT NULL,
                status ENUM('aberto', 'em_andamento', 'concluido') NOT NULL DEFAULT 'aberto',
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
                FOREIGN KEY (id_setor) REFERENCES setores(id_setor)
            )
        """)

        connection.commit()
        print("Banco de dados e tabelas prontos!")

    except Error as e:
        print(f"Erro na inicialização: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ---------- ROTAS ----------

@app.route('/')
def home():
    return jsonify({
        'mensagem': 'Bem vindo(a) ao nosso sistema de Chamado Técnico',
        'status': 'Servidor Online'
    })


# ----- USUARIOS -----
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.get_json()
    if not dados or 'nome' not in dados or 'email' not in dados:
        return jsonify({'erro': 'nome e email são obrigatórios'}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({'erro': 'Falha na conexão'}), 500

    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email) VALUES (%s, %s)",
            (dados['nome'], dados['email'])
        )
        connection.commit()
        return jsonify({'mensagem': 'Usuário criado', 'id_usuario': cursor.lastrowid}), 201
    except Error as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/usuarios')
def listar_usuarios():
    connection = get_db_connection()
    if not connection:
        return jsonify({'erro': 'Falha na conexão'}), 500
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")
        return jsonify(cursor.fetchall()), 200
    finally:
        cursor.close()
        connection.close()


# ----- SETORES -----
@app.route('/setores', methods=['POST'])
def criar_setor():
    dados = request.get_json()
    if not dados or 'nome' not in dados:
        return jsonify({'erro': 'nome é obrigatório'}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({'erro': 'Falha na conexão'}), 500
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO setores (nome) VALUES (%s)", (dados['nome'],))
        connection.commit()
        return jsonify({'mensagem': 'Setor criado', 'id_setor': cursor.lastrowid}), 201
    except Error as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/setores')
def listar_setores():
    connection = get_db_connection()
    if not connection:
        return jsonify({'erro': 'Falha na conexão'}), 500
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM setores")
        return jsonify(cursor.fetchall()), 200
    finally:
        cursor.close()
        connection.close()


# ----- CHAMADOS -----
@app.route('/chamados')
def listar_chamados():
    connection = get_db_connection()
    if not connection:
        return jsonify({'erro': 'Falha na conexão'}), 500
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.id_chamado, c.titulo, c.descricao, c.prioridade, c.status, c.criado_em,
                   u.nome AS solicitante, s.nome AS setor
            FROM chamados c
            JOIN usuarios u ON c.id_usuario = u.id_usuario
            JOIN setores s ON c.id_setor = s.id_setor
            ORDER BY FIELD(c.prioridade, 'alta', 'media', 'baixa')
        """)
        return jsonify(cursor.fetchall()), 200
    finally:
        cursor.close()
        connection.close()


@app.route('/chamados', methods=['POST'])
def criar_chamado():
    dados = request.get_json()
    if not dados or 'titulo' not in dados or 'id_usuario' not in dados or 'id_setor' not in dados or 'prioridade' not in dados:
        return jsonify({'erro': 'titulo, id_usuario, id_setor e prioridade são obrigatórios'}), 400

    if dados['prioridade'] not in PRIORIDADES_VALIDAS:
        return jsonify({'erro': 'Prioridade inválida'}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({'erro': 'Falha na conexão'}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO chamados (titulo, descricao, id_usuario, id_setor, prioridade)
            VALUES (%s, %s, %s, %s, %s)
        """, (dados['titulo'], dados.get('descricao'), dados['id_usuario'], dados['id_setor'], dados['prioridade']))
        connection.commit()
        return jsonify({'mensagem': 'Chamado criado', 'id_chamado': cursor.lastrowid}), 201
    except Error as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/chamados/<int:id>', methods=['PUT'])
def atualizar_chamado(id):
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Nenhum dado enviado'}), 400

    if 'status' in dados and dados['status'] not in STATUS_VALIDOS:
        return jsonify({'erro': 'Status inválido'}), 400
    if 'prioridade' in dados and dados['prioridade'] not in PRIORIDADES_VALIDAS:
        return jsonify({'erro': 'Prioridade inválida'}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({'erro': 'Falha na conexão'}), 500

    try:
        cursor = connection.cursor()
        campos = []
        valores = []

        if 'status' in dados:
            campos.append("status = %s")
            valores.append(dados['status'])
        if 'prioridade' in dados:
            campos.append("prioridade = %s")
            valores.append(dados['prioridade'])
        if not campos:
            return jsonify({'erro': 'Nenhum campo válido para atualizar'}), 400

        valores.append(id)
        query = f"UPDATE chamados SET {', '.join(campos)} WHERE id_chamado = %s"
        cursor.execute(query, tuple(valores))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({'erro': 'Chamado não encontrado'}), 404

        return jsonify({'mensagem': 'Chamado atualizado com sucesso'}), 200
    finally:
        cursor.close()
        connection.close()


@app.route('/chamados/<int:id>', methods=['DELETE'])
def deletar_chamado(id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'erro': 'Falha na conexão'}), 500
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM chamados WHERE id_chamado = %s", (id,))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'erro': 'Chamado não encontrado'}), 404
        return jsonify({'mensagem': 'Chamado removido'}), 200
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    init_db()
    app.run(debug=True)

