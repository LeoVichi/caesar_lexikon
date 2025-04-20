import stanza
import json
import re
import os
import unicodedata
from collections import Counter

# Baixar o modelo de Latim do Stanza se necessário
try:
    stanza.download('la')
except Exception:
    pass  # Se já estiver baixado, continua sem erro

# Carregar o processador de NLP para Latim
nlp = stanza.Pipeline(lang='la', processors='tokenize,pos,lemma')

# Ler o texto do *De Bello Gallico*
with open("de_bello_gallico.txt", "r", encoding="utf-8") as f:
    texto = f.read()

# Processar o texto com NLP
doc = nlp(texto)

# Diretório do Lewis & Short JSON
# Obter caminho absoluto do diretório onde o script está
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))

# Caminho para o diretório do dicionário (pasta anterior ao script)
DIRETORIO_DICIONARIO = os.path.join(os.path.dirname(DIRETORIO_ATUAL), "repositoria", "latin-dictionary", "lewis-short-json-master")

# Lista de palavras-chave militares para análise de contexto
palavras_militares_contexto = {
    "castra", "bellum", "pugna", "gladius", "centurio", "exercitus", "proelium",
    "signum", "pilum", "tormenta", "testudo", "lorica", "eques", "acies", "scutum"
}

# Função para normalizar texto (remover diacríticos e acentos)
def normalizar(texto):
    if texto:
        return unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII").lower()
    return ""

# Função para limpar referências literárias das definições
def limpar_definicao(texto):
    return re.sub(r'\b\d{1,4}\b', '', texto).strip()

# Função para buscar definições no Lewis & Short JSON
def buscar_definicao_lewis_short(termo):
    if not termo:
        return "Definitio non inventa."

    termo_normalizado = normalizar(termo)
    letra_inicial = termo_normalizado[0].upper()
    arquivo_json = os.path.join(DIRETORIO_DICIONARIO, f"ls_{letra_inicial}.json")

    if not os.path.exists(arquivo_json):
        return "Definição não encontrada no Lewis & Short."

    with open(arquivo_json, "r", encoding="utf-8") as f:
        lista_entradas = json.load(f)

    melhor_definicao = None

    for entrada in lista_entradas:
        lemma = entrada.get("key")
        if lemma:
            lemma_normalizado = normalizar(lemma)

            if lemma_normalizado == termo_normalizado or re.sub(r'\d+$', '', lemma_normalizado) == termo_normalizado:
                sentidos = entrada.get("senses", [])

                # Extração de definições, incluindo listas aninhadas
                definicoes_filtradas = []

                def extrair_definicoes(lista):
                    for item in lista:
                        if isinstance(item, str):
                            definicao_limpa = limpar_definicao(item)
                            if len(definicao_limpa) > 5 and len(definicao_limpa) < 300:
                                definicoes_filtradas.append(definicao_limpa)
                        elif isinstance(item, list):
                            extrair_definicoes(item)

                extrair_definicoes(sentidos)

                if definicoes_filtradas:
                    return definicoes_filtradas[0]

                melhor_definicao = "Definição não disponível."

    return melhor_definicao if melhor_definicao else "Definição não encontrada no Lewis & Short."

# Criar lista de substantivos válidos (evitando fragmentos incorretos)
substantivos_validos = []
substantivos_invalidos = {"castr", "milit", "duc", "victor", "popul", "consul", "legat"}

for sent in doc.sentences:
    for word in sent.words:
        if word.upos == "NOUN":
            lemma_corrigido = word.lemma.lower().strip()
            if len(lemma_corrigido) >= 4 and lemma_corrigido not in substantivos_invalidos:
                substantivos_validos.append(lemma_corrigido)

# Criar contador de frequência dos termos válidos
frequencia_termos = Counter(substantivos_validos)

# Função para verificar se um termo aparece em contexto militar
def termo_aparece_em_contexto_militar(termo, contexto):
    return any(palavra in contexto.lower() for palavra in palavras_militares_contexto)

# Criar glossário militar
glossario_militar = {}

for termo, count in frequencia_termos.most_common(50):
    definicao_dicionario = buscar_definicao_lewis_short(termo)

    frases_encontradas = [
        sent.text for sent in doc.sentences if re.search(rf'\b{termo}\b', sent.text, re.IGNORECASE)
    ]

    definicao_contexto = " ".join(frases_encontradas[:3])
    if len(definicao_contexto) > 300:
        definicao_contexto = definicao_contexto[:297] + "..."

    # Filtrar apenas termos que aparecem em contexto militar
    if termo_aparece_em_contexto_militar(termo, definicao_contexto):
        glossario_militar[termo] = {
            "definição_lewis_short": definicao_dicionario,
            "definição_contexto": definicao_contexto if definicao_contexto else "Definitio non inventa.",
            "frequência": count
        }

# Salvar glossário militar
# Criar diretório de saída se não existir
DIRETORIO_OUTPUT = os.path.join(DIRETORIO_ATUAL, "output")
os.makedirs(DIRETORIO_OUTPUT, exist_ok=True)

# Caminho completo do arquivo de saída
CAMINHO_SAIDA = os.path.join(DIRETORIO_OUTPUT, "glossario_militar.json")

# Salvar glossário militar no diretório de saída
with open(CAMINHO_SAIDA, "w", encoding="utf-8") as f:
    json.dump(glossario_militar, f, ensure_ascii=False, indent=4)

print(f"📜 Glossário militar gerado com sucesso em: {CAMINHO_SAIDA}")

