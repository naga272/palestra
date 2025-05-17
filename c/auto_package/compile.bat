@echo off
gcc -Wall -Wextra -W -O3 main.c header.c -o main.exe
echo programma compilato con successo
echo questo programma richiede un argomento
echo es: $ main.exe "__directory__"