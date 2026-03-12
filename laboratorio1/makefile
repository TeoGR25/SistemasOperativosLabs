CC = gcc
CFLAGS = -Wall -Wextra -std=c11

SRC = src/main.c src/scheduler.c src/process.c src/utils.c

OBJ = $(SRC:.c=.o)

TARGET = scheduler

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJ)

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f src/*.o $(TARGET)