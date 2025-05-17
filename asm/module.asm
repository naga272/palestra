;***** FUNCTION SECTION *****;
; ordine del passaggio dei parametri secondo lo standard V_ABI
; se il num di parametri supera il numero di registri i restanti parametri vengono pushati nello stack
; SV_ABI = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]
; NB: supporto a AVX

; void putchar(fd, char);
putchar:endbr64    
        push rbp
        mov rbp, rsp

        mov rax, 1
        mov rsi, rdi
        mov rdi, rsi
        mov rdx, 1
        syscall

        leave
        ret


; unsigned int len_array(char* rdi)
strlen:
    endbr64
    push rbp
    mov rbp, rsp
    xor rax, rax                        ; offset vettore    
    .ciclo: 
        prefetcht0[rdi + rax]           ; sposto nella cache l1
        vmovdqu ymm0, [rdi + rax]       ; sposto rdi + rax e i 256 bit successivi in ymm0  
        vpxor ymm1, ymm1, ymm1          ; azzero i bit di ymm1
        vpcmpeqb ymm2, ymm0, ymm1       ; inserisco in ymm2 il risultato del contronto  
        vpmovmskb ecx, ymm2              ; ottengo una maschera a 32 bit 
        test ecx, ecx 
        jnz .found_zero

        add rax, 32
        jmp .ciclo
    
    .found_zero:
        tzcnt ecx, ecx
        add rax, rcx
        leave
        ret


; unsigned int print(const char*);
print:  endbr64
        push rbp
        mov rbp, rsp

        mov rsi, rdi 

        mov rdi, rsi 
        call strlen
        mov rcx, rax

        mov rdx, rax
        mov rax, 1
        mov rdi, stdout
        syscall

        .done:  
            ; return a capo
            mov rax, 1
            mov rsi, 0x0d
            mov rdx, 1
            mov rdi, 1 
            syscall

            mov rax, 1
            mov rsi, 0x0a
            mov rdx, 1
            mov rdi, 1
            syscall
            mov rax, rcx
            mov rsp, rbp
            leave
            ret


; int readchar(unsigned int fd, char);
readchar:
        ; var = readchar(stdin, carattere)
        ;            --- oppure ---
        ; var = readchar(file_fd, carattere)
        endbr64
        push rbp
        mov rbp, rsp

        xor rax, rax
        mov rax, [rbp + 32] ; sizeof(fd) == 4 bytes

        ; controllo che il fd passato come argomento non sia negativo, 
        ; in caso contrario restituisco il valore della macro EXIT_FAILURE
        mov rcx, 0
        sub rcx, rax
        js .bad_end

        xor rsi, rsi
        mov rdi, rax
        mov rax, 0
        syscall

        mov rax, rsi
        jmp .end_read

    .bad_end:
        mov rax, EXIT_FAILURE

    .end_read:
        mov rsp, rbp
        leave
        ret


; unsigned int len_array(const char*)
len_array:  
        endbr64
        push rbp
        mov rbp, rsp
        
        xor rax, rax

        .ciclo: cmp byte[rdi + rax], 0
                je .done
                
                prefetcht0[rdi * 8]
                inc rax
                jmp .ciclo
        .done:  mov rsp, rbp
                leave
                ret


; int fprint(int fd, size_t n, char *caratteri);
fprint: 
        ; funzione per la scrittura di n caratteri sul fd
        endbr64
        push rbp
        mov rbp, rsp
        
        ; da completare
        mov rcx, rdi
        mov rdi, rdx ; primo param
        mov rdx, rsi ; terzo param
        mov rsi, rcx ; secondo param

        mov rax, 1
        syscall

        mov rax, EXIT_SUCCESS   ; non ricorso che stavo facendo
        mov rbp, rsp
        leave
        ret


; int mkdir(const char* path, umode_t mode)
mkdir:  endbr64 ; funzione per la creazione di una directory
        push rbp                
        mov rbp, rsp            

        mov rax, 83
        syscall

        cmp rax, EXIT_SUCCESS
        je .fine

        ; bad ending
        mov rax, EXIT_FAILURE 
        jmp .done

        .fine:  ; good ending
            mov rax, EXIT_SUCCESS

        .done:
            mov rsp, rbp
            ret


