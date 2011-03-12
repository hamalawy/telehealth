g++ main.c BPfilter.c mdfir1.c mwindow.c -o filter

CC=g++
CFLAGS=-c -Wall
LDFLAGS=
SOURCES=main.c BPfilter.c mdfir1.c mwindow.c
OBJECTS=$(SOURCES:.c=.o)
EXECUTABLE=filter

all: $(SOURCES) $(EXECUTABLE)
	
$(EXECUTABLE): $(OBJECTS) 
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

.c.o:
	$(CC) $(CFLAGS) $< -o $@
