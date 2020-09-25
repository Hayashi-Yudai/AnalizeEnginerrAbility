CREATE TABLE EventTable (
  event_id BIGSERIAL NOT NULL,
  username VARCHAR(255) NOT NULL,
  event_type VARCHAR(20) NOT NULL,
  repository_name VARCHAR(255) NOT NULL,
  commits INTEGER NOT NULL,
  additions INTEGER NOT NULL,
  deletions INTEGER NOT NULL,
  changed_files INTEGER NOT NULL,
  event_number INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL
);
