#!/bin/sh
all:simpleSpeexDecode
clean:
	/bin/rm -f ./simpleSpeexDecode
simpleSpeexDecode: simpleSpeexDecode.c
	gcc simpleSpeexDecode.c -L/usr/local/lib -lspeex -I/usr/local/include -o simpleSpeexDecode
install:
	cp ./simpleSpeexDecode /usr/local/bin/
