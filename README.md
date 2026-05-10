# 🔐 FaceID Security - Sistema de Reconhecimento Facial

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)

Projeto acadêmico focado em segurança biométrica e visão computacional. Trata-se de uma aplicação web capaz de gerenciar usuários e realizar reconhecimento facial em tempo real com alta precisão, utilizando processamento otimizado para navegadores e infraestrutura moderna em contêineres Docker.

## ✨ Funcionalidades Implementadas
* **Autenticação Administrativa:** Sistema de login seguro com rotas protegidas para garantir que apenas administradores possam cadastrar ou listar pessoas.
* **Gestão de Usuários:** Cadastro completo com validação biométrica preventiva (impede o cadastro de fotos sem rostos detectáveis).
* **Reconhecimento Multimodal:** Identificação via upload de arquivos ou captura direta por webcam.
* **Otimização de Renderização:** Interface preparada com aceleração via GPU (`transform: translateZ`) para garantir a fluidez no streaming de vídeo.
* **Interface Moderna:** Layout responsivo com **Dark Mode** nativo utilizando Bootstrap 5.
* **Cálculo de Confiança:** Algoritmo baseado em *Euclidean Distance* para exibir a porcentagem exata de precisão da IA ao identificar um rosto.

## 🚀 Tecnologias e Bibliotecas
* **Core:** Python 3.11 & Flask.
* **IA & Visão Computacional:** `face_recognition` (baseado em dlib), OpenCV, NumPy.
* **Infraestrutura:** Docker (Containerização) & Gunicorn (Servidor WSGI de produção).
* **Frontend:** JavaScript assíncrono (Fetch API) para processamento em tempo real sem recarregamento de página.

## ⚙️ Como executar o projeto localmente

### Pré-requisitos
* Python 3.11+
* Compilador C++ (necessário para compilação da biblioteca `dlib`)
* Docker (Opcional, para execução via contêiner)

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/rafelms/Projeto-FaceID.git](https://github.com/rafelms/Projeto-FaceID.git)
    cd Projeto-FaceID
    ```

2.  **Configuração do Ambiente Virtual:**
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No Linux/Mac:
    source venv/bin/activate
    ```

3.  **Instalação de Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execução:**
    ```bash
    python database.py  # Inicializa o banco de dados SQLite
    python app.py       # Inicia o servidor de desenvolvimento
    ```

## 🐳 Deploy com Docker
Para evitar conflitos de dependências de sistema e facilitar o deploy em nuvem (como no Render), utilize o Dockerfile incluso:

```bash
# Construir a imagem
docker build -t faceid-security .

# Rodar o container
docker run -p 10000:10000 faceid-security