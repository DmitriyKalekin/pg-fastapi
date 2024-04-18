CREATE
DATABASE tracker WITH OWNER postgres ENCODING 'UTF8';


\connect tracker postgres;


CREATE
EXTENSION IF NOT EXISTS "uuid-ossp";

DROP TABLE IF EXISTS accounts;
CREATE TABLE accounts
(
    uid          uuid PRIMARY KEY   DEFAULT uuid_generate_v4(),
    email        VARCHAR(255) NULL UNIQUE,
    name         VARCHAR(255) NULL,
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at   TIMESTAMP NULL,
    deleted_at   TIMESTAMP NULL,
    blocked_till TIMESTAMP NULL
);
--
CREATE INDEX ON accounts (created_at);
CREATE INDEX ON accounts (blocked_till);
CREATE INDEX ON accounts (deleted_at);
--
COMMENT ON TABLE accounts is 'Аккаунты (Подтвержденные)';
COMMENT ON COLUMN accounts.uid is 'uuid';
COMMENT ON COLUMN accounts.email is 'Подтвержденный емейл';
COMMENT ON COLUMN accounts.created_at is 'Создание по UTC';
COMMENT ON COLUMN accounts.updated_at is 'Обновление по UTC';
COMMENT ON COLUMN accounts.deleted_at is 'Удален по UTC';
COMMENT ON COLUMN accounts.blocked_till is 'Снятие блокировки по UTC';


DROP TABLE IF EXISTS lib_status;
CREATE TABLE lib_status
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);






DROP TABLE IF EXISTS projects;
CREATE TABLE projects
(
    id          BIGSERIAL PRIMARY KEY,
    project_key VARCHAR(50)  NOT NULL,
    name        VARCHAR(255) NOT NULL,
    manager_id  uuid NULL,                        -- FOREIGN KEY ... CONTRAINT accounts
    status_id   int          NOT NULL DEFAULT 1, -- FOREIGN KEY ... CONTRAINT
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP(6),

    constraint fk_manager_account
        foreign key (manager_id)
            REFERENCES accounts (uid),
            
    constraint fk_status_project
        foreign key (status_id)
            REFERENCES lib_status (id)
);
--
CREATE INDEX ON projects (created_at);
--
COMMENT ON TABLE projects is 'Проекты';
COMMENT ON COLUMN projects.project_key is 'Ключ проекта';
COMMENT ON COLUMN projects.name is 'Название проекта';
COMMENT ON COLUMN projects.manager_id is 'Привязанный аккаунт';
COMMENT ON COLUMN projects.status_id is 'Статус';
COMMENT ON COLUMN projects.created_at is 'Создание по UTC';



DROP TABLE IF EXISTS tasks;
CREATE TABLE tasks
(
    id          BIGSERIAL PRIMARY KEY,
    project_key VARCHAR(50)  NOT NULL,
    project_id  int          NOT NULL,           -- FOREIGN KEY ... CONTRAINT
    summary     VARCHAR(255) NOT NULL,
    description TEXT NULL,
    assignee_id uuid NULL,                       -- FOREIGN KEY ... CONTRAINT accounts
    status_id   int          NOT NULL DEFAULT 1, -- FOREIGN KEY ... CONTRAINT
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP(6),

    constraint fk_assignee_task
        foreign key (assignee_id)
            REFERENCES accounts (uid),

    constraint fk_status
        foreign key (status_id)
            REFERENCES lib_status (id)


);