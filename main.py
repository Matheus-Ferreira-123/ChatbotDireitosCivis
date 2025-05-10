from config import GEMINI_API_KEY
import google.generativeai as genai
from pln_utils import detectar_intencao, limpar_texto, verificar_categoria_input

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def conversar(usuario_input):
    intencao = detectar_intencao(usuario_input)

    if intencao == "sair": 
        return "Até mais! Pode contar comigo para responder qualquer outra questão sobre seus direitos civis."
    
    if verificar_categoria_input(usuario_input):
        response = model.generate_content(usuario_input)
        return response.text
    else:
        return "Desculpe, só posso responder perguntas sobre direitos civis brasileiros. (digite \'sair\' caso queira encerrar)"

def main():

    print("Olá! Eu sou um chatbot especializado nos direitos civis brasileiros. Como posso ajudar?")

    while True:
        user_input = input("> ")
        resposta = conversar(user_input)
        print(resposta)

        if user_input.lower() in ["sair", "tchau", "até mais"]:
            break

if __name__ == "__main__":
    main()