from flask import (
    Flask, render_template, request,
    session, redirect,
    url_for
)
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv
import requests
import hashlib
import secrets
import os


class Username():
    def __init__(self, username: str, permessi: str):
        self.username = username
        self.permessi = True if permessi == 1 else False


def get_db():
    return mysql.connector.connect(
        host=os.getenv("host"),
        user=os.getenv("user"),
        password=os.getenv("password"),
    )


load_dotenv()


app = Flask(__name__, template_folder="template")
app.secret_key = secrets.token_hex(32)

link = "https://www.opendata.maggioli.cloud/dataset/c8c0ceaf-d8f8-486d-a4de-866a7b52b82a/resource/7492bd8c-038a-4665-a69f-314da39923e0/download/comune-di-grezzana-conteggio-protocolli.csv"

db = get_db()
cur = db.cursor()
you_are_in_school = False


if not you_are_in_school:
    cur.execute("CREATE DATABASE IF NOT EXISTS accounts")
    cur.execute("USE accounts")


def init_db():
    '''
    Docstring for init_db
    create table conteggio_protocolli and users if not yet created
    and populate table users and conteggio_protocolli
    '''
    global db, cur
    cur.execute("""
        CREATE TABLE IF NOT EXISTS conteggio_protocolli (
            id INT AUTO_INCREMENT PRIMARY KEY,
            entrata INT NOT NULL,
            uscita INT NOT NULL,
            anno INT NOT NULL,
            mese nvarchar(32) not null,
            descrizione TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username varchar(32) UNIQUE NOT NULL,
            password varchar(256) NOT NULL,
            is_admin bool not null,
            is_authenticated bool not null,
            last_login DATETIME
        )
    """)

    db.commit()


def encrypt(string: str) -> str:
    h = hashlib.new('sha256')
    h.update(string)
    return h.hexdigest()


def insert_users_accounts():
    global db, cur
    '''
    Se la tabella e' gia popolata, evito di fare ulteriori insert
    (creando account duplicati)
    '''

    cur.execute("SELECT COUNT(*) FROM users")
    count = cur.fetchone()[0]

    if count != 0:
        return

    psw_list = [
        b'admin',
        b'ipsum',
        b'ipsum',
        b'ipsum',
        b'ipsum'
    ]

    psw_crypted = []
    for element in psw_list:
        psw_crypted.append(encrypt(element))

    cur.execute(f"""
        INSERT into users(username, password, is_admin, is_authenticated, last_login)
        values ('admin', '{psw_crypted[0]}', True, False, NULL),
                ('lorem', '{psw_crypted[1]}', False, False, NULL),
                ('mario', '{psw_crypted[2]}', False, False, NULL),
                ('rossi', '{psw_crypted[3]}', False, False, NULL),
                ('ipsum', '{psw_crypted[4]}', False, False, NULL);
    """)


def insert_conteggio_protocolli():
    '''
    Docstring for insert_conteggio_protocolli
    populate the table conteggio protocolli if not yet populated
    '''
    global db, cur

    cur.execute("SELECT COUNT(*) FROM conteggio_protocolli")
    count = cur.fetchone()[0]

    if count != 0:
        return

    text = requests.get(link, verify=False).text

    with open("flussi/dataset.csv", "w") as f_out:
        # tolto il \n aggiuntivo, altrimenti il dataset a doppi \n
        for line in text:
            f_out.write(line.replace("\n", ""))

    csv = text.splitlines()
    rows = csv[1:]

    query = """
        INSERT INTO conteggio_protocolli
        (entrata, uscita, anno, mese, descrizione)
        VALUES (%s, %s, %s, %s, %s)
    """

    data = []
    for row in rows:
        f = [x.replace('"', '') for x in row.split(";")]
        data.append((int(f[0]), int(f[1]), int(f[2]), f[3], f[4]))

    cur.executemany(query, data)
    db.commit()


def valid_login(username: str, password: str) -> list:
    global db, cur

    psw_crypted = encrypt(password.encode())

    cur.execute(f"""
        SELECT username, is_admin
        FROM users
        WHERE username='{username}' and password='{psw_crypted}';
    """)

    # lista di tuple [(), (), ...]
    response = cur.fetchall()
    db.commit()

    return response


def do_login(username, password):
    global db, cur
    response = valid_login(username, password)

    if response == []:
        return render_template("profilo.html", context={"valid": False})

    time_now = datetime.now()
    cur.execute("""
        UPDATE users
        SET last_login = %s, is_authenticated = TRUE
        WHERE username = %s
    """, (time_now, username))
    db.commit()

    response = response[0]
    user = Username(response[0], response[1])
    print(user.permessi)

    session['username'] = user.username
    session['password'] = password
    session['is_admin'] = user.permessi
    session['logged_in'] = True

    # durata sessione 31 giorni
    session.permanent = True

    user_list_table = []

    if user.permessi:
        cur.execute("""
            SELECT id, username, password, is_admin, is_authenticated, last_login
            FROM users;
        """)
        user_list_table = cur.fetchall()

    table_api = cur.execute("""
        SELECT * FROM conteggio_protocolli;
    """)
    table_api = cur.fetchall()

    return render_template("profilo.html", context={
            "valid": True,
            "user": user,
            "table_user": user_list_table,
            "conteggio_protocolli": table_api
        }
    )


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        return do_login(username, password)

    return render_template("login.html")


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    global db, cur

    if not session.get('logged_in'):
        return "Devi essere loggato!", 401

    if not session.get('is_admin'):
        return "Solo amministratori possono eliminare utenti!", 403

    if user_id == session.get('user_id'):
        return "Non puoi eliminare il tuo stesso account!", 400

    try:
        # checkutente esiste
        cur.execute(
            "SELECT username, is_admin FROM users WHERE id = %s",
            (user_id,)
        )
        user = cur.fetchone()

        if not user:
            return "Utente non trovato", 404

        username, is_admin = user

        # non si puo eliminare l'ultimo admin rimanente
        if is_admin:
            cur.execute("SELECT COUNT(*) FROM users WHERE is_admin = TRUE")
            admin_count = cur.fetchone()[0]

            if admin_count <= 1:
                return f"Impossibile eliminare {username}: è l'ultimo amministratore!", 400

        # delet eutente
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        db.commit()

        # back to login
        return redirect(url_for('profile'))

    except Exception as e:
        db.rollback()
        return f"Errore durante l'eliminazione: {str(e)}", 500


@app.route("/update_account/<int:user_id>", methods=["POST"])
def update_account(user_id):
    global db, cur
    if not session.get('logged_in'):
        return "Devi essere loggato!", 401

    if not session.get('is_admin'):
        return "Solo amministratori possono modificare utenti!", 403

    if request.method == "POST":
        new_password = request.form.get("password_update")
        new_password = encrypt(new_password.encode())
        cur.execute("""
            UPDATE users
            SET password = %s, is_authenticated = TRUE
            WHERE id = %s
        """, (new_password, user_id))
        db.commit()

    return do_login(session.get("username"), session.get("password"))


@app.route("/logout")
def logout():
    global db, cur

    # Aggiorna lo stato nel database se c'è un utente loggato
    if session.get('user_id'):
        cur.execute("""
            UPDATE users
            SET is_authenticated = FALSE
            WHERE id = %s
        """, (session['user_id'],))
        db.commit()

    # Cancella la sessione
    session.clear()

    return redirect(url_for('home'))


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    init_db()
    insert_users_accounts()
    insert_conteggio_protocolli()
    app.run(debug=True)
