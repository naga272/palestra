@echo on
gcc client.c -o client.exe -lws2_32 -mwindows
gcc server.c -o server.exe -lws2_32
