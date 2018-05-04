CREATE TABLE IF NOT EXISTS http (
    id BIGINT,
    meth TEXT,
    url TEXT,
    params TEXT,
    time TIMESTAMP,
    PRIMARY KEY (id, time)
);
