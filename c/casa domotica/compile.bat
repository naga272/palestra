@ECHO OFF

echo compilazione...
gcc -Wall -W -Wextra main.c domotica/domotica.c domotica/log.c -o ./main.exe -O0
