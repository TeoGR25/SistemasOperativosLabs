# Sistema de Registro de Tickets en C

## Estructura del Proyecto

El proyecto está organizado en módulos:

- src/: código fuente
- type/: archivos header
- assets/: almacenamiento resultados
- Makefile: compilación automática

## Compilación

## Ejecución
```
make run
```

## Limpieza
```
make clean
```

## 1. Descripción del Proyecto

Este proyecto implementa un simulador de scheduler con política Multi-Level Feedback Queue (MLFQ) desarrollado en lenguaje C.
El objetivo es modelar el comportamiento de un planificador de procesos similar al utilizado en sistemas operativos, permitiendo analizar métricas de rendimiento como tiempos de espera, respuesta y retorno.

La simulación se ejecuta en tiempo discreto (ciclos de CPU) y utiliza múltiples colas de prioridad con diferentes quantums de ejecución.

El programa genera como salida un archivo CSV con las métricas de cada proceso simulado.

## 2. Características del Scheduler

El algoritmo implementado corresponde a un Multi-Level Feedback Queue (MLFQ) con las siguientes reglas:

Niveles de prioridad
Cola	Prioridad	Quantum
Q0	    Alta	    2 ciclos
Q1	    Media	    4 ciclos
Q2	    Baja	    8 ciclos

### Políticas del scheduler
- Siempre se ejecuta la cola de mayor prioridad no vacía.
- Dentro de cada cola se aplica Round Robin.
- Si un proceso consume todo su quantum, se demueve a la siguiente cola.
- Si un proceso termina antes del quantum, no se demueve.
- Se implementa un priority boost periódico que devuelve los procesos a la cola de mayor prioridad.

## 3. Métricas calculadas

Para cada proceso se calculan las siguientes métricas:

```
Response Time
```

Tiempo desde la llegada del proceso hasta su primera ejecución.

```
Response Time = first_response_time - arrival_time
Turnaround Time
```

Tiempo total desde la llegada del proceso hasta su finalización.

```
Turnaround Time = finish_time - arrival_time
Waiting Time
```

Tiempo total que el proceso pasó esperando en las colas.

```
Waiting Time = Turnaround Time - Burst Time
```
---

# Escenario de Prueba y Análisis del Scheduler MLFQ

## Escenario de Prueba Utilizado

Para evaluar el comportamiento del algoritmo **Multi-Level Feedback Queue (MLFQ)** usamos los procesos:

| Proceso | Arrival Time | Burst Time |
| ------- | ------------ | ---------- |
| P1      | 0            | 8          |
| P2      | 1            | 4          |
| P3      | 2            | 9          |
| P4      | 3            | 5          |

Configuración del scheduler:

- **Q0 (alta prioridad):** quantum = 2 ciclos
- **Q1 (prioridad media):** quantum = 4 ciclos
- **Q2 (prioridad baja):** quantum = 8 ciclos
- **Priority Boost:** cada **20 ciclos**

En este escenario los procesos llegan de manera escalonada, permite observar cómo el scheduler gestiona la **interrupción de procesos en ejecución, la democión entre colas y la distribución del CPU entre múltiples procesos**.

Los procesos inicialmente ingresan a la cola de mayor prioridad (Q0).
Si consumen completamente su quantum sin terminar, son **removidos a una cola de menor prioridad**.

---

# Respuesta a las preguntas
## ¿Qué ocurre si el *priority boost* es muy frecuente?

Todos los procesos regresarán constantemente a la cola de mayor prioridad (Q0) jaciendo que la cola de prioridad baja **pierdn relevancia**, porque los procesos regresan rápidamente a la cola superior.
El comportamiento del scheduler comienza a parecerse a **Round Robin global**.

## ¿Qué ocurre si no existe *priority boost*?

Si **no existe priority boost**, los procesos que son movidos a colas de baja prioridad pueden **permanecer allí indefinidamente**. Los procesos antiguos recibiendo CPU **cada vez con menor frecuencia**.

Un proceso en una cola baja podría **esperar demasiado tiempo antes de volver a ejecutarse**.


## ¿Cómo afecta un quantum pequeño en la cola de mayor prioridad?

Un **quantum pequeño en la cola de mayor prioridad (Q0)** tiene permite:

- Detectar rápidamente procesos cortos**.
- Mejora el **tiempo de respuesta** para procesos interactivos.
- Evita que procesos largos monopolizen la CPU en niveles altos.

**Desventajas**

- Produce **más cambios de contexto**.
- Incrementa la sobrecarga del scheduler.
- Procesos largos serán demovidos rápidamente a colas inferiores.


## ¿Puede haber *starvation*?

Sí, el **starvation es posible en MLFQ**, especialmente en estas condiciones:

- Muchos procesos cortos llegan constantemente al sistema.
- Procesos largos han sido demovidos a colas de baja prioridad.
- No existe o es muy raro el **priority boost**.

Para evitar eso el **priority boost periódico** se utiliza precisamente para evitar este problema porque cuando ocurre el boost todos los procesos regresan a la cola de mayor prioridad y se les da nuevamente la oportunidad de competir por la CPU. Por lo que ningún proceso quede permanentemente relegado a colas de baja prioridad.