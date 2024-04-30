\connect tracker postgres;

DROP TABLE IF EXISTS projects;
CREATE TABLE projects
(
    id          BIGSERIAL    PRIMARY KEY,
    project_key VARCHAR(50)  NOT NULL,
    name        VARCHAR(255) NOT NULL,
    manager_id  uuid         NULL,                      
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP(6),

    constraint fk_manager_account
        foreign key (manager_id)
            REFERENCES accounts (uid)
);
--
CREATE INDEX ON projects (created_at);
--
COMMENT ON TABLE projects is 'Проекты';
COMMENT ON COLUMN projects.project_key is 'Ключ проекта';
COMMENT ON COLUMN projects.name is 'Название проекта';
COMMENT ON COLUMN projects.manager_id is 'Привязанный аккаунт';
COMMENT ON COLUMN projects.created_at is 'Создание по UTC';
