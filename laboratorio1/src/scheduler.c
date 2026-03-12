#include <stdio.h>
#include <stdlib.h>

#include "../types/scheduler.h"

Scheduler* create_scheduler(Process *processes, int n) {

    Scheduler *s = (Scheduler*) malloc(sizeof(Scheduler));

    if (s == NULL) {
        printf("Error reservando memoria para scheduler\n");
        exit(1);
    }

    s->processes = processes;
    s->total_processes = n;
    s->time = 0;

    return s;
}

void run_simulation(Scheduler *scheduler) {

    int finished = 0;

    while (finished < scheduler->total_processes) {

        for (int i = 0; i < scheduler->total_processes; i++) {

            Process *p = &scheduler->processes[i];

            if (p->arrival_time <= scheduler->time && p->remaining_time > 0) {

                if (p->first_response_time == -1) {
                    p->first_response_time = scheduler->time;
                }

                if (p->start_time == -1) {
                    p->start_time = scheduler->time;
                }

                int quantum;

                if (p->current_queue == 0)
                    quantum = Q0_QUANTUM;
                else if (p->current_queue == 1)
                    quantum = Q1_QUANTUM;
                else
                    quantum = Q2_QUANTUM;

                int run_time = quantum;

                if (p->remaining_time < quantum)
                    run_time = p->remaining_time;

                p->remaining_time -= run_time;

                scheduler->time += run_time;

                if (p->remaining_time == 0) {

                    p->finish_time = scheduler->time;
                    finished++;

                } else {

                    if (p->current_queue < 2)
                        p->current_queue++;
                }

                break;
            }
        }

        scheduler->time++;
    }
}

void free_scheduler(Scheduler *scheduler) {
    free(scheduler);
}