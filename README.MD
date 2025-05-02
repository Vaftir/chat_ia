# PDF Conversational Assistant

Uma aplicação Streamlit para conversar com documentos PDF usando LangChain e OpenAI. Extrai texto de PDFs (incluindo escaneados via OCR), cria embeddings e permite questionar o conteúdo via chat inteligente.

## ✨ Funcionalidades

- **Upload múltiplo de PDFs** (texto e escaneados)
- Extração de texto com 3 métodos:
  - PyPDF2 para PDFs textuais
  - pdfminer.six como fallback
  - OCR com PyMuPDF+Tesseract para imagens
- Divisão inteligente de texto em chunks
- Vetorização com OpenAI Embeddings
- Memória de conversa contextual
- Respostas com citações às fontes originais
- Suporte a modelos GPT-3.5/GPT-4

## 🚀 Instalação

1. **Pré-requisitos**:
   - Python 3.9+
   - Tesseract OCR instalado ([Instruções](#-dependências-específicas))

2. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/pdf-chatbot.git
cd pdf-chatbot
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

1. Crie um arquivo `.env` na raiz do projeto:
```env
OPENAI_API_KEY=sk-sua-chave-aqui
# Opcional:
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.7
```

2. Instale o Tesseract OCR:
- **Windows**: [Installer oficial](https://github.com/UB-Mannheim/tesseract/wiki)
- **Linux**: `sudo apt install tesseract-ocr`
- **Mac**: `brew install tesseract`

## 🖥 Uso

1. Inicie a aplicação:
```bash
streamlit run app.py
```

2. No navegador:
- Faça upload de PDFs
- Aguarde o processamento (verifique logs no terminal)
- Comece a conversar!

## 🗂 Estrutura do Projeto
```
.
├── app.py                 # Aplicação principal Streamlit
├── utils/
│   ├── langchain_utils.py # Configurações LangChain/OpenAI
│   └── pdf_utils.py       # Processamento de PDFs e OCR
├── requirements.txt       # Dependências
├── .env                  # Chaves API e configurações
└── README.md
```

## 📦 Dependências Principais
| Pacote | Versão | Finalidade |
|--------|--------|------------|
| `streamlit` | >=1.34 | Interface web |
| `langchain-openai` | >=0.0.8 | Integração OpenAI |
| `PyPDF2` | >=3.0 | Extração básica de PDF |
| `pdfminer.six` | >=20221105 | Fallback para PDFs complexos |
| `PyMuPDF` | >=1.24 | Renderização de PDF para OCR |
| `pytesseract` | >=0.3.10 | Reconhecimento óptico de caracteres |
| `faiss-cpu` | >=1.8.0 | Vector store eficiente |

## 🤝 Contribuição
Contribuições são bem-vindas! Siga os passos:
1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

 
## 📄 Licença
Distribuído sob licença MIT. Veja LICENSE para mais informações.


**Recursos adicionais para incluir posteriormente:**
1. Adicione um screenshot ou GIF animado na seção de demo
2. Inclua uma seção de "FAQ/Troubleshooting"
3. Adicione badges de status (build, version, etc)
4. Inclua informações de deployment (Docker, Cloud, etc)
5. Adicione exemplos de uso avançado

