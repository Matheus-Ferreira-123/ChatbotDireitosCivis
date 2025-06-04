from dotenv import load_dotenv
import os
import spacy
import unicodedata
import fitz
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')
nlp = spacy.load('pt_core_news_sm')

def detectar_intencao(texto):
    texto_limpo = limpar_texto(texto)

    if texto_limpo == "/info":
        return "info"
    elif texto_limpo.strip() == "" or texto_limpo.strip().isnumeric():
        return "invalid"
    return "conversa"

def limpar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto

def extrair_texto_pdf(caminho_pdf):
    doc = fitz.open(caminho_pdf)
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    return texto

def conversar(usuario_input):
    
    if detectar_intencao(usuario_input) == "info":
        return "Esse é um projeto desenvolvido na faculdade com foco em oferecer um canal de consulta acessível e eficiente para esclarecer dúvidas gerais sobre o código civil brasileiro, como contratos, processos judiciais, família e sucessões, entre outras; e seu objetivo não é apenas informar, mas fortalecer o acesso à justiça de forma mais rápida e eficaz ao usuário."
    
    if detectar_intencao(usuario_input) == "invalid":
        return "Digite uma mensagem válida para que eu consiga lhe ajudar."
    
    chat = model.start_chat(history=[])
    
    prompt = f"""
    Baseando-se SOMENTE com o que foi informado no conteúdo abaixo, responda ao input do usuário apenas
    se o conteúdo tiver algo a ver com o que está no conteúdo. NÃO invente nada além do que está no conteúdo fornecido.
    Caso o input não tenha nada relacionado ao que consta nos conteúdos, responda ESTRITAMENTE com essa mensagem:
    "Desculpe, mas o tema abordado não está relacionado à minha área de conhecimento. Apenas posso responder 
    perguntas sobre direitos civis brasileiros. Gostaria que eu ajudasse de alguma outra forma?"

    Conteúdo (Código civil):
    {TEXTO_CIVIL}

    Input do usuário:
    {limpar_texto(usuario_input)}
    """
    response = chat.send_message(prompt)
    return response.text.strip()
    
    
TEXTO_CIVIL = extrair_texto_pdf("documents/codigo_civil.pdf")
#TEXTO_CONSUMIDOR = extrair_texto_pdf("documents/cdc_e_normas_correlatas.pdf")
#TEXTO_IDOSO = extrair_texto_pdf("documents/estatuto_do_idoso.pdf")