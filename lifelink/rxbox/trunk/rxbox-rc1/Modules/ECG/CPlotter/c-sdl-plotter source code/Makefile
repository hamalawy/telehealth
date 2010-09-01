CC=g++
CFLAGS=-c -Wall -I /usr/include/SDL/ -lSDL -lSDL_gfx -lSDL_image
LDFLAGS=-I /usr/include/SDL/ -lSDL -lSDL_gfx -lSDL_image
SOURCES=plotter.c BPfilter.c mdfir1.c mwindow.c
OBJECTS=$(SOURCES:.c=.o)
EXECUTABLE=plotter

all: $(SOURCES) $(EXECUTABLE)
	
$(EXECUTABLE): $(OBJECTS) 
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

.c.o:
	$(CC) $(CFLAGS) $< -o $@
