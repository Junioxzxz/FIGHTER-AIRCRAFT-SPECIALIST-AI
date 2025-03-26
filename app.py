from flask import Flask,render_template, request, Response
import google.generativeai as genai
from dotenv import load_dotenv
import os
from time import sleep
from helper import carrega, salva
from gerenciar_historico import remover_mensagens_mais_antigas
import uuid
from gerenciar_imagem import gerar_imagem_gemini

load_dotenv()

CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")
MODELO_ESCOLHIDO = "gemini-1.5-flash"   
genai.configure(api_key=CHAVE_API_GOOGLE)

app = Flask(__name__)
app.secret_key = 'fighter_specialist'

# We'll create a file with fighter aircraft data if it doesn't exist
FIGHTER_DATA_FILE = os.path.join("dados", "fighter_aircraft.txt")

def create_fighter_data_file():
    if not os.path.exists(FIGHTER_DATA_FILE):
        fighter_data = """
# Fighter Aircraft Database

## Fighter Aircraft Categories

1. First Generation Fighters (1945-1955)
   - F-86 Sabre, MiG-15, Hawker Hunter
   - Characteristics: Subsonic speeds, basic radar, machine guns and unguided rockets

2. Second Generation Fighters (1955-1960)
   - F-104 Starfighter, MiG-19, Dassault Mirage III
   - Characteristics: Supersonic speeds, radar-guided missiles, improved avionics

3. Third Generation Fighters (1960-1970)
   - F-4 Phantom II, MiG-21, Mirage F1
   - Characteristics: Improved avionics, multi-role capabilities, missile-centric combat

4. Fourth Generation Fighters (1970-1990)
   - F-15 Eagle, F-16 Fighting Falcon, MiG-29, Su-27
   - Characteristics: High maneuverability, powerful radar, digital avionics

5. 4.5 Generation Fighters (1990-2000)
   - F/A-18E/F Super Hornet, Eurofighter Typhoon, Rafale, Su-35
   - Characteristics: AESA radar, high agility, advanced weapons integration

6. Fifth Generation Fighters (2000-present)
   - F-22 Raptor, F-35 Lightning II, Su-57, J-20
   - Characteristics: Stealth technology, sensor fusion, supercruise capability

7. Sixth Generation Fighters (In development)
   - NGAD (USA), Tempest (UK), FCAS (EU), F-X (Japan)
   - Characteristics: Advanced AI integration, optional manning, directed energy weapons

## Key Fighter Aircraft Specifications

### F-22 Raptor
- Manufacturer: Lockheed Martin
- First flight: 1997
- Top speed: Mach 2.25 (1,500 mph, 2,410 km/h)
- Range: 1,840 miles (2,960 km)
- Armament: AIM-9X, AIM-120, M61A2 cannon
- Stealth features: Radar-absorbent materials, internal weapons bays, aligned edges

### F-35 Lightning II
- Manufacturer: Lockheed Martin
- Variants: F-35A (CTOL), F-35B (STOVL), F-35C (CV)
- Top speed: Mach 1.6 (1,200 mph, 1,930 km/h)
- Range: 1,350 miles (2,220 km)
- Armament: AIM-120, AIM-9X, GBU-31 JDAM, JSM, internal 25mm gun
- Features: Sensor fusion, DAS (Distributed Aperture System), stealth

### Su-57 Felon
- Manufacturer: Sukhoi
- First flight: 2010
- Top speed: Mach 2 (1,520 mph, 2,440 km/h)
- Range: 2,175 miles (3,500 km)
- Armament: R-77, Kh-38, Kh-59, 30mm cannon
- Features: Reduced radar cross-section, thrust vectoring, side-looking radar

### J-20 Mighty Dragon
- Manufacturer: Chengdu Aerospace Corporation
- First flight: 2011
- Top speed: Mach 2.0 estimated
- Range: 1,200 miles (2,000 km) estimated
- Armament: PL-15, PL-10, internal weapon bays
- Features: Canards, DSI (Diverterless Supersonic Inlet), stealth characteristics

### Eurofighter Typhoon
- Manufacturers: Airbus, BAE Systems, Leonardo
- First flight: 1994
- Top speed: Mach 2 (1,550 mph, 2,495 km/h)
- Range: 1,800 miles (2,900 km)
- Armament: Meteor, IRIS-T, Brimstone, Storm Shadow, 27mm cannon
- Features: Canard-delta wing, high agility, CAPTOR-E AESA radar

### Dassault Rafale
- Manufacturer: Dassault Aviation
- First flight: 1986
- Top speed: Mach 1.8 (1,390 mph, 2,225 km/h)
- Range: 2,000 miles (3,200 km)
- Armament: MICA, Meteor, SCALP-EG, AM39 Exocet, 30mm cannon
- Features: Omnirole capability, SPECTRA ECM suite, RBE2-AA AESA radar
"""
        salva(FIGHTER_DATA_FILE, fighter_data)

