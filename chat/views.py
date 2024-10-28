from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from transformers import pipeline
from .models import Document
import PyPDF2
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from django.http import JsonResponse 
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import Document


# Initialize the language model for answering
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

def index_pdf_content(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore

# Chat API view
class ChatAPIView(APIView):
    def post(self, request):
        query = request.data.get('query')
        document = Document.objects.last()
        
        if not document:
            return Response({"error": "No document found"}, status=status.HTTP_404_NOT_FOUND)


        vectorstore = index_pdf_content(document.file.path)
        relevant_docs = vectorstore.similarity_search(query)

        # Extract  the response from LLM
        context = " ".join([doc.page_content for doc in relevant_docs[:3]])  
        response = qa_pipeline(question=query, context=context)

        return Response({"answer": response['answer']}, status=status.HTTP_200_OK)

from django.core.files.storage import default_storage
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response

logger = logging.getLogger(__name__)

@api_view(['POST'])
def YourViewFunction(request):
    try:
        if request.method == 'POST':
            file = request.FILES.get('file')
            logger.debug(f"File received: {file}") 
            
            if not file:
                return Response({'error': 'No file provided'}, status=400)
            
            document = Document.objects.create(file=file)
            logger.debug(f"Document saved: {document.file.url}") 
            return Response({'message': 'File uploaded successfully', 'file_path': document.file.url}, status=201)

    except Exception as e:
        logger.error(f"Error in YourViewFunction: {str(e)}")
        return Response({'error': 'An internal error occurred.'}, status=500)

    return Response({'error': 'Invalid request'}, status=400)
