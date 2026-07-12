import socket
import sys


def main():
    HOST = '0.0.0.0'
    PORT = 4444

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen()
            print(f"[*] Server in ascolto su {HOST}:{PORT}")

            conn, addr = s.accept()
            print(f"[*] Connessione accettata da {addr}")

            output = conn.recv(4096).decode()
            print(f"\n{output}", end='')

            while True:
                command = input("")

                if command.lower() == 'exit':
                    conn.sendall(command.encode())
                    break

                conn.sendall(command.encode())

                output = conn.recv(4096).decode()
                print(f"\n{output}", end='')

    except KeyboardInterrupt:
        print("\n[*] Server chiuso.")
    except Exception as e:
        print(f"[!] Errore: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