# Create fighter data file if it doesn't exist
create_fighter_data_file()

# Load fighter aircraft data
contexto = carrega(FIGHTER_DATA_FILE)

caminho_imagem_enviada = None
UPLOAD_FOLDER = "imagens_temporarias"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def criar_chatbot():
    personalidade = "fighter_specialist"

    prompt_do_sistema = f"""
    # FIGHTER AIRCRAFT SPECIALIST AI

    You are an expert AI assistant specialized exclusively in fighter aircraft information, with comprehensive knowledge spanning from early propeller-driven fighters to cutting-edge 6th generation aircraft.

    ## Your Expertise Areas
    - Technical specifications and performance data of fighter aircraft
    - Development history and program details
    - Combat records and operational use
    - Comparative analysis between different fighter models
    - Stealth features and advanced technologies
    - Weapons systems and armament options

    ## Response Behavior
    - Focus EXCLUSIVELY on fighter aircraft information
    - Provide precise technical details and historical context
    - If asked about non-fighter aircraft (commercial planes, bombers, transport) or non-aviation topics, politely redirect to relevant fighter jet topics
    - Use metric and imperial measurements when discussing performance
    - Include development timelines for historical context
    - Compare capabilities objectively between different fighter generations and nations

    ## Response Format
    - Begin with a direct answer to the question
    - Provide technical specifications when relevant
    - Include historical context when appropriate
    - Compare with contemporary fighters when useful
    - Conclude with key distinguishing features

    # CONTEXT
    {contexto}

    # Image Analysis
    When analyzing fighter aircraft images:
    - Identify the aircraft model and variant
    - Note distinguishing features visible in the image
    - Point out key technological elements visible
    - Compare with similar aircraft if relevant
    """

    configuracao_modelo = {
        "temperature" : 0.2,
        "max_output_tokens" : 8192
    }

    llm = genai.GenerativeModel(
        model_name=MODELO_ESCOLHIDO,
        system_instruction=prompt_do_sistema,
        generation_config=configuracao_modelo
    )

    chatbot = llm.start_chat(history=[])

    return chatbot

chatbot = criar_chatbot()

def bot(prompt):
    maximo_tentativas = 1
    repeticao = 0
    global caminho_imagem_enviada

    while True:
        try:
            mensagem_usuario = f"""
            FIGHTER AIRCRAFT QUERY:
            {prompt}
            """

            if caminho_imagem_enviada:
                mensagem_usuario += "\n Analyze this fighter aircraft image and provide detailed information about it."
                arquivo_imagem = gerar_imagem_gemini(caminho_imagem_enviada)
                resposta = chatbot.send_message([arquivo_imagem, mensagem_usuario])
                os.remove(caminho_imagem_enviada)
                caminho_imagem_enviada = None
            else:
                resposta = chatbot.send_message(mensagem_usuario)

            if len(chatbot.history) > 10:
                chatbot.history = remover_mensagens_mais_antigas(chatbot.history)

            return resposta.text
        except Exception as erro:
            repeticao += 1
            if repeticao >= maximo_tentativas:
                return "Error with Gemini API: %s" % erro
            
            if caminho_imagem_enviada:
                os.remove(caminho_imagem_enviada)
                caminho_imagem_enviada = None

            sleep(50)

@app.route("/upload_imagem", methods=["POST"])
def upload_imagem():
    global caminho_imagem_enviada

    if "imagem" in request.files:
        imagem_enviada = request.files["imagem"]
        nome_arquivo = str(uuid.uuid4()) + os.path.splitext(imagem_enviada.filename)[1]
        caminho_arquivo = os.path.join(UPLOAD_FOLDER, nome_arquivo)
        imagem_enviada.save(caminho_arquivo)
        caminho_imagem_enviada = caminho_arquivo
        return "Image uploaded successfully", 200
    return "No file uploaded", 400

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]
    resposta = bot(prompt)
    return resposta

@app.route("/")
def home():
    return render_template("chatbot.html")

if __name__ == "__main__":
    app.run(debug = True)