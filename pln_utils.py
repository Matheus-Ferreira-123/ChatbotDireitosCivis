from config import GEMINI_API_KEY
import spacy
import unicodedata
import fitz
import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')
nlp = spacy.load('pt_core_news_sm')

def detectar_intencao(texto):
    texto_limpo = limpar_texto(texto)

    if any(palavra in texto_limpo for palavra in ["sair", "tchau", "ate mais"]):
        return "sair"
    elif any(palavra in texto_limpo for palavra in ["ola", "tudo bem", "como vai", "oi"]):
        return "ola"
    return "conversa"

def limpar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto

def verificar_categoria_input(texto_usuario, contexto_constituicao):
    
    resposta = gerar_resposta(texto_usuario, contexto_constituicao)
    resposta_limpa = limpar_texto(resposta)

    print(f"Resposta da IA: {resposta_limpa}")
    return resposta_limpa == "sim"

def extrair_texto_pdf(caminho_pdf):
    doc = fitz.open(caminho_pdf)
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    return texto

def gerar_resposta(texto_usuario, contexto_constituicao):
    prompt = f"""
    Baseando-se apenas nas informações abaixo retiradas da Constituição Federal,
    o texto do usuário possui alguma relação com o código de direitos civis brasileiro?

    Responda SOMENTE com "Sim" ou "Não", sem justificativas ou adições.

    Conteúdo (Constituição Federal):
    {contexto_constituicao}

    Texto do usuário:
    {texto_usuario}
    """

    resposta = model.generate_content(prompt)
    return resposta.text.strip()
    
TEXTO_CONSTITUICAO = extrair_texto_pdf("documents/codigo_civil.pdf")