; int print_int(int n);
print_int:	; funzione che stampa a schermo un numero intero,
    ; accetta come parametro un solo intero
    endbr64
    push rbp
    mov rbp, rsp

    mov rax, rdi         ; carico l'intero passato come argomento

    mov rcx, digitSpace	        ; carico l'indirizzo di digitSpace (e' un vettore di 100 elementi)	
    mov rbx, 10		            ; base 10
    mov [rcx], rbx              ; inizializzo la base nel buffer 
    inc rcx                     ; avanzo la posizione del buffer
    mov [digitSpacePos], rcx    ; salvo la posizione

    .st_loop:	
        xor rdx, rdx		; mi preparo per la divisione
        div rbx			    ; divido il contenuto di rax per rbx
        push rax		    ; salvo il quoziente nello stack (il resto si trova in rdx)
        add rdx, 48         ; (0 <= rdx <= 9) + 48, mi consente di trovare il carattere ascii che corrisponde al numero

        mov rcx, [digitSpacePos]    ; carico la posizione corrente nel buffer
        mov [rcx], dl               ; il carattere lo vado a memorizzare nel buffer
        inc rcx
        mov [digitSpacePos], rcx    ; vado ad aggiornale la posizione

        pop rax
        cmp rax, 0                  ; se il quoziente risulta 0 significa che ho finito 
        jne .st_loop

    ; a questo punto digitSpace contiene il numero in ordine inverso (centinaia, decine, unita') -> (unita', decine, centinaia)
    .end_loop:
        mov rax, 1
        mov rdx, 1
        mov rdi, 1
        mov rsi, rcx
        syscall			

        mov rcx, [digitSpacePos]
        dec rcx

        mov [digitSpacePos], rcx

        cmp rcx, digitSpace
        jge .end_loop

        mov rax, EXIT_SUCCESS
        leave
        ret


; int fread_all(char *filename)
fread_all:
	;	Funzione che legge e stampa il contenuto del file passato come parametro	
	;	Restituisce 1 se qualcosa è andato storto, 0 se è andato tutto bene.
	endbr64
    push rbp
	mov rbp, rsp

    mov rax, qword [rdi]   ; Legge il parametro passato (path del file)
    FOPEN rax, O_RDONLY, 0o000  ; Macro per chiamare `open`
	test rax, rax
	js .error

    push rax

    sub rsp, 256  ; 1 byte solo per buff
	.repeat:  
        mov rsi, rsp            ; n char da prendere in input
		mov rdi, rax	        ; sposto il fd in rdi
		mov rax, 0              ; syscall SYS_READ
		mov rdx, 256            ; LEN
		syscall 

        cmp rax, 0              ; abbiamo raggiunto l'EOF
        je .eof

        mov rdx, rax            ; numero di byte letti
        mov rax, 1              ; syscall SYS_WRITE
        mov rdi, stdout         ; fd STDOUT
        mov rsi, rsp   
        syscall

	    jmp .repeat
	
	.eof:	
        add rsp, 256            ; dealloco la memoria dallo stack
        pop rax                 ; mi riprendo il fd del file per chiuderlo

        FCLOSE rax
		mov rax, EXIT_SUCCESS
		leave
		ret

	.error: leave
		; push msg_error_read
		; call print
		mov rax, 60
		mov rdi, EXIT_FAILURE
		syscall


; DA COMPLETARE 
writef:	
    endbr64
    push rbp
	mov rbp, rsp

    mov rax, rdi
	FOPEN rax, O_WRONLY, 0o666
	test rax, rax
	js .error


	FCLOSE rax

	mov rax, EXIT_SUCCESS
	leave
	ret

	.error: 
		; push msg_error_write
		; call print
		leave
        mov rax, 60
		mov rdi, EXIT_FAILURE
        xor rsi, rsi
        syscall


; void exit(register int rdi);
exit:   endbr64
        mov rdi, rax
        mov rax, 60     
        syscall


; pid_t fork(void);
fork:   endbr64
        mov rax, 57
        syscall
        ret


; pid_t getpid(void);
getpid: endbr64
        mov rax, 39
        syscall
        mov rax, rax
        ret
    
    
; int rmdir(const char *);
rmdir: endbr64
        push rbp
        mov rbp, rsp
    
        mov rax, 84
        mov rsi, rdi
        syscall
    
        test rax, rax
        js  .error
    
        mov rax, 1
        jmp .end
    
        .error:
            mov rax, errno
            mov dword [rax], 2
            mov rax, EXIT_FAILURE
        .end:
            mov rsp, rbp
            leave
            ret


