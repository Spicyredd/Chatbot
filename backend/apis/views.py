from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import APIModel
from .serializer import APISerializer, APIFileSerializer
from .ai.geminiModel import GeminiModel
from django.core.cache import cache
import dill
import os
from django.conf import settings
import pdfplumber
import faiss
from langchain_community.vectorstores import FAISS, DistanceStrategy
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain.text_splitter import RecursiveCharacterTextSplitter
import asyncio

# Create your views here.

def setVectorStore(pdfName):
        file_path = os.path.join(settings.MEDIA_ROOT, 'files', pdfName.replace(' ', '_'))
    
        # pdf_reader = pdfplumber .PdfReader(file_path)
        # # pdfplumber.pd

        # # Extract text from each page
        # pdf_text = ""
        # for page in pdf_reader.pages:
        #     pdf_text += page.extract_text()
        
        with pdfplumber.open(file_path) as pdf:
            pdf_text = " ".join(page.extract_text() or "" for page in pdf.pages)

        # with open('pdf.txt', 'w') as f:
        #     f.write(pdf_text)
        sentenceTransformer = HuggingFaceEmbeddings(model_name='    ')
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )

        texts = text_splitter.create_documents([pdf_text])
        # print(texts)

        # vectorStore = FAISS(
        #     embedding_function=sentenceTransformer,
        #     index=index,
        #     docstore=InMemoryDocstore(),
        #     index_to_docstore_id={}
        # )
        vectorStore = FAISS.from_documents(documents=texts, embedding=sentenceTransformer,distance_strategy=DistanceStrategy.COSINE)

        vectorStore.add_documents(texts)
        # vectorRetriever = vectorStore.as_retriever()
        return vectorStore


class APIModelGetView(APIView):
    def get(self, request):
        records = APIModel.objects.all().order_by('created_at')
        serializer =APISerializer(records, many=True, context={'request': request})
        # print(serializer.error_messages)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class APIModelPostView(APIView):
    def post(self, request):
        serializer = APISerializer(data=request.data, context = {'request': request})
        if serializer.is_valid():
            serializer.save()
            newModel = GeminiModel()
            if str(request.data['toggle']) == "true":
                toggle = True
            else:
                toggle = False
            if toggle:
                response = asyncio.run(newModel.response(request.data['message'], True))
            else:
                response = asyncio.run(newModel.response(request.data['message']))
            APIModel.objects.create(sender="gemini", message=response)
            messages = APIModel.objects.all().order_by('created_at')
            serializer = APISerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class APIModelFilePostView(APIView):
    def post(self, request):
        serializer = APIFileSerializer(data=request.data, context = {'request':request})
        if serializer.is_valid():
            serializer.save()
            vectorStore = setVectorStore(str(request.data['pdf']))
            cache.set('vectorStore', dill.dumps(vectorStore))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)