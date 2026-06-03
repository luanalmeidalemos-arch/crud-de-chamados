# 🎫 Sistema de Chamados Técnicos — API REST

API REST completa para gerenciamento de chamados técnicos, desenvolvida com Python, Flask e MySQL.

## 📌 Sobre o Projeto

Sistema backend que permite abrir, acompanhar e resolver chamados técnicos por setor. Desenvolvido como projeto prático para aplicar conceitos de desenvolvimento back-end, modelagem de banco de dados relacional e boas práticas de API REST.

## ✨ Funcionalidades

- ✅ Cadastro e listagem de usuários
- ✅ Cadastro e listagem de setores
- ✅ Abertura de chamados com prioridade (alta, média, baixa)
- ✅ Atualização de status (aberto, em andamento, concluído)
- ✅ Listagem de chamados ordenada por prioridade
- ✅ Exclusão de chamados
- ✅ Inicialização automática do banco de dados

## 🛠️ Tecnologias

- Python 3
- Flask
- MySQL
- mysql-connector-python
- python-dotenv

## 📁 Estrutura

crud-de-chamados/
├── app.py            # Rotas e lógica principal
├── config.py         # Configurações do banco
├── menu.py           # Menu CLI
├── .env.example      # Variáveis de ambiente necessárias
├── requirements.txt  # Dependências
└── .gitignore

## 🚀 Como Rodar

### 1. Clone o repositório
```bash
git clone https://github.com/luanalmeidalemos-arch/crud-de-chamados.git
cd crud-de-chamados
```

### 2. Crie o ambiente virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
```bash
cp .env.example .env
```
Edite o `.env` com suas credenciais do MySQL.

### 5. Rode a aplicação
```bash
python app.py
```

O banco de dados e as tabelas são criados automaticamente na primeira execução.

## endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | /usuarios | Lista todos os usuários |
| POST | /usuarios | Cria um usuário |
| GET | /setores | Lista todos os setores |
| POST | /setores | Cria um setor |
| GET | /chamados | Lista chamados por prioridade |
| POST | /chamados | Abre um chamado |
| PUT | /chamados/:id | Atualiza status ou prioridade |
| DELETE | /chamados/:id | Remove um chamado |

## 👨‍💻 Autor

**Luan Lemos**
Estudante de ADS — Universidade Veiga de Almeida
[LinkedIn](https://linkedin.com/in/devluanlemos) • [GitHub](https://github.com/luanalmeidalemos-arch)