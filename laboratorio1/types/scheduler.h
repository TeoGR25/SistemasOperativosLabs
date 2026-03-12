#ifndef SCHEDULER_H
#define SCHEDULER_H

#include "process.h"

#define Q0_QUANTUM 2
#define Q1_QUANTUM 4
#define Q2_QUANTUM 8

#define BOOST_INTERVAL 20

typedef struct {

    Process *processes;
    int total_processes;

    int time;

} Scheduler;

Scheduler* create_scheduler(Process *processes, int n);

void run_simulation(Scheduler *scheduler);

void free_scheduler(Scheduler *scheduler);

#endif