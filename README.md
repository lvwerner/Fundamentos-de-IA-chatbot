# Chat IA — Interface Streamlit + Groq

Interface de chat com modelos de linguagem via Groq API, construída com Streamlit e LangChain.

---

## ✅ O que você precisa fazer antes de rodar

### 1. Criar uma conta Groq e obter sua chave de API

Acesse **https://console.groq.com**, crie uma conta gratuita e gere uma chave de API (API Key).

### 2. Configurar a chave no projeto

Copie o arquivo de exemplo e cole sua chave dentro dele:

```bash
cp .env.example .env
```

Abra o arquivo `.env` e edite a linha:

```
GROQ_API_KEY=cole_sua_chave_aqui
```

> ⚠️ **Sem essa chave o projeto não funciona.** Não compartilhe esse arquivo com ninguém.

### 3. Ativar o ambiente virtual

```bash
# Windows
myfirstproject\Scripts\activate

# macOS / Linux
source myfirstproject/bin/activate
```

### 4. Executar o projeto

```bash
streamlit run app.py
```

O navegador abrirá automaticamente em `http://localhost:8501`.

---

## Como usar

1. Digite sua mensagem na caixa de texto na parte inferior
2. Clique em **Enviar** ou pressione **Enter**
3. A resposta da IA aparece na tela em instantes
4. Use o painel lateral para ajustar as configurações

---

## Configurações disponíveis (painel lateral)

| Configuração | O que faz |
|---|---|
| **Modelo** | Escolhe qual IA responde. Llama 3.3 70b é o mais capaz; Llama 3.1 8b é o mais rápido |
| **Criatividade** | Valor baixo (0.0–0.3) = respostas mais objetivas. Valor alto (0.7–1.0) = respostas mais criativas |
| **Tokens máx.** | Controla o tamanho máximo de cada resposta |
| **Limpar chat** | Apaga o histórico e começa uma conversa nova |

---

## Problemas comuns

**"GROQ_API_KEY not found"**
→ O arquivo `.env` não existe ou está sem a chave. Revise o Passo 2.

**Interface lenta ou travando**
→ Troque para o modelo `llama-3.1-8b-instant` e reduza o valor de Tokens máx.

**Erro de conexão**
→ Verifique sua internet e se a chave de API é válida no painel da Groq.

---

## Tecnologias usadas

- [Streamlit](https://docs.streamlit.io) — interface web
- [LangChain](https://python.langchain.com) — integração com modelos de IA
- [Groq API](https://console.groq.com/docs) — execução dos modelos
