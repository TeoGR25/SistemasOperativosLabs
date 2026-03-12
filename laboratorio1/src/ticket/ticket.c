#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "../../types/ticket.h"

Ticket* crear_ticket(void) {
    Ticket *ticket = (Ticket*) malloc(sizeof(Ticket));
    if (ticket == NULL) {
        fprintf(stderr, "Error: No se pudo asignar memoria para el ticket.\n");
        return NULL;
    }

    ticket->correo = NULL;
    ticket->tipo_reclamacion = NULL;

    return ticket;
}

void generar_radicado(Ticket *ticket) {
    srand((unsigned int) time(NULL));
    long tiempo = (long) time(NULL);
    int aleatorio = rand() % 1000;

    ticket->radicado = tiempo + aleatorio;
}

int guardar_ticket(const Ticket *ticket) {
    char nombre_archivo[256];

    snprintf(nombre_archivo, sizeof(nombre_archivo),
             "assets/ticket_%ld.txt", ticket->radicado);

    FILE *archivo = fopen(nombre_archivo, "w");

    if (archivo == NULL) {
        fprintf(stderr, "Error: No se pudo crear el archivo.\n");
        return 0;
    }

    fprintf(archivo, "Radicado: %ld\n", ticket->radicado);
    fprintf(archivo, "Identificacion: %ld\n", ticket->identificacion);
    fprintf(archivo, "Correo: %s\n", ticket->correo);
    fprintf(archivo, "Tipo de reclamacion: %s\n", ticket->tipo_reclamacion);

    fclose(archivo);
    return 1;
}

void liberar_ticket(Ticket *ticket) {
    if (ticket == NULL) return;

    free(ticket->correo);
    free(ticket->tipo_reclamacion);
    free(ticket);
}