#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

from sqlalchemy         import create_engine, inspect, Column, Integer, String, Float, MetaData, Table
from sqlalchemy.orm     import sessionmaker, declarative_base

from forum_app.utility.general  import detect_encoding_file, last_version
from datetime           import datetime
from log                import Log

import threading
import shutil
import time
import sys
import os
import re


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forum.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


Base = declarative_base()


class BanWordDB(Base):
    __tablename__ = "BanWord"

    id = Column(Integer, primary_key=True)
    word = Column(String)

    def __init__(self, word: str):
        self.word = word


def task(dir_ban_word: str):
    '''
    *   Questa Procedura ogni 5 minuti controlla se ci sono file all'interno della directory
    *   ../flussi. Se ci sono legge tutti i file al suo interno per inserirli all'interno 
    *   della tabella BanWord. La tabella è visibile anche dalla suite admin di django
    '''
    engine = create_engine("sqlite:///./db.sqlite3")
    Session = sessionmaker(bind=engine)
    session = Session()

    if not inspect(engine).has_table("BanWord"):
        Base.metadata.create_all(engine)

    while True:
        try:
            for filename in os.listdir(dir_ban_word):       # lista file dentro la cartella dir_ban_word
                file_path = os.path.join(dir_ban_word, filename)
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, "r", encoding = detect_encoding_file(file_path)) as f_in:
                            for row in f_in.read().split("\n"):
                                if not re.match(r"\s*\n*", row):
                                    session.add(BanWordDB(row.upper()))
                            session.commit()

                        if os.path.isfile(file_path):  # dopo aver registrato il contenuto del file, elimino il file che non serve più
                            os.remove(file_path)
                            Log().logMe(f"File {file_path} rimosso.")
                        else:
                            Log().logMe(f"Warning: {file_path} non è un file all'interno {dir_ban_word}")

                    except (UnicodeDecodeError, 
                            FileNotFoundError, 
                            IsADirectoryError) as e:  # caso in cui non sono riuscito a codificare
                        Log().logMe(f"Impossibile decodificare {file_path}: {e}")
        except Exception as e:  # caso in cui l'errore non è stato causato da un problema di codifica del file
            Log().logMe(f"Si è verificato un errore non di codifica: {e} in {dir_ban_word}")

        time.sleep(60 * 2)  # ogni 2 minuti controlla dentro la cartella dir_ban_word


if __name__ == "__main__":
    '''
    Per il momento questa parte non ci serve
    if "runserver" in sys.argv: 
        # avvio il thread solo se viene avviato il server, non durante le altre situazioni come la makemigrations, migrate ecc...
        scheduling = threading.Thread(target = task, args = ("../flussi",))
        scheduling.daemon = True
        scheduling.start()
    '''
    Log().logMe(f"versione server {last_version('../CHANGELOG.txt')} avviato")
    main()
