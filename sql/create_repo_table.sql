CREATE TABLE RepoTable (
  repository_name VARCHAR(255) NOT NULL,
  username VARCHAR(255) NOT NULL,
  star INTEGER NOT NULL,
  fork INTEGER NOT NULL,
  language VARCHAR(255),
  repo_size BIGSERIAL NOT NULL,
  created_at TIMESTAMP NOT NULL,
  structure_file VARCHAR(255),
  PRIMARY KEY (repository_name)
);
