#ifndef TICKET_H
#define TICKET_H

#include <stdio.h>

typedef struct {
    long radicado;
    long identificacion;
    char *correo;
    char *tipo_reclamacion;
} Ticket;

Ticket* crear_ticket(void);
void generar_radicado(Ticket *ticket);
int guardar_ticket(const Ticket *ticket);
void liberar_ticket(Ticket *ticket);

#endif