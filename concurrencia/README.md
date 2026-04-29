# Laboratorio de Concurrencia con Contenedores

Este proyecto implementa un sistema concurrente usando Docker Compose, PostgreSQL y múltiples contenedores workers en Python.

El objetivo es demostrar conceptos de concurrencia, exclusión mutua, sincronización, condiciones de carrera y consistencia de datos mediante varios contenedores que procesan datos en paralelo y escriben resultados en una base de datos compartida.

## Arquitectura

El sistema está compuesto por:

- 1 contenedor PostgreSQL.
- 1 contenedor inicializador de base de datos.
- 5 contenedores workers.
- 1 volumen compartido para logs.

```text
docker-compose.yml
│
├── db
│   └── PostgreSQL
│
├── db-init
│   └── Ejecuta database/init.sql
│
├── worker-1
├── worker-2
├── worker-3
├── worker-4
└── worker-5
    └── Ejecutan worker.py