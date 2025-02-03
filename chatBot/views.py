import os
import tempfile
import base64
import pickle

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from dotenv import load_dotenv

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts.chat import ChatPromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI

from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

load_dotenv()

llm = ChatOpenAI(
    openai_api_key=settings.OPENAI_API_KEY,
    temperature=0,
    model_name='gpt-3.5-turbo',
)

prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided text only.
    Please provide the most accurate responses based on the question.
    If answer cannot find from the context, please reply to the users that the information is not found in the provided documents.

    <context>
    {context}
    <context>
    Questions:{input}
    """
)

DESCRIPTION = '''
A chatbot designed to answer questions directly from your uploaded documents 
'''

def index(request):
    return render(request, 'chatbot/index.html', {'description': DESCRIPTION})


MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'media')

def upload_document(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('document')

        if not uploaded_file:
            messages.error(request, 'No file uploaded.')
            return redirect('index')

        if not uploaded_file.name.endswith('.pdf'):
            messages.error(request, 'Only PDF files are supported.')
            return redirect('index')

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", dir=MEDIA_ROOT) as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            loader = PyPDFLoader(temp_file_path)
            docs = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=200)
            final_documents = text_splitter.split_documents(docs)

            embeddings = HuggingFaceEmbeddings(
                model_name='all-MiniLM-L6-v2'
            )

            vectorstore_path = os.path.join(MEDIA_ROOT, f"{request.session.session_key}_vectorstore.faiss")
            if os.path.exists(vectorstore_path):
                vectors = FAISS.load_local(
                    vectorstore_path,
                    embeddings,
                    allow_dangerous_deserialization=True,
                )
                vectors.add_documents(final_documents)
                vectors.save_local(vectorstore_path)
            else:
                vectors = FAISS.from_documents(final_documents, embeddings)
                vectors.save_local(vectorstore_path)

            request.session['vectorstore_path'] = vectorstore_path

            messages.success(request, 'Document uploaded and processed successfully.')
            return redirect('chat')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('index')

    return redirect('index')


@csrf_exempt
def chat(request):
    if request.method == 'POST':
        user_query = request.POST.get('query')
        if user_query:
            try:
                vectorstore_path = request.session.get('vectorstore_path')
                if not vectorstore_path or not os.path.exists(vectorstore_path):
                    return JsonResponse({'error': 'No documents uploaded.'})

                embeddings = HuggingFaceEmbeddings(
                    model_name='all-MiniLM-L6-v2'
                )
                vectors = FAISS.load_local(
                    vectorstore_path, 
                    embeddings, 
                    allow_dangerous_deserialization=True,
                )

                retriever = vectors.as_retriever()

                qa_chain = load_qa_chain(llm)

                docs = retriever.get_relevant_documents(user_query)

                answer = qa_chain.run(input_documents=docs, question=user_query)

                return JsonResponse({'response': answer})

            except Exception as e:
                return JsonResponse({'error': str(e)})

        return JsonResponse({'error': 'No query provided.'})

    return render(request, 'chatbot/chat.html')

@require_POST
def clear_session(request):
    try:
        request.session.flush()
        messages.success(request, 'Session cleared.')
    except Exception as e:
        messages.error(request, f"Error clearing session: {str(e)}")
    return redirect('index')