from config import GEMINI_API_KEY
import google.generativeai as genai
from pln_utils import detectar_intencao, limpar_texto, verificar_categoria_input, extrair_texto_pdf

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

TEXTO_CONSTITUICAO = extrair_texto_pdf("documents/codigo_civil.pdf")

def conversar(usuario_input):
    intencao = detectar_intencao(usuario_input)

    if intencao == "sair": 
        return "Até mais! Pode contar comigo para responder qualquer outra questão sobre seus direitos civis."
    elif intencao == "ola":
        return "Olá! Como posso lhe ajudar?"
    
    if verificar_categoria_input(usuario_input, TEXTO_CONSTITUICAO):
        prompt = f"""
        Baseando-se apenas no código civil brasileiro (somente com o que foi informado no conteúdo abaixo, contendo a Constituição Federal),
        responda à pergunta do usuário. NÃO invente nada além do que está no conteúdo fornecido.

        Conteúdo (Constituição Federal):
        {TEXTO_CONSTITUICAO}

        Input do usuário:
        {usuario_input}
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    else:
        return "Desculpe, só posso responder perguntas sobre direitos civis brasileiros. (Digite 'sair' caso queira encerrar)"

def main():

    print("Olá! Eu sou um chatbot especializado nos direitos civis brasileiros. Como posso ajudar? (Digite 'sair' para encerrar)")

    while True:
        user_input = input("> ").strip()
        if user_input is None:
            break
        resposta = conversar(user_input)
        print(resposta)

        if limpar_texto(user_input) in ["sair", "tchau", "até mais"]:
            break

if __name__ == "__main__":
    main()