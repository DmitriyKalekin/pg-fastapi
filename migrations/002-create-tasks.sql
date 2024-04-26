\connect tracker postgres;

DROP TABLE IF EXISTS tasks;
CREATE TABLE tasks
(
    id          BIGSERIAL PRIMARY KEY,
    summary     VARCHAR(255) NULL,
    description TEXT NULL,
    assignee_id uuid NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP (6),
    updated_at  TIMESTAMP NULL,
    status_id   INT NOT NULL DEFAULT 1,
    task_id     INT NOT NULL,
    project_key VARCHAR(255) NOT NULL,
    project_id  INT NOT NULL,

    CONSTRAINT fk_tasks_projects 
        foreign key (project_id) 
            REFERENCES projects (id),

    constraint fk_assignee_task
        foreign key (assignee_id)
            REFERENCES accounts (uid),

    constraint fk_status
        foreign key (status_id)
            REFERENCES lib_status (id)


);
--
CREATE INDEX ON tasks (created_at);
CREATE INDEX ON tasks (updated_at);
--
COMMENT ON TABLE tasks is 'Задачи';
COMMENT ON COLUMN tasks.summary is 'Короткое описание';
COMMENT ON COLUMN tasks.description is 'Полное описание';
COMMENT ON COLUMN tasks.assignee_id is 'Ответственный';
COMMENT ON COLUMN tasks.created_at is 'Создание по UTC';
COMMENT ON COLUMN tasks.updated_at is 'Обновление по UTC';
COMMENT ON COLUMN tasks.status_id is 'Статус задачи';
COMMENT ON COLUMN tasks.task_id is 'Идентификатор Задачи';
COMMENT ON COLUMN tasks.project_key is 'Ключ проекта';
COMMENT ON COLUMN tasks.project_id is 'Идентификатор Проекта';
