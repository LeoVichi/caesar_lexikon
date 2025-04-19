
# 🛡️ Glossário Militar de Termos Latinos em *De Bello Gallico*

Este projeto utiliza **Processamento de Linguagem Natural (NLP)** com a biblioteca [Stanza](https://stanfordnlp.github.io/stanza/) para extrair e analisar substantivos latinos do texto *Commentarii de Bello Gallico*, de Júlio César, identificando aqueles usados em contextos militares e cruzando com definições do dicionário **Lewis & Short**.

## 📚 Objetivo

Criar um glossário contextualizado de termos militares latinos baseado na frequência de uso e no contexto textual da obra *De Bello Gallico*, com definições extraídas automaticamente do dicionário Lewis & Short em formato JSON.

---

## 🚀 Funcionalidades

- Tokenização, lematização e análise gramatical do texto com Stanza.
- Identificação de substantivos mais frequentes.
- Filtro semântico baseado em palavras-chave militares.
- Consulta automática ao dicionário Lewis & Short.
- Geração de arquivo JSON com o glossário militar contextualizado.

---

## 📂 Estrutura esperada do projeto

```
project/
│
├── script.py                     # Este script principal
├── de_bello_gallico.txt         # Texto original em Latim
├── output/
│   └── glossario_militar.json   # Arquivo gerado com os resultados
└── repositoria/
    └── latin-dictionary/
        └── lewis-short-json-master/
            ├── ls_A.json
            ├── ls_B.json
            └── ...              # Arquivos JSON com o dicionário
```

> Certifique-se de manter a estrutura do dicionário conforme acima. Os arquivos `ls_A.json`, `ls_B.json`, etc., são essenciais para a extração de definições.

---

## 🧠 Pré-requisitos

- Python 3.8+
- Ambiente virtual recomendado

---

## 📦 Instalação

### Clone o repositório principal
```bash
git clone https://github.com/LeoVichi/caesar_lexikon
cd caesar_lexikon
```

### Crie a pasta para repositórios auxiliares
```bash
mkdir -p repositoria/latin-dictionary
```

### Clone o dicionário Lewis & Short
```bash
git clone https://github.com/IohannesArnold/lewis-short-json repositoria/latin-dictionary/lewis-short-json-master
```

### Crie um ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### Instale as dependências
```bash
pip install -r requirements.txt
```

### Execute o script
```bash
python lexikon.py
```

---

## 📄 Exemplo de saída

O script gera um arquivo `output/glossario_militar.json` com estrutura semelhante a:

```json
{
  "castra": {
    "definição_lewis_short": "Camp, military camp, fortified place",
    "definição_contexto": "Castra ab hostibus capta sunt...",
    "frequência": 23
  }
}
```

---

## 🧰 Tecnologias utilizadas

- [Stanza](https://stanfordnlp.github.io/stanza/)
- [Python Standard Library](https://docs.python.org/3/library/)
- [Lewis & Short Latin Dictionary (JSON)](https://github.com/IohannesArnold/lewis-short-json)

---

## 📜 Licença

Este projeto está licenciado sob a [MIT License](LICENSE), exceto o dicionário Lewis & Short, que segue a licença própria disponível no repositório original.

---

## 🙋 Autor

**Leonardo Vichi**  
contact@leonardovichi.com  
[iuliuscaesar.org](https://iuliuscaesar.org)

---

## ✨ Contribuição

Pull requests são bem-vindos! Para mudanças maiores, por favor abra uma *issue* primeiro para discutirmos o que você gostaria de modificar.

---

## 📘 Referências

- Caesar, *Commentarii de Bello Gallico*
- Charlton T. Lewis, Charles Short, A Latin Dictionary. 1879
- Stanford NLP Group - Stanza
