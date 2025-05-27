
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
;	Programmino che emula il comportamento delle classi di alto livello
;	Implementare la classe persona che rispetta le seguenti caratteristiche:
;	@nome: *char
;	@cognome: *char
;	@eta: int
;	@inc_eta: metodo che incrementa l'attributo @eta
;	
;	__author__: naga272
;	__data__: 21_04_2025
;
;	next step: rendere il campo nome e cognome dinamici
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;



%macro	GXOR 0
	xor rax, rax
	xor rbx, rbx
	xor rcx, rcx
	xor rdx, rdx
%endmacro


%define EXIT_SUCCESS 0x00
%define EXIT_FAILURE 0x01 
%define end_line 0xa, 0x00


section .data


msg_alloc_error db "Errore durante l'allocazione dinamica della memoria", 0


; nb: per verificarne in gdb il contenuto bisogna conoscerne precisamente la posizione nella struct (usando i bytes) 
persona:
	.nome: 		db "Mario", end_line ; 0-5 bytes
	.cognome: 	db "Rossi", end_line ; 6-12 bytes
	.eta:		dd 0x00	      ; 13-17 bytes
	.inc_eta:	dq 0x00	      ; 18-26 bytes
end_struct_persona:


section .text
	global _start


%define size_struct_persona 	end_struct_persona - persona 		; size struct persona
%define off_nome 		end_struct_persona - persona.nome	; offset del nome 		
%define off_cognome 		end_struct_persona - persona.cognome 	; offset cognome
%define off_eta 		end_struct_persona - persona.eta	; offset eta
%define off_inc_eta 		end_struct_persona - persona.inc_eta	; offset ptr a funzione



; void inc_eta(struct persona *rdi) // funzione che incrementa l'eta dell'oggetto di 1
inc_eta:endbr64
	push rbp
	mov rbp, rsp
	
	inc dword [rdi + off_eta]	
	
	leave
	ret


Persona:endbr64
	push rbp
	mov rbp, rsp
	
	mov rdi, size_struct_persona
	call malloc	

	; ora mi devo occupare di copiare byte x byte dalla sytruct in .data in quella dell'heap
	push rax ; salvo l'offset della struct persona che sta nell'heap
	
	mov rsi, persona
	mov rdx, 0
	.loop: 	cmp rdx, size_struct_persona
		je .done
		
		mov cl, byte [rsi + rdx]
		mov byte[rax + rdx], cl	

		inc rdx
		jmp .loop
	.done:
	pop rax
 	
	; assegno al ptr a funzione inc_eta e ritorno all'address inziale dell'oggetto
	mov qword[rax + off_inc_eta], inc_eta

	leave
	ret


; void* malloc(size_t n);
malloc:	endbr64
	push rbp
	mov rbp, rsp

	mov rsi, rdi	; length
	xor rdi, rdi	; l'address me lo lascio dare dal kernel
	mov rdx, 0x03	; flag protection: PROT_READ | PROT_WRITE
	mov rcx, 0x22	; flags: MAP_PRIVATE | MAP_ANONYMOUS
	mov r8, -1	; fd = -1
	mov r9, 0	; offset = 0
	call mmap

	test rax, rax
	js .error
	leave
	ret

	.error:	mov rdi, msg_alloc_error
		call print
		mov rdi, EXIT_FAILURE
		call _exit	


; void* mmap(void* rdi, size_t rsi, int rdx, int r10, int r8, off_t r9);
mmap: 	endbr64
	push rbp
	mov rbp, rsp
	
	mov rax, 9	
	mov r10, rcx
	syscall	

	leave
	ret


; void free(void* rdi);
free: 	endbr64
	push rbp
	mov rbp, rsp

	mov rax, 12
	syscall

	leave
	ret


main:	endbr64
	push rbp
	mov rbp, rsp

	call Persona

	; stampa a schermo il nome
	mov rdi, rax
	call print
	
	mov rdi, rax
	call [rdi + off_inc_eta]

	mov rdi, rax
	call free

	mov rax, EXIT_SUCCESS
	leave
	ret


; unsigned int print(unsigned char* rdi);
print: 	endbr64
	push rbp
	mov rbp, rsp
	push rax	
	push rdi 	; per sicurezza salvo il registro nello stack	
	call strlen

	mov rdx, rax
	mov rsi, rdi
	mov rax, 1
	mov rdi, 1
	syscall

	pop rdi
	pop rax
	leave	
	ret


strlen: endbr64
        push rbp
        mov rbp, rsp

        mov rax, -1
	.ciclo: inc rax
		cmp byte[rdi + rax], 0
		jnz .ciclo
	
	leave
	ret


_start:	endbr64
	GXOR
	call main

_exit:  endbr64
	mov rdi, rax
	mov rax, 60
	syscall

