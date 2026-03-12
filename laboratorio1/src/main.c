#include <stdio.h>
#include <stdlib.h>

#include "../types/process.h"
#include "../types/scheduler.h"
#include "../types/utils.h"

int main() {

    int n = 4;

    Process *processes = create_process_list(n);

    processes[0] = create_process(1,0,8);
    processes[1] = create_process(2,1,4);
    processes[2] = create_process(3,2,9);
    processes[3] = create_process(4,3,5);

    Scheduler *scheduler = create_scheduler(processes,n);

    run_simulation(scheduler);

    export_results(processes,n,"assets/results.csv");

    free_scheduler(scheduler);
    free(processes);

    printf("Simulacion completada. Resultados en assets/results.csv\n");

    return 0;
}