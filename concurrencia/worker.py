import os
import time
import random
import socket
import fcntl
from datetime import datetime, timezone

import psycopg2
from psycopg2 import OperationalError, errors


DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "concurrency_lab")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

WORKER_ID = os.getenv("WORKER_ID", socket.gethostname())

LOG_DIR = os.getenv("LOG_DIR", "/shared_logs")
LOG_FILE = os.path.join(LOG_DIR, "workers.log")
LOCK_FILE = os.path.join(LOG_DIR, "workers.lock")


def current_time():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f UTC")


def write_log(message):
    """
    Escribe en un archivo compartido usando bloqueo explícito de archivo.
    Esto evita que varios contenedores escriban al mismo tiempo en el log.
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    log_line = f"[{current_time()}] [{WORKER_ID}] {message}\n"

    with open(LOCK_FILE, "w") as lock_file:
        fcntl.flock(lock_file, fcntl.LOCK_EX)

        try:
            with open(LOG_FILE, "a", encoding="utf-8") as log_file:
                log_file.write(log_line)
                log_file.flush()
        finally:
            fcntl.flock(lock_file, fcntl.LOCK_UN)

    print(log_line, end="", flush=True)


def get_connection():
    """
    Intenta conectarse a PostgreSQL.
    Si la base de datos todavía no está lista, reintenta varias veces.
    """
    attempts = 10

    for attempt in range(1, attempts + 1):
        try:
            connection = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
            )
            connection.autocommit = False
            return connection
        except OperationalError:
            write_log(f"Database not ready. Retry {attempt}/{attempts}")
            time.sleep(2)

    raise Exception("Could not connect to the database after several attempts.")


def claim_pending_input(connection):
    """
    Toma un registro pendiente de manera segura.

    FOR UPDATE SKIP LOCKED permite que varios workers consulten la tabla al mismo tiempo,
    pero evita que dos workers tomen la misma fila.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE input
                SET status = 'in_process',
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = (
                    SELECT id
                    FROM input
                    WHERE status = 'pending'
                    ORDER BY id
                    LIMIT 1
                    FOR UPDATE SKIP LOCKED
                )
                RETURNING id, description;
                """
            )

            row = cursor.fetchone()
            connection.commit()

            if row is None:
                return None

            input_id, description = row
            return {
                "id": input_id,
                "description": description,
            }

    except Exception as error:
        connection.rollback()
        write_log(f"Error claiming input: {error}")
        raise


def process_input(task):
    """
    Simula el procesamiento de un dato.
    El tiempo aleatorio ayuda a evidenciar la concurrencia entre workers.
    """
    processing_time = random.uniform(0.5, 2.5)

    write_log(
        f"Processing input_id={task['id']} "
        f"description='{task['description']}' "
        f"estimated_time={processing_time:.2f}s"
    )

    time.sleep(processing_time)

    result = f"Processed '{task['description']}' by {WORKER_ID}"

    return result


def save_result(connection, task, result):
    """
    Guarda el resultado en la tabla común result y marca el input como processed.

    El id de result lo genera PostgreSQL automáticamente.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO result (input_id, worker_identifier, result)
                VALUES (%s, %s, %s);
                """,
                (task["id"], WORKER_ID, result),
            )

            cursor.execute(
                """
                UPDATE input
                SET status = 'processed',
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s;
                """,
                (task["id"],),
            )

            connection.commit()

    except errors.UniqueViolation:
        connection.rollback()
        write_log(
            f"Duplicated result detected for input_id={task['id']}. "
            "The database unique constraint prevented inconsistency."
        )

    except Exception as error:
        connection.rollback()
        write_log(f"Error saving result for input_id={task['id']}: {error}")
        raise


def main():
    write_log("Worker started.")

    connection = get_connection()

    try:
        while True:
            task = claim_pending_input(connection)

            if task is None:
                write_log("No pending inputs available. Worker finished.")
                break

            write_log(f"Claimed input_id={task['id']}")

            result = process_input(task)

            save_result(connection, task, result)

            write_log(f"Saved result for input_id={task['id']}")

            time.sleep(random.uniform(0.2, 1.0))

    finally:
        connection.close()
        write_log("Database connection closed.")


if __name__ == "__main__":
    main()