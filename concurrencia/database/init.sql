DROP TABLE IF EXISTS result;
DROP TABLE IF EXISTS input;

CREATE TABLE input (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_input_status CHECK (status IN ('pending', 'in_process', 'processed'))
);

CREATE TABLE result (
    id SERIAL PRIMARY KEY,
    input_id INT NOT NULL REFERENCES input(id),
    worker_identifier VARCHAR(50) NOT NULL,
    result TEXT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_result_input_id UNIQUE (input_id)
);

CREATE INDEX idx_input_status ON input(status);
CREATE INDEX idx_result_worker ON result(worker_identifier);

INSERT INTO input (description, status)
SELECT 
    'Dato de prueba #' || generate_series,
    'pending'
FROM generate_series(1, 30);