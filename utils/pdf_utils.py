# utils/pdf_utils.py

from typing import List, Union
import logging
import io

from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text as pdfminer_extract
import fitz  # PyMuPDF
from PIL import Image
import pytesseract

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def extrair_texto_pyppdf2(arquivo: Union[str, io.BytesIO]) -> str:
    """
    Extrai texto usando PyPDF2. 
    Retorna string concatenada de todas as páginas, ou '' se nada for extraído.
    """
    try:
        reader = PdfReader(arquivo)
        textos = [
            pagina.extract_text() or ""
            for pagina in reader.pages
        ]
        resultado = "".join(textos).strip()
        if resultado:
            logger.info("PyPDF2 extraiu texto (%d caracteres)", len(resultado))
        return resultado
    except Exception as e:
        logger.warning("PyPDF2 falhou: %s", e)
        return ""


def extrair_texto_pdfminer(arquivo: Union[str, io.BytesIO]) -> str:
    """
    Extrai texto usando pdfminer.six. 
    Retorna tudo que conseguir, ou '' em caso de falha.
    """
    try:
        texto = pdfminer_extract(arquivo)
        if texto.strip():
            logger.info("pdfminer extraiu texto (%d caracteres)", len(texto))
        return texto.strip()
    except Exception as e:
        logger.warning("pdfminer.six falhou: %s", e)
        return ""


def extrair_texto_ocr(arquivo: Union[str, io.BytesIO]) -> str:
    """
    Converte cada página do PDF em imagem e aplica OCR com pytesseract.
    Bom para PDFs escaneados sem camada de texto.
    """
    texto_total = []
    try:
        doc = fitz.open(stream=arquivo.read() if hasattr(arquivo, "read") else arquivo, filetype="pdf")
        for idx, pagina in enumerate(doc):
            pix = pagina.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            ocr = pytesseract.image_to_string(img).strip()
            logger.info("OCR página %d extraiu %d caracteres", idx+1, len(ocr))
            texto_total.append(ocr)
    except Exception as e:
        logger.error("OCR falhou: %s", e)
    return "\n".join(texto_total)


def extrair_texto_dos_pdfs(arquivos: List[Union[str, io.BytesIO]]) -> str:
    """
    Para cada arquivo PDF, tenta em ordem:
      1. PyPDF2
      2. pdfminer.six
      3. OCR (PyMuPDF + pytesseract)
    Retorna o texto completo concatenado de todos os arquivos.
    """
    resultados: List[str] = []
    for arquivo in arquivos:
        # 1) PyPDF2
        texto = extrair_texto_pyppdf2(arquivo)
        if texto:
            resultados.append(texto)
            continue

        # 2) pdfminer.six
        texto = extrair_texto_pdfminer(arquivo)
        if texto:
            resultados.append(texto)
            continue

        # 3) OCR
        logger.info("Aplicando OCR ao arquivo")
        texto = extrair_texto_ocr(arquivo)
        resultados.append(texto)

    return "\n\n".join(resultados)


def dividir_texto_em_trechos(
    texto: str,
    tamanho_trecho: int = 1500,
    sobreposicao: int = 300
) -> List[str]:
    """
    Divide uma string longa em chunks sem cortar frases:
    usa RecursiveCharacterTextSplitter do LangChain.
    """
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=tamanho_trecho,
        chunk_overlap=sobreposicao,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return splitter.split_text(texto)
