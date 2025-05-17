
from sqlalchemy import create_engine, inspect, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base


from datetime import datetime
import platform
import time
import sys
import os


"""
*   Modulo creato da: Federico Bastianello
*   versione: 1.0.1
*   modulo per il Log di un programma
"""


class Log():
    Base = declarative_base()

    def __init__(self, db_path="./log/trace.db"):
        self.__engine       = create_engine(f"sqlite:///{db_path}")
        self.__session      = sessionmaker(bind = self.__engine)()

        self.__percorso     = os.path.abspath("./")
        self.__file_name    = sys.argv[0]
        self.__username     = os.environ['USERNAME' if platform.system() == 'Windows' else 'USER']
        self.__pcname       = platform.node()
        self.__sysVersion   = sys.version
        self.__timestamp    = time.time()
        self.__timenow      = datetime.now()

    def logMe(self, message):
        if not inspect(self.__engine).has_table("log"):
            Log.Base.metadata.create_all(self.__engine)

        self.__session.add(LogDB(self, message))
        self.__session.commit()

    def get_file_name(self):
        return self.__file_name

    def get_username(self):
        return self.__username

    def get_pcname(self):
        return self.__pcname

    def get_sysVersion(self):
        return self.__sysVersion

    def get_timestamp(self):
        return self.__timestamp
    
    def get_timenow(self):
        return self.__timenow

    def get_message(self):
        return self.__message

    def __str__(self):
        info = f"percorso log: {self.__percorso}\n"
        info += f"{self.__file_name}\n"
        info += f"{self.__username}\n"
        info += f"{self.__pcname}\n"
        info += f"{self.__sysVersion}\n"
        info += f"{self.__timestamp}\n"
        info += f"{self.__timenow}\n"
        return info


class LogDB(Log.Base):
    __tablename__ = "log"

    id          = Column(Integer, primary_key=True)
    file_name   = Column(String)
    username    = Column(String)
    pcname      = Column(String)
    sysverion   = Column(String)
    timestamp   = Column(String)
    orario      = Column(String)
    message     = Column(String)

    def __init__(self, log:object, message:str):
        self.file_name  = log.get_file_name() 
        self.username   = log.get_username()
        self.pcname     = log.get_pcname()
        self.sysverion  = log.get_sysVersion()
        self.timestamp  = log.get_timestamp()
        self.orario     = log.get_timenow()
        self.message    = message


class LogBot():
    """
    *    Creo una tabella nel db trace.db esclusivamente per loggare domande e risposte dell'app chatbot
    """
    Base = declarative_base()
    def __init__(self, question:str, answer:str, db_path="./log/trace.db"):
        self.__engine       = create_engine(f"sqlite:///{db_path}")
        self.__session      = sessionmaker(bind = self.__engine)()

        self.__question     = question
        self.__answer       = answer
        self.__timestamp    = time.time()
        self.__timenow      = datetime.now()

        if not inspect(self.__engine).has_table("chatBotDB"):
            LogBot.Base.metadata.create_all(bind=self.__engine)()

    def logMe(self):
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
        return f""
