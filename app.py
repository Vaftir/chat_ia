# app.py
import streamlit as st
from streamlit_chat import message

from utils.pdf_utils import (
    extrair_texto_dos_pdfs,
    dividir_texto_em_trechos
)
from utils.langchain_utils import (
    criar_vector_store,
    criar_conversation_chain
)


def main() -> None:
    st.set_page_config(page_title="Converse com seus arquivos", page_icon=":books:")
    st.title("📚 Chat com seus PDFs")

    # Inicializa estado
    if "texto_pdf" not in st.session_state:
        st.session_state.texto_pdf = ""
    if "conversation_chain" not in st.session_state:
        st.session_state.conversation_chain = None

    # Layout em colunas: upload à esquerda, chat à direita
    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("Upload de PDFs")
        pdf_docs = st.file_uploader(
            "Selecione um ou mais arquivos PDF",
            type="pdf",
            accept_multiple_files=True
        )
        if pdf_docs:
            if st.button("Processar PDFs"):
                with st.spinner("Extraindo e processando texto..."):
                    # Extrai texto com fallback (PyPDF2, pdfminer, OCR)
                    st.session_state.texto_pdf = extrair_texto_dos_pdfs(pdf_docs)

                    # Valida extração
                    if not st.session_state.texto_pdf.strip():
                        st.warning(
                            "Não foi possível extrair texto dos PDFs. "
                            "Verifique se eles contêm texto pesquisável ou tente novamente com documentos diferentes."
                        )
                    else:
                        # Divide em trechos para embeddings
                        chunks = dividir_texto_em_trechos(st.session_state.texto_pdf)

                        # Cria vector store e cadeia de conversação
                        vectorstore = criar_vector_store(chunks)
                        st.session_state.conversation_chain = criar_conversation_chain(
                            vectorstore
                        )
                        st.success("✅ PDFs processados! Faça sua pergunta ao bot.")

    with col2:
        st.subheader("Chat")
        user_question = st.text_input("Digite sua pergunta:", key="input_question")

        if user_question and st.session_state.conversation_chain:
            try:
                with st.spinner("Pensando..."):
                    result = st.session_state.conversation_chain.invoke(
                        {"question": user_question}
                    )
                history = result.get("chat_history", [])
                for i, msg in enumerate(history):
                    is_user = (i % 2 == 0)
                    message(
                        msg.content,
                        is_user=is_user,
                        key=f"{i}_{'user' if is_user else 'bot'}"
                    )
            except Exception as e:
                st.exception(e)


if __name__ == "__main__":
    main()