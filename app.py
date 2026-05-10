from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import sqlite3
import face_recognition
import base64
import io

app = Flask(__name__)
# Configura a pasta onde as imagens serão salvas
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Rota da Tela Inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota da Tela de Cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        foto = request.files['foto']
        
        if foto and foto.filename != '':
            filename = secure_filename(foto.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            foto.save(filepath)
            
            # --- NOVA LÓGICA DE INTELIGÊNCIA ARTIFICIAL AQUI ---
            # 1. Carrega a imagem recém-salva para a memória da IA
            imagem_carregada = face_recognition.load_image_file(filepath)
            
            # 2. Procura por rostos na imagem
            rostos_encontrados = face_recognition.face_locations(imagem_carregada)
            
            # 3. Valida se encontrou pelo menos um rosto
            if len(rostos_encontrados) == 0:
                # Se não tem rosto, apagamos o arquivo inútil e cancelamos o cadastro
                os.remove(filepath)
                return "Erro: Nenhum rosto humano detectado na imagem. Tente outra foto!", 400
            # ---------------------------------------------------
            
            # Se passou pela IA, salva no banco de dados
            conn = sqlite3.connect('faceid.db')
            cursor = conn.cursor()
            
            cursor.execute("INSERT INTO pessoas (nome, cpf) VALUES (?, ?)", (nome, cpf))
            pessoa_id = cursor.lastrowid 
            
            cursor.execute("INSERT INTO imagens (pessoa_id, caminho_imagem) VALUES (?, ?)", (pessoa_id, filepath))
            
            conn.commit()
            conn.close()
            
            return redirect(url_for('lista_pessoas')) # Redireciona para a lista para ver o sucesso

    return render_template('cadastro.html')

@app.route('/pessoas')
def lista_pessoas():
    # Conecta ao banco de dados e busca todos os cadastros
    conn = sqlite3.connect('faceid.db')
    cursor = conn.cursor()
    
    # Busca os dados básicos da pessoa
    cursor.execute("SELECT id, nome, cpf, data_cadastro FROM pessoas")
    pessoas = cursor.fetchall()
    conn.close()
    
    # Envia a lista 'pessoas' para a página HTML renderizar
    return render_template('lista_pessoas.html', pessoas=pessoas)

# Rota para excluir uma pessoa e sua imagem
@app.route('/excluir/<int:id>', methods=['POST'])
def excluir_pessoa(id):
    conn = sqlite3.connect('faceid.db')
    cursor = conn.cursor()

    # 1. Busca o caminho da imagem no banco de dados para apagar o arquivo físico
    cursor.execute("SELECT caminho_imagem FROM imagens WHERE pessoa_id = ?", (id,))
    imagens = cursor.fetchall()

    for img in imagens:
        caminho_arquivo = img[0]
        # Verifica se o arquivo realmente existe na pasta antes de tentar apagar
        if os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo)

    # 2. Apaga os registros do banco de dados (tabelas 'imagens' e 'pessoas')
    cursor.execute("DELETE FROM imagens WHERE pessoa_id = ?", (id,))
    cursor.execute("DELETE FROM pessoas WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    # Redireciona de volta para a lista atualizada
    return redirect(url_for('lista_pessoas'))

@app.route('/reconhecer', methods=['GET', 'POST'])
def reconhecer():
    mensagem = None
    
    if request.method == 'POST':
        foto_upload = request.files['foto']
        
        if foto_upload and foto_upload.filename != '':
            # 1. Carrega a foto que o usuário acabou de enviar para teste
            imagem_desconhecida = face_recognition.load_image_file(foto_upload)
            encodings_desconhecidos = face_recognition.face_encodings(imagem_desconhecida)

            # Verifica se tem um rosto na foto de teste
            if len(encodings_desconhecidos) > 0:
                rosto_alvo = encodings_desconhecidos[0]

                # 2. Busca todos os cadastros no banco de dados
                conn = sqlite3.connect('faceid.db')
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT p.id, p.nome, i.caminho_imagem 
                    FROM pessoas p
                    JOIN imagens i ON p.id = i.pessoa_id
                """)
                registros = cursor.fetchall()
                conn.close()

                reconhecido = False

                # 3. Compara o rosto da foto enviada com cada foto salva no servidor
                for registro in registros:
                    pessoa_id, nome, caminho_imagem = registro
                    
                    try:
                        # Carrega a foto original do usuário salvo
                        img_banco = face_recognition.load_image_file(caminho_imagem)
                        encodings_banco = face_recognition.face_encodings(img_banco)
                        
                        if len(encodings_banco) > 0:
                            rosto_banco = encodings_banco[0]
                            
                            # 4. A mágica acontece aqui! O sistema compara as duas faces.
                            resultado = face_recognition.compare_faces([rosto_banco], rosto_alvo, tolerance=0.5)
                            
                            if resultado[0] == True:
                                # Calcula a distância e a porcentagem de confiança
                                distancia = face_recognition.face_distance([rosto_banco], rosto_alvo)[0]
                                confianca = round((1 - distancia) * 100, 2)
                                
                                mensagem = f"Sucesso! Pessoa identificada: {nome} (ID: {pessoa_id}) com {confianca}% de confiança."
                                reconhecido = True
                                break # Achou a pessoa, pode parar de procurar
                    except Exception as e:
                        print(f"Erro ao ler imagem do banco: {e}")

                if not reconhecido:
                    mensagem = "Rosto não reconhecido no banco de dados."
            else:
                mensagem = "Nenhum rosto humano foi detectado na imagem enviada."

    return render_template('reconhecer.html', mensagem=mensagem)

# Rota para exibir a página da Webcam
@app.route('/webcam')
def webcam():
    return render_template('webcam.html')

# Rota invisível (API) que recebe a foto do JavaScript e processa
@app.route('/processar_webcam', methods=['POST'])
def processar_webcam():
    dados = request.get_json()
    
    if 'imagem' not in dados:
        return jsonify({"erro": "Nenhuma imagem recebida"}), 400
        
    # Limpa o texto da imagem em Base64 e converte de volta para arquivo
    imagem_base64 = dados['imagem'].split(',')[1]
    imagem_bytes = base64.b64decode(imagem_base64)
    imagem_arquivo = io.BytesIO(imagem_bytes)
    
    # IA analisa a foto tirada pela webcam
    imagem_desconhecida = face_recognition.load_image_file(imagem_arquivo)
    encodings_desconhecidos = face_recognition.face_encodings(imagem_desconhecida)
    
    if len(encodings_desconhecidos) > 0:
        rosto_alvo = encodings_desconhecidos[0]
        
        # Busca no banco de dados
        conn = sqlite3.connect('faceid.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.nome, i.caminho_imagem 
            FROM pessoas p
            JOIN imagens i ON p.id = i.pessoa_id
        """)
        registros = cursor.fetchall()
        conn.close()
        
        # Compara com as pessoas cadastradas
        for registro in registros:
            pessoa_id, nome, caminho_imagem = registro
            try:
                img_banco = face_recognition.load_image_file(caminho_imagem)
                encodings_banco = face_recognition.face_encodings(img_banco)
                
                if len(encodings_banco) > 0:
                    rosto_banco = encodings_banco[0]
                    resultado = face_recognition.compare_faces([rosto_banco], rosto_alvo, tolerance=0.5)
                    
                    if resultado[0] == True:
                        # Calcula a distância e a porcentagem de confiança
                        distancia = face_recognition.face_distance([rosto_banco], rosto_alvo)[0]
                        confianca = round((1 - distancia) * 100, 2)
                        
                        return jsonify({
                            "reconhecido": True, 
                            "nome": nome, 
                            "id": pessoa_id,
                            "confianca": confianca
                        })
            except Exception as e:
                pass
                
        return jsonify({"reconhecido": False, "mensagem": "Rosto não reconhecido."})
    else:
        return jsonify({"reconhecido": False, "mensagem": "Nenhum rosto detectado."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)