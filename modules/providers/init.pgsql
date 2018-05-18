CREATE TABLE IF NOT EXISTS prefix (
        id BIGINT PRIMARY KEY,
        user_prefix text,
        mod_prefix text
);
CREATE TABLE IF NOT EXISTS locale(
        id BIGINT PRIMARY KEY,
        locale TEXT
);
