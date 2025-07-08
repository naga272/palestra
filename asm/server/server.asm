
%macro STARTFOO 0
        endbr64
        push rbp
        mov rbp, rsp
%endmacro

%macro GXOR 0
        xor rax, rax
        xor rbx, rbx
        xor rcx, rcx
        xor rdx, rdx
%endmacro


%define AF_INET 2       ; IPV4
%define SOCK_STREAM 1   ; connessione TCP

section .bss
        buffer resb 1024

section .data
        argc dq 1
        argv dq 1
        envp dq 1


        sockaddr_in:
                .sin_family:     db AF_INET, 0x00       ; 4 bytes
                .sin_port:       db 0x23, 0x28          ; porta 9000 (in big endian)
                .ip_addr:        db 127, 0, 0, 1        ; 4 bytes
                .pad:            dq 0x00, 0x00          ; padding di 16 bytes
        end_sockaddr_in:
 
        msg_err_socket  db "Impossibile creare la socket", 0
        msg_err_bind    db "impossibile assegnare la porta e ip", 0
        msg_err_listen  db "Impossibile mettersi in ascolto", 0
        msg_err_accept  db "Impossibile accettare la connessione", 0
        msg_accept      db "connessione accettata", 0

        response db "HTTP/1.1 200 OK", 13, 10
                 db "Content-Type: text/html", 13, 10
                db "Content-Length: 53", 13, 10
                db 13, 10
                db "<html><body><h1>Lorem Ipsum dolorem</h1></body></html>", 0

section .text
        global _start

%define len_sockaddr_in end_sockaddr_in         - sockaddr_in
%define off_sin_family  sockaddr_in.sin_family  - sockaddr_in
%define off_sin_port    sockaddr_in.sin_port    - sockaddr_in
%define off_ip_addr     sockaddr_in.ip_addr     - sockaddr_in
%define off_pad         sockaddr_in.pad         - sockaddr_in


; long strlen(char* rdi)
strlen:
    STARTFOO
    xor rcx, rcx
    not rcx             ; rcx = -1 (massimo valore)
    xor al, al          ; al = 0 (terminatore)
    mov rdi, rdi        ; indirizzo della stringa
    repne scasb         ; cerca \0 in rdi
    not rcx             ; lunghezza = ~rcx
    dec rcx             ; escludi terminatore
    mov rax, rcx
    leave
    ret


; int print(char* rdi);
print:  STARTFOO
        call strlen
        mov rdx, rax
        mov rax, 1
        mov rsi, rdi
        mov rdi, 1
        syscall

        mov rax, rdx
        leave
        ret


; int socket(int rdi, int rsi, int rdx)
socket: ; funzione che restituisce un file descriptor
        ; rax >= 0 IF OK
        STARTFOO
        mov rax, 41
        syscall
        test rax, rax
        js .error
        
        leave
        ret
        .error: mov rdi, msg_err_socket
                call print

                mov rdi, 1
                call _exit


; int bind(int sock_fd, struct sockaddr_in* rsi, size_t rdx);
bind:   ; funzione che assegna ip e porta
        ; rax == 0 if OK
        STARTFOO
 
        mov rax, 49
        syscall
        test rax, rax
        js .error
        leave
        ret

        .error: mov rdi, msg_err_bind
                call print
                mov rdi, 1
                call _exit


; int listen(int socket_fd, int backlog)
listen: ; consente a una socket di mettersi in modalita di ascolto per accettare
        ; connessioni in arrivo
        ; ret: rax == 0 if OK 
        STARTFOO
 
        mov rax, 50
        syscall
        test rax, rax
        js .error

        leave
        ret

        .error: mov rdi, msg_err_listen
                call print
                mov rdi, 1
                call _exit


; int accept(int sock_fd, struct sockaddr_in* rsi, size_t rdx); 
accept: ; quando arriva una richiesta, accept restituisce un nuovo fd
        ; ret: rax >= 0 IF OK
        STARTFOO
        mov rax, 43
        syscall 
        test rax, rax
        js .error

        leave
        ret
        .error: mov rdi, msg_err_accept
                call print
                mov rdi, 1
                call _exit


close:  ; chiusura fd 
        STARTFOO
        mov rax, 3
        syscall
        leave
        ret


main:   STARTFOO
        mov rdi, AF_INET
        mov rsi, SOCK_STREAM
        mov rdx, 0x00
        call socket
        mov r9, rax                     ; salvo in r9 il fd

        mov rdi, r9                     ; socket fd
        mov rsi, sockaddr_in            ; (struct sockaddr_in*) &rsi
        mov rdx, len_sockaddr_in        ; sizeof(struct sockadd_in)
        call bind

        mov rdi, r9     ; socket fd
        mov rsi, 10     ; numero massimo di client che si mettono in coda sul socket
        call listen     
        .loop:  ; in c quivalente a:
                ; int new_fd = accept(fd, NULL, NULL);
                mov rdi, r9
                xor rsi, rsi
                xor rdx, rdx
                call accept
                mov r10, rax

                mov rdi, msg_accept
                call print

                ; lettura del fd del client (restituito da accept)
                mov rdi, r10
                mov rax, 0
                mov rsi, buffer
                mov rdx, 1024
                syscall

                mov rdi, response
                call strlen
                mov rdx, rax            ; len msg HTTP
                mov rdi, r10             ; fd client
                mov rsi, response       ; msg HTTP
                mov rax, 1              ; sysWrite
                syscall
                
                mov rdi, r10
                call close

                jmp .loop

        mov rax, 0
        leave
        ret


_start: endbr64
        mov [argc], rdi
        mov [argv], rsi
        mov [envp], rdx
        GXOR
        call main
        mov rdi, rax
        call _exit


_exit:  endbr64
        mov rax, 60
        syscall

