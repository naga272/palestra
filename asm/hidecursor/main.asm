section .data
    hidecursor  db 27, '[?25l', 0
    showcursor  db 27, '[?25h', 0
    message     db 'Hello, terminal. Your cursor is gone...', 10, 0

section .text
    global _start

_start:
    ; write(1, hidecursor, strlen(hidecursor))
    mov rax, 1          ; syscall: write
    mov rdi, 1          ; fd: stdout
    mov rsi, hidecursor
    call strlen
    mov rdx, rax        ; length from strlen
    mov rax, 1
    syscall

    ; write(1, message, strlen(message))
    mov rax, 1
    mov rdi, 1
    mov rsi, message
    call strlen
    mov rdx, rax
    mov rax, 1
    syscall

    ; sleep(2) → syscall: nanosleep
    ; struct timespec: { 2, 0 } → 2 secondi, 0 nanosecondi

    mov rax, 35         ; syscall: nanosleep
    lea rdi, [rel req]
    xor rsi, rsi        ; NULL (no remaining time)
    syscall

    ; write(1, showcursor, strlen(showcursor))
    mov rax, 1
    mov rdi, 1
    mov rsi, showcursor
    call strlen
    mov rdx, rax
    mov rax, 1
    syscall

    ; exit(0)
    mov rax, 60
    xor rdi, rdi
    syscall

; strlen: calcola lunghezza della stringa null-terminata
strlen:
    push rsi
    xor rax, rax
.next:
    cmp byte [rsi + rax], 0
    je .done
    inc rax
    jmp .next
.done:
    pop rsi
    ret


section .data

    req:
        dq 2          ; tv_sec = 2
        dq 0          ; tv_nsec = 0
