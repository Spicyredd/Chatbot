from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.runnable import RunnableMap
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from django.core.cache import cache
import dill
from googletrans import Translator
class GeminiModel:
    def __init__(self):
        dillObject = cache.get('vectorStore')
        if dillObject:
            self.vectorStore = dill.loads(dillObject) # Placeholder for the FAISS store
        else:
            self.vectorStore = None
        
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
        self.translator = Translator()
        
    
    async def response(self, query, toggle=False):
        if self.vectorStore:
            # temp = await self.translator.translate(query, dest="ne")
            # query = temp.text
            # Answer the question as based on the following context:
            template = """
            You are an AI assistant trained to answer questions based on the provided document excerpts. Use the following context to answer the question:

            Context:
            {context}

            Question: {question}

            Please provide a concise and accurate answer based on the context above.
            """

            prompt = ChatPromptTemplate.from_template(template)
            output_parser = StrOutputParser()

            
            print(self.vectorStore.similarity_search_with_score(query, k=10))
            self.chain = RunnableMap({
            "context": lambda x: self.vectorStore.similarity_search(x['question'], k=10),
            "question": lambda x: x['question']
            }) | prompt | self.llm | output_parser
            response = self.chain.invoke({"question": query})
            if toggle:
                response = await self.translator.translate(response, dest="ne")
                return response.text
            return response
        
        template= """
        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)
        output_parser = StrOutputParser()
        self.chain = RunnableMap({
        "question": lambda x: x['question']
        }) | prompt | self.llm | output_parser
        response = self.chain.invoke({"question":   query})
        if toggle:
                response = await self.translator.translate(response, dest="ne")
                return response.text
        return response