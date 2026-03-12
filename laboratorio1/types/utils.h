#ifndef UTILS_H
#define UTILS_H

#include "process.h"

int calculate_response_time(Process *p);

int calculate_turnaround_time(Process *p);

int calculate_waiting_time(Process *p);

void export_results(Process *processes, int n, const char *filename);

#endif