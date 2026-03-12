#include <stdio.h>
#include <stdlib.h>

#include "../types/utils.h"

int calculate_response_time(Process *p) {
    return p->first_response_time - p->arrival_time;
}

int calculate_turnaround_time(Process *p) {
    return p->finish_time - p->arrival_time;
}

int calculate_waiting_time(Process *p) {
    return calculate_turnaround_time(p) - p->burst_time;
}

void export_results(Process *processes, int n, const char *filename) {

    FILE *file = fopen(filename, "w");

    if (file == NULL) {
        printf("Error creando archivo CSV\n");
        return;
    }

    fprintf(file,"PID,Arrival,Burst,Start,Finish,Response,Turnaround,Waiting\n");

    for (int i = 0; i < n; i++) {

        Process *p = &processes[i];

        fprintf(file,"%d,%d,%d,%d,%d,%d,%d,%d\n",
                p->pid,
                p->arrival_time,
                p->burst_time,
                p->start_time,
                p->finish_time,
                calculate_response_time(p),
                calculate_turnaround_time(p),
                calculate_waiting_time(p));
    }

    fclose(file);
}