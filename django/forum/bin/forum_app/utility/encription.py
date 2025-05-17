from    cryptography.hazmat.primitives              import hashes
from    cryptography.hazmat.primitives.asymmetric   import padding, rsa
from    cryptography.hazmat.backends                import default_backend
from    cryptography.fernet                         import Fernet
from    cryptography.hazmat.primitives              import serialization
from    sqlalchemy                                  import create_engine, inspect, Column, Integer, String, Float, MetaData, Table
from    sqlalchemy.orm                              import sessionmaker, declarative_base
from    typing                                      import Tuple
import  pandas as pd


class Security:
    '''
    * Classe creata da Braga Mattia che serve per crittografare i dati nel database.
    '''
    def __init__(self) -> None:
        pass

    @staticmethod
    def generate(password: str) -> Tuple[str, str]:
        """
            *    Questo metodo genera una coppia di valori: la password crittografata e la chiave di crittografia utilizzata. 
            *    - Parametro:
            *      - password (str): La password in chiaro che deve essere crittografata.
            *    - Ritorna:
            *      - enc_pwd (str): La password crittografata.
            *      - key (str): La chiave di crittografia utilizzata, decodificata in formato UTF-8.
        """
        key = Security.generate_key()
        enc_pwd = Security.encrypt_password(password, key)
        return enc_pwd, key.decode("utf-8")
    
    @staticmethod
    def generate_key() -> bytes:
        """
        *    Questo metodo genera una nuova chiave di crittografia utilizzando la libreria Fernet.
        *    - Ritorna:
        *      - key (bytes): La chiave di crittografia generata.
        """
        return Fernet.generate_key()

    @staticmethod
    def encrypt_password(password: str, key: bytes) -> bytes:
        """
        *    Questo metodo crittografa la password utilizzando la chiave fornita.
        *    - Parametri:
        *      - password (str): La password in chiaro che deve essere crittografata.
        *      - key (bytes): La chiave di crittografia utilizzata per crittografare la password.
        *    - Ritorna:
        *      - encrypted_password (bytes): La password crittografata, decodificata in formato UTF-8.
        """
        f = Fernet(key)
        encrypted_password = f.encrypt(password.encode("utf-8"))
        return encrypted_password.decode("utf-8")
    
    @staticmethod
    def decrypt_password(enc_password: str, key: bytes) -> bytes:
        """
        *   Funzione per decifrare una stringa cifrata
        *   - Parametri: 
        *       - enc_password (str): Password criptata
        *       - key (bytes): chiave per la decriptazione
        *   - Ritorna:
        *       - dec_password (bytes): Password decriptata
        """
        f = Fernet(key)
        dec_password = f.decrypt(enc_password).decode("utf-8")
        return dec_password

    @staticmethod
    def get_strFromDB(db: str, table:str, stringa_enc: str, key: bytes) -> bytes:
        """
        *   Funzione che preleva da un db una stringa e la chiave e le decripta
        *   - Parametri:
        *       - db (str): nome database   
        *       - table (str): nome tabella del database
        *       - stringa_enc(str): stringa criptata del db
        *       - key (bytes): chiave della stringa, serve per capire come decodificarla
        *   - Ritorna:
        *       - stringa decriptata (bytes) oppure se non è riuscito a trovarla da un messaggio di errore (sempre in bytes)
        """
        engine = create_engine(f"sqlite:///{db}")
        df = pd.read_sql_query(f"SELECT * FROM {table}", engine)

        for _, row in df.iterrows():
            db_key_username = row["ukey"].encode("utf-8") # ho avuto problemi di codifica, lasciare utf-8
            db_key_password = row["pkey"].encode("utf-8")

            if row["username"] == stringa_enc and db_key_username == key:
                return Security.decrypt_password(stringa_enc, key)
            
            if row["password"] == stringa_enc and db_key_password == key:
                return Security.decrypt_password(stringa_enc, key)

        return b"Stringa o chiave non trovata"