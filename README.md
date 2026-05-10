# 🔐 FaceID Security - Sistema de Reconhecimento Facial

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)

Projeto acadêmico desenvolvido para a disciplina de **[Nome da Disciplina]**. Trata-se de uma aplicação web capaz de realizar o cadastro de usuários e efetuar o reconhecimento facial através de upload de imagens ou via webcam em tempo real, calculando a porcentagem de confiança da IA.

## ✨ Funcionalidades
* **Cadastro de Usuários:** Validação automática de rostos via Inteligência Artificial no momento do cadastro.
* **Reconhecimento por Upload:** Identificação de pessoas a partir de fotos enviadas pelo sistema.
* **Reconhecimento por Webcam:** Identificação em tempo real direto pelo navegador do usuário.
* **Cálculo de Confiança:** Exibição da porcentagem de precisão da IA (face distance) ao identificar um rosto.

## 🚀 Tecnologias Utilizadas
* **Backend:** Python 3, Flask
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
* **Banco de Dados:** SQLite3
* **Inteligência Artificial:** OpenCV, biblioteca `face_recognition`

## ⚙️ Como executar o projeto localmente

### Pré-requisitos
Certifique-se de ter o Python e o Git instalados em sua máquina.

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone [URL_DO_SEU_REPOSITORIO_AQUI]

2. Acesse a pasta do projeto no terminal:
    ```bash
    cd PROJETO-FACE-ID

3. Crie e ative um ambiente virtual:
- Windows:
    ```bash
    python -m venv venv
.\venv\Scripts\activate

-Linux/Mac
    ```bash
    python3 -m venv venv
    source venv/bin/activate 

   
4. Instale as dependências:
    ```bash
    pip install -r requirements.txt

5. Crie o arquivo de banco de dados (tabelas):
    ```bash
    python database.py

6. Inicie o servidor local:
    ```bash
    python app.py

7. Acesse no navegador:
    Abra o seu navegador e acesse: http://127.0.0.1:5000