# 🤖 Chat IA - Interface Streamlit

Uma interface bonita e moderna para conversar com modelos de IA usando Groq API e LangChain.

## 🎨 Características

✨ **Interface Moderna**
- Design limpo e responsivo com Streamlit
- Animações suaves e efeitos visuais
- Chat histórico persistente

⚡ **Modelos Rápidos**
- Llama 3.3 70b (recomendado - mais atualizado)
- Llama 3.1 8b (mais rápido)
- Gemma 2 9b (alternativa rápida)

🎛️ **Controles Ajustáveis**
- Controlar nível de criatividade (temperatura)
- Ajustar tamanho máximo das respostas
- Limpar histórico de conversa

## 📋 Pré-requisitos

- Python 3.8+
- Chave de API Groq (gratuita em https://console.groq.com)
- Dependências já instaladas (requirements.txt)

## ⚙️ Instalação

### 1. Configure sua chave da API

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env e adicione sua chave
# GROQ_API_KEY=sua_chave_aqui
```

### 2. Ative o ambiente virtual

```bash
# No Windows
myfirstproject\Scripts\activate

# No macOS/Linux
source myfirstproject/bin/activate
```

### 3. Execute a aplicação

```bash
streamlit run app.py
```

A interface abrirá automaticamente em `http://localhost:8501`

## 🚀 Como Usar

1. **Digite sua mensagem** na caixa de entrada
2. **Clique em "Enviar"** ou pressione Enter
3. **Aguarde a resposta** da IA
4. **Ajuste configurações** no painel lateral conforme necessário

## 🎯 Dicas

- Use a **criatividade alta** (0.8-1.0) para respostas mais criativas
- Use **criatividade baixa** (0.0-0.3) para respostas mais factuais
- O **Mixtral** é ótimo para equilibrar velocidade e qualidade
- Clique em **"Limpar Chat"** para começar uma nova conversa

## 🔧 Personalização

Edite `app.py` para:
- Mudar cores e temas
- Adicionar novos modelos
- Personalizar o layout
- Adicionar funcionalidades extras

## 📚 Recursos

- [Documentação Streamlit](https://docs.streamlit.io)
- [LangChain Docs](https://python.langchain.com)
- [Groq API](https://console.groq.com/docs)

## ⚠️ Troubleshooting

**Erro: "GROQ_API_KEY not found"**
- Certifique-se que o arquivo `.env` existe e tem sua chave

**Interface lenta**
- Tente um modelo mais rápido (Llama 8b)
- Reduza o tamanho máximo da resposta

**Erro de conexão**
- Verifique sua conexão com a internet
- Verifique se sua chave API é válida

---

**Desenvolvido com ❤️ usando Streamlit, LangChain e Groq**
