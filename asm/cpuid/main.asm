
%macro gxor 0
        xor rax, rax
        xor rbx, rbx
        xor rcx, rcx
        xor rdx, rdx
%endmacro

%define __WIN64

%ifdef __WIN64
        extern GetStdHandle
        extern WriteConsoleA
        extern ExitProcess
%endif

section .bss
        cpu_name resb 49 ; usato per ottenere il nome della cpu

%ifdef __WIN64 
        written resd 1 ; lo uso per WriteConsoleA
%endif

section .data
        NL              db 0x0d, 0x0a, 0x00
        sse_msg         db "SSE supported", 0x00
        sse2_msg        db "SSE2 supported", 0x00
        sse3_msg        db "SSE3 supported", 0x00
        ssse3_msg       db "SSSE3 supported", 0x00
        sse4_msg        db "SSE4.1 supported", 0x00
        avx_msg         db "AVX supported", 0x00
        avx2_msg        db "AVX2 supported", 0x00
        avx512_msg      db "AVX-512 supported", 0x00

section .text
        global _start


strlen:
    endbr64
    push rdi
    xor rcx, rcx
    not rcx
    xor al, al
    repne scasb
    not rcx
    dec rcx
    mov rax, rcx
    pop rdi
    ret


;void print(char* rdi);
print:  endbr64
        push rbp
        mov rbp, rsp

        call strlen
        mov rdx, rax

        %ifdef __WIN64 ; caso windows x86_64
                mov r8, rdx
                mov ecx, -11
                call GetStdHandle
                mov rcx, rax                ; rcx = handle
                mov rdx, rsi                ; rdx = stringa
                lea r9, [written]           ; r9 = puntatore a n. caratteri scritti
                sub rsp, 32                 ; shadow space obbligatoria
                call WriteConsoleA
                add rsp, 32

                ; --- Stampa newline ---
                mov ecx, -11
                call GetStdHandle
                mov rcx, rax
                lea rdx, [rel NL]
                mov r8, 3
                lea r9, [written]

                sub rsp, 32
                call WriteConsoleA
                add rsp, 32
        %else   ; caso linux
                mov rax, 1
                mov rsi, rdi
                mov rdi, 1
                syscall

                mov rdi, 1
                mov rsi, NL
                mov rdx, 3
                mov rax, 1
                syscall
        %endif
        leave
        ret


get_name_cpu: 
        endbr64
        push rbp
        mov rbp, rsp

        ; CPUID 0x80000002
        mov eax, 0x80000002
        cpuid
        mov [rdi], eax
        mov [rdi+4], ebx
        mov [rdi+8], ecx
        mov [rdi+12], edx

        ; CPUID 0x80000003
        mov eax, 0x80000003
        cpuid
        mov [rdi+16], eax
        mov [rdi+20], ebx
        mov [rdi+24], ecx
        mov [rdi+28], edx

        ; CPUID 0x80000004
        mov eax, 0x80000004
        cpuid
        mov [rdi+32], eax
        mov [rdi+36], ebx
        mov [rdi+40], ecx
        mov [rdi+44], edx

        ; null terminator
        mov byte [rdi+48], 0x00
        mov rax, rdi
        leave
        ret


main:   endbr64
        push rbp
        mov rbp, rsp

        mov rdi, cpu_name
        call get_name_cpu

        ; stampa stringa
        mov rdi, rax
        call print

        ; ecx: SSE3, SSSE3, SSE4.1, AVX
        ; edx: SSE, SSE2
        ; bt serve èper testare se il flag in edx e' settato a uno oppure no
        ; se lo e' significa che la cpu supporta quel tipo di ottimizzazioni
        mov eax, 1
        cpuid
        
        mov r8d, edx
        mov r9d, ecx
        bt r8d, 25 ; caso SSE
        jc .sse_supported
        .checked_sse:
                bt r8d, 26
                jc .sse2_supported
        .checked_sse2:
                bt r9d, 0
                jc .sse3_supported
        .checked_sse3:
                bt r9d, 9
                jc .ssse3_supported
        .checked_ssse3:
                bt r9d, 19
                jc .sse4_1_supported
        .checked_sse4_1:
                bt r9d, 28
                jc .avx_supported
        .checked_avx:
                ; verifica AVX2, AVX-512
                mov eax, 7
                xor ecx, ecx
                xor ebx, ebx
                cpuid
                mov r8d, ebx

                bt r8d, 5
                jc .avx2_supported
        .checked_avx2:
                bt r8d, 16
                jc .avx512_supported
        .checked_avx512:
        jmp .done

        .sse_supported:
                mov rdi, sse_msg
                call print
                jmp .checked_sse
        .sse2_supported:
                mov rdi, sse2_msg
                call print
                jmp .checked_sse2
        .sse3_supported:
                mov rdi, sse3_msg
                call print
                jmp .checked_sse3
        .ssse3_supported:
                mov rdi, ssse3_msg
                call print
                jmp .checked_ssse3
        .sse4_1_supported:
                mov rdi, sse4_msg
                call print
                jmp .checked_sse4_1
        .avx_supported:
                mov rdi, avx_msg
                call print
                jmp .checked_avx
        .avx2_supported:
                mov rdi, avx2_msg
                call print
                jmp .checked_avx2
        .avx512_supported:
                mov rdi, avx512_msg
                call print
                jmp .checked_avx512
        .done:  mov rax, 0
                leave
                ret


_start: endbr64
        gxor
        call main
_exit:  endbr64
        %ifdef __WIN64
                mov rcx, rax
                call ExitProcess
        %else
                mov rdi, rax
                mov rax, 60
                syscall
        %endif
