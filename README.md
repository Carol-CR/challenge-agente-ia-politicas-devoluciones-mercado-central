Dory - Agente de Inteligencia Artificial de Politicas de Atencion al cliente

Descripcion general del proyecto: El asustente de inteligencia, a quien se le hace llamar como 'Dory', desarrollado en python es capaz de responder preguntas sobre un documento PDF de politicas de atencion al cliente, cambios y devoluciones del supermercado Mercado Central 24h, dicho documento fue proporcionado como una sugerencia del propio Alura o programa.

La aplicacion utiliza un entorno RAG, para poder consultar informacion contenida en el documento pdf sin la necesidad de entrenar un llm desde cero.

Esta sumatoria de elementos permite al usuario realizar preguntas relacionadas donde el sistema buscara la informacion mas relevante dentro del documento para generar una respuesta, en caso de no existir dicha informacion se proporciona el numero de servicio donde señalar estas falencia.

Arquitectura de la solucion e intrucciones para ejecutarlo: 
El sistema sigue un flujo de trabajo robusto y escalable:

1. Ingesta de Datos: `PyMuPDF` lee y extrae el texto del documento PDF, preservando la estructura de tablas y secciones.
2.Procesamiento: `RecursiveCharacterTextSplitter` divide el texto en fragmentos manejables (chunks) con solapamiento para no perder contexto.
3. Vectorización: `HuggingFaceEmbeddings` (modelo `all-MiniLM-L6-v2`) convierte el texto en vectores numéricos para su búsqueda semántica.
4. Almacenamiento: `FAISS` actúa como base de datos vectorial local para búsquedas rápidas y eficientes por similitud.
5. Generación: `ChatGoogleGenerativeAI` (modelo Gemini) recibe el contexto recuperado y genera una respuesta natural, precisa y en español.
6. Interfaz: `Streamlit` despliega la aplicación web de forma interactiva, mostrando la respuesta y las fuentes consultadas.

Tecnologias usadas
- Python 3
- Streamlit
- LangChain
- Google Gemini
- FAISS
- HuggingFace Embeddings
- PyMuPDF

Ejemplos de preguntas y respuestas dadas por Dory:
P1: ¿Cuál es el número de la línea gratuita?
R1: De acuerdo con el documento oficial de políticas de Mercado Central 24h, el número de la línea gratuita es:
800-CENTRAL (800-236-8725)
A continuación, se detallan todos los datos y condiciones de este canal de atención especificados en la tabla de canales disponibles:
•	Horario de Atención: Lunes a domingo de 07:00 a 23:00 hrs.
•	Tiempo Máximo de Respuesta: Máximo 5 minutos en espera.
•	Tipo de Solicitud que Atiende: Quejas, reclamaciones, información de políticas y seguimiento de folios.

P2: ¿Qué pasa si encuentro un producto vencido en el anaquel?
R2: Según la Sección 6.3 — Compensación al Cliente por Producto Vencido en Anaquel, si usted detecta un producto con fecha de caducidad vencida en nuestros anaqueles y lo reporta al personal de tienda o al Módulo de Atención, recibirá los siguientes beneficios:
•	Reposición gratuita del mismo producto con fecha de caducidad vigente (o el reembolso del precio si no hay existencia).
•	Bonificación adicional del 10% del valor del producto en puntos VIP Central, como reconocimiento por su colaboración en el programa de calidad.
•	Esta compensación aplica aun si usted no compró el producto vencido, sino que simplemente lo detectó en el anaquel.

P3: ¿Cuánto tiempo tengo para devolver lácteos?
R3: De acuerdo con la política de cambios de Mercado Central 24h (en la sección de categorías de productos, previa a la sección 4.4), para Lácteos y Derivados tienes un plazo de 48 horas desde la compra para realizar la devolución.
Para que la solicitud sea válida, se debe cumplir con la siguiente condición:
El producto debe presentarse con el sello de seguridad sin violar, salvo que el mal estado sea interno y comprobable.

COMENTARIOS
El llm seleccionado pesa un poco mas de lo esperado por lo que puede llegar a usar mas ram de la esperada, provocando que su acceso y reaccion sea un poco tardada

EVIDENCIA DEL DEPLOY en Streamlit Cloud
Enlace publico de la aplicacion desplegada: https://challenge-agente-ia-politicas-devoluciones-mercado-central-d5j.streamlit.app/

<img width="1250" height="597" alt="EvidenciaDeply1" src="https://github.com/user-attachments/assets/f5f188bd-0c8e-4a3b-b8eb-5a750497daa5" />

<img width="1102" height="738" alt="EvidenciaDeploy2" src="https://github.com/user-attachments/assets/0f5711d3-ab74-474c-a638-55b717252428" />


