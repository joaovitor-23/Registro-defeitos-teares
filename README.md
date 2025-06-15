📊 Sistema de Controle de Teares

Um sistema web completo para registro e gerenciamento de dados de produção têxtil, com foco no controle de defeitos em teares.

✨ Funcionalidades

Cadastro completo de ocorrências em teares

- Visualização organizada dos registros
- Edição fácil de informações existentes
- Exportação de dados para Excel e PDF
- Limpeza segura do banco de dados
- Design responsivo para qualquer dispositivo

📦 Dependências

- Flask
- Flask-SQLAlchemy
- Pandas
- XlsxWriter
- WeasyPrint

📋 Estrutura do Projeto

Registro-defeitos-teares/
├── app.py                # Aplicação principal
├── requirements.txt      # Dependências
├── dados.db              # Banco de dados (criado automaticamente)
├── static/
│   └── styles.css        # Estilos personalizados
└── templates/
    ├── base.html         # Template base
    ├── index.html        # Página inicial (cadastro)
    ├── registros.html    # Listagem de registros
    ├── editar.html       # Edição de registros
    └── exportar_pdf.html # Template para PDF

🛠️ Tecnologias Utilizadas

![python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![flask](https://img.shields.io/badge/Flask-2.0+-lightgrey?logo=flask)
![bootstrap](https://img.shields.io/badge/Bootstrap-5.0+-purple?logo=bootstrap)
![sqlite](https://img.shields.io/badge/SQLite-3.0+-green?logo=sqlite)

