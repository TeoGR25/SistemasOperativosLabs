#include <stdio.h>
#include <stdlib.h>

#include "../types/process.h"

Process create_process(int pid, int arrival, int burst) {

    Process p;

    p.pid = pid;
    p.arrival_time = arrival;
    p.burst_time = burst;
    p.remaining_time = burst;

    p.start_time = -1;
    p.finish_time = -1;
    p.first_response_time = -1;

    p.current_queue = 0;

    return p;
}

Process* create_process_list(int n) {

    Process *list = (Process*) malloc(sizeof(Process) * n);

    if (list == NULL) {
        printf("Error reservando memoria para procesos\n");
        exit(1);
    }

    return list;
}

int is_finished(Process *p) {
    return p->remaining_time <= 0;
}