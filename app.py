import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader 
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import streamlit as st

load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash", 
    temperature=0.3
)


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

def cargar_documento(ruta_pdf):
    
    loader = PyMuPDFLoader(ruta_pdf)
    documentos = loader.load()
    
    divisor = RecursiveCharacterTextSplitter(
        chunk_size=2000, 
        chunk_overlap=300,
        length_function=len,
        separators=["\n\n", "\n", "。", ".", "!", "?", " ", ""]
    )
    textos = divisor.split_documents(documentos)
    return textos

def crear_base_de_conocimiento(textos):
    vectorstore = FAISS.from_documents(textos, embeddings)
    return vectorstore

st.title("Agente del Mercado Central 24h")
st.write("Hola! Soy Dory, estoy aqui para ayudarte sobre cualquier duda que tengas sobre las políticas de atención al cliente, cambios y devoluciones.")

if 'vectorstore' not in st.session_state:
    with st.spinner("Cargando documento y creando base de conocimiento... (La primera vez tarda un poco)"):
        textos = cargar_documento("politicas.pdf")
        st.session_state.vectorstore = crear_base_de_conocimiento(textos)
        st.success("La información ha sido cargada con éxito y está lista para ser usada.")

pregunta = st.text_input("¿Qué quieres saber sobre las políticas de atención al cliente, cambios y devoluciones del Mercado Central?")

if pregunta:
    with st.spinner("Buscando respuesta..."):
        
        docs = st.session_state.vectorstore.similarity_search(pregunta, k=5)
        
        contexto = "\n\n---\n\n".join([doc.page_content for doc in docs])
        
        prompt = f"""Eres el asistente oficial de atención al cliente de Mercado Central 24h.

CONTEXTO (extraído del documento oficial de políticas):
{contexto}

PREGUNTA DEL CLIENTE: {pregunta}

INSTRUCCIONES OBLIGATORIAS:
1. Responde ÚNICAMENTE con información del CONTEXTO anterior.
2. Si la información está en el contexto, da la respuesta COMPLETA con todos los detalles (plazos, condiciones, montos, secciones).
3. Cita la sección del documento cuando sea posible (ej: "Según la sección 4.3...").
4. Si NO encuentras la respuesta en el contexto, responde exactamente: "No encontré esta información en el documento de políticas. Te sugiero contactar al Módulo de Atención al Cliente o llamar al 800-CENTRAL."
5. NO inventes información. NO uses conocimiento externo.
6. Responde en español, de forma clara y profesional.

RESPUESTA:"""
        
        respuesta = llm.invoke(prompt)
        
        
        if hasattr(respuesta, 'content'):
            contenido = respuesta.content
        else:
            contenido = str(respuesta)
            
        if isinstance(contenido, list):
            texto_respuesta = ""
            for item in contenido:
                if isinstance(item, dict) and 'text' in item:
                    texto_respuesta += item['text']
                elif isinstance(item, str):
                    texto_respuesta += item
            if not texto_respuesta:
                texto_respuesta = str(contenido)
        else:
            texto_respuesta = str(contenido)
        
        st.write("### Respuesta:")
        st.write(texto_respuesta)
        
        with st.expander("📄 Ver fuentes consultadas"):
            for i, doc in enumerate(docs, 1):
                st.write(f"**Fuente {i}:**")
                st.write(doc.page_content[:400] + "...")