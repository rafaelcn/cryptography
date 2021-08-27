CC=g++
FL=-std=c++17 -Wall
FD=-Werror -O0 -g
EX=vigenere.exe

FI=$(shell (find src -name "*.cpp"))

all:
	$(CC) $(FL) $(FI) -o bin/$(EX)

debug:
	$(CC) $(FL) $(FD) $(FI) -o bin/$(EX)

vars:
	@echo $(FI)