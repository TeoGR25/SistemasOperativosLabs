#ifndef QUEUE_H
#define QUEUE_H

#include "process.h"

typedef struct Node {
    Process *process;
    struct Node *next;
} Node;

typedef struct Queue {
    Node *front;
    Node *rear;
} Queue;

void enqueue(Queue *q, Process *p);
Process* dequeue(Queue *q);
int is_empty(Queue *q);

#endif