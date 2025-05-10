import spacy
import unicodedata

nlp = spacy.load('pt_core_news_sm')

def detectar_intencao(texto):
    texto = texto.lower()
    if "sair" in texto or "tchau" in texto:
        return "sair"
    return "conversa"

def limpar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto

def verificar_categoria_input(texto):

    PALAVRAS_CHAVE = [
    "contrato", "obrigacao", "propriedade", "casamento", "divorcio", 
    "pensao", "heranca", "testamento", "locacao", "dano moral", 
    "direito de familia", "sucessao", "responsabilidade civil",
    "boa noite", "bom dia", "boa tarde", "ola", "tudo bem", "como vai"
    ]
    
    texto = limpar_texto(texto)
    for palavra in PALAVRAS_CHAVE:
        if palavra in texto:
            return True
    return False