; int renamedir(const char* oldpath, const char* newpath);
renamedir: endbr64
        push rbp
        mov rbp, rsp
    
        mov rax, 82             ; sys_rename
        syscall
    
        test rax, rax
        js  .error
    
        mov rax, 1
        jmp .end
    
        .error:
            mov rax, errno
            mov dword [rax], 2
            mov rax, EXIT_FAILURE
        .end:
            mov rsp, rbp
            leave
            ret


; int killp(pid_t pid, int SIGNAL)
killp:  endbr64
        push rbp
        mov rbp, rsp
        mov rax, 62
        syscall
    
        test rax, rax
        js .bad_end
        mov rax, EXIT_SUCCESS
        jmp .end
    
        .bad_end:
            mov rax, EXIT_FAILURE
    
        .end:
            mov rsp, rbp
            leave
            ret

    
; int killprange(pid_t min, pid_t max, int SIGNAL)
killprange: 
        endbr64
        push rbp
        mov rbp, rsp
        mov rax, rdi ; SIGNAL
        mov rbx, rsi ; max
        mov rcx, rdx ; min

        ; ciclo che killa i processi nel range min - max
        .extermine: 
                cmp rcx, rbx
                je .end

                push rcx
                push rax
                call killp

                inc rcx
                jmp .extermine
        
        .end:   mov rsp, rbp
                leave
                ret


; void shutdown(int, int);
shutdown:   endbr64
            push rbp
            mov rbp, rsp

            mov rax, 48
            mov rdi, 0
            mov rsi, 0
            syscall

            mov rax, EXIT_SUCCESS
            mov rsp, rbp
            leave
            ret


; void execve(const char* filename, const char* const *argv, const char* const *envp)
execve:
    endbr64
    push rbp
    mov rbp, rsp

    mov rdi, [rbp + 32] ; const char* filename
    mov rsi, [rbp + 24] ; const char* const *argv
    mov rdx, [rbp + 16] ; const char* const *envp
    mov rax, 59
    syscall
    
    mov rax, EXIT_SUCCESS
    ret


; time_t time(NULL);
time:   endbr64
        push rbp
        mov rbp, rsp

        mov rdi, 0	; passo il null per ottenere il timestamp attuale
        mov rax, 201
        syscall

        mov rax, EXIT_SUCCESS
        mov rbp, rsp
        leave
        ret


; bool is_prime(int);
is_prime: 
    push rbp
    mov rbp, rsp

;    if n <= 1:
;        return False
    mov rax, rdi
    cmp rax, 1
    jle .go_out_bad

    mov rdi, rax    ; mi metto il valore da parte
    
;    if n <= 3:
;        return True
    mov rcx, 3 
    cmp rax, rcx
    jle .go_out_well


    ; if n % 2 == 0 or n % 3 == 0:
    ;     return False
    mov rcx, 2
    xor rdx, rdx
    div rcx
    cmp rdx, 0
    je .go_out_bad

    mov rax, rdi      ; ripristino n in rax
    mov rcx, 3
    xor rdx, rdx
    div rcx
    cmp rdx, 0
    je .go_out_bad

    ; i = 5
    mov rcx, 5

    ; while i * i <= n:   
    .while_loop:push rcx
                imul rcx, rcx   ; i * i
                cmp rcx, rdi    ; i <= n
                jg .go_out_well 
                
                ; if n % i == 0:
                ;   return False
                mov rax, rdi
                xor rdx, rdx 
                div rcx
                cmp rdx, 0
                je .go_out_bad

                ; if n % (i + 2) == 0:
                ;   return False
                mov rax, rdi
                add rcx, 2      ; i + 2
                xor rdx, rdx 
                div rcx         ; n % i
                cmp rdx, 0
                je .go_out_bad

                ; i += 6
                add rcx, 4  ; 2 aggiunti prima
                jmp .while_loop

    .go_out_well: ; il numero e' primo
        mov rax, EXIT_SUCCESS
        jmp .end
    .go_out_bad: ; il numero non e' primo
        mov rax, EXIT_FAILURE
    .end:
        mov rsp, rbp
        pop rbp
        leave
        ret

