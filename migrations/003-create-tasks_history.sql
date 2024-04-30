\connect tracker postgres;

DROP TABLE IF EXISTS tasks_history;
CREATE TABLE tasks_history 
(
    id          BIGSERIAL PRIMARY KEY,
    task_id     BIGINT NOT NULL, -- think about entering data
    project_key VARCHAR(255) NOT NULL -- think about entering data
);
--
COMMENT ON TABLE tasks_history is 'История Задач';
COMMENT ON COLUMN tasks_history.task_id is 'Идентификатор задачи';
COMMENT ON COLUMN tasks_history.project_key is 'Ключ проекта';