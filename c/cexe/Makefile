CC = gcc
DIR = ./bin
FILE = main


all: compile run
.PHONY: all


compile:
	$(CC) $(DIR)/$(FILE).c -o $(DIR)/$(FILE)


run:
	$(DIR)/$(FILE)


gdb:
	gdb $(DIR)/$(FILE)
