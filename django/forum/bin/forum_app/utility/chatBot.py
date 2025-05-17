# from langchain_core.prompts import ChatPromptTemplate
from langchain_groq             import ChatGroq
from langchain_core.messages    import HumanMessage, SystemMessage
from sqlalchemy                 import create_engine, inspect, Column, Integer, String, Float
from sqlalchemy.orm             import sessionmaker, declarative_base
from datetime                   import datetime
from .general                   import detect_encoding_file
import time
import os


def searchDb(startPath):
    dir_path = os.path.dirname(startPath)

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('trace.db'):
                return root + '/' + str(file)


pathPhisicalDB = searchDb("../")


class Model:
    school_info             = open("./forum_app/instChatbot/prompt.txt", "r", encoding = detect_encoding_file("./forum_app/instChatbot/prompt.txt")).read() 
    additional_instructions = open("./forum_app/instChatbot/additionalInst.txt", "r", encoding = detect_encoding_file("./forum_app/instChatbot/additionalInst.txt")).read()

    def __init__(self, groq_api_key: str, language: str = "english"):
        '''
        *   @_system_content -> viene creato una sola volta e aggiornato solo se necessario (questo consente di risparmiare tempo). 
        '''
        self.llm                     = ChatGroq(temperature=0.7, groq_api_key=groq_api_key, model_name="llama-3.1-8b-instant")
        self.language                = language
        self.school_info             = Model.school_info
        self.additional_instructions = Model.additional_instructions
        self._system_content         = self._create_system_content()  # crea il prompt iniziale una sola volta
    
    def _create_system_content(self):
        '''*
        *   Costruisce il messaggio di sistema (system_content) di base. 
        *   Questo messaggio fornisce al modello l'istruzione iniziale su come rispondere (tonalità e tipo di contenuto)
        *'''
        
        return f"""You are a helpful assistant on a school community home page.
You are responsible for answering questions about the school's courses, events, announcements, and general information.
Respond in {self.language}. 
Be concise, friendly, and engaging.

School Information:
{self.school_info}

Additional Instructions:
{self.additional_instructions}

Always maintain a positive and supportive tone, and prioritize the well-being and education of students."""
        
    def update_context(self, school_info = None, additional_instructions = None):
        '''*
        *   Funzione per aggiornare dinamicamente i valori di school_info o additional_instructions senza creare una nuova istanza.
        *   Viene usata quando si devono modificare i dati o aggiungere nuove istruzioni
        *'''
        # Aggiorna solo se ci sono nuovi dati
        if school_info is not None:
            self.school_info = school_info

        if additional_instructions is not None:
            self.additional_instructions = additional_instructions

        # Ricrea il prompt base
        self._system_content = self._create_system_content()
    
    
    async def chat(self, msg: str):
        '''*
        * Funzione per interagire con il modello
        *'''
        if not msg:
            raise ValueError("Please provide a message to chat with the bot.")
        
        # Usa il prompt creato una sola volta
        messages = [
            SystemMessage(content = self._system_content),
            HumanMessage(content = msg)
        ]

        response = await self.llm.ainvoke(messages)
        return response.content


class LogBot():
    Base = declarative_base()
    def __init__(self, question:str, answer:str, db_path=pathPhisicalDB):
        
        self.__engine       = create_engine(f"sqlite:///{db_path}")
        self.__session      = sessionmaker(bind = self.__engine)()

        self.__question     = question
        self.__answer       = answer
        self.__timestamp    = time.time()
        self.__timenow      = datetime.now()

        if not inspect(self.__engine).has_table("chatBotDB"):
            LogBot.Base.metadata.create_all(bind=self.__engine)()

    def logMe(self):
        if not inspect(self.__engine).has_table("chatBotDB"):
            LogBot.Base.metadata.create_all(bind=self.__engine)()
        self.__session.add(LogBotDB(self))
        self.__session.commit()

    def get_question(self):
        return self.__question
    
    def get_answer(self):
        return self.__answer

    def get_timestamp(self):
        return self.__timestamp
    
    def get_timenow(self):
        return self.__timenow

    def __str__(self):
        return f"Domanda: {self.__question}\nRisposta: {self.__answer}\nData: {self.__timenow}"


class LogBotDB(LogBot.Base):
    __tablename__ = "chatBotDB"

    id          = Column(Integer, primary_key=True)
    timestamp   = Column(String)
    orario      = Column(String)
    question    = Column(String)
    answer      = Column(String)

    def __init__(self, chatbotSession:object):
        self.timestamp  = chatbotSession.get_timestamp()
        self.orario     = chatbotSession.get_timenow()
        self.question   = chatbotSession.get_question()
        self.answer     = chatbotSession.get_answer()
