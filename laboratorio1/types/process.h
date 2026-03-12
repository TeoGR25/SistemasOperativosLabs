#ifndef PROCESS_H
#define PROCESS_H

typedef struct {

    int pid;

    int arrival_time;
    int burst_time;
    int remaining_time;

    int start_time;
    int finish_time;
    int first_response_time;

    int current_queue;

} Process;

Process create_process(int pid, int arrival, int burst);

Process* create_process_list(int n);

int is_finished(Process *p);

#endif