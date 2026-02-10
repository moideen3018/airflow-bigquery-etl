CREATE TABLE IF NOT EXISTS `{{ project_id }}.{{ dataset }}.github_events` (
  event_id STRING,
  event_type STRING,
  repo_name STRING,
  actor_login STRING,
  created_at TIMESTAMP,
  ingested_at TIMESTAMP
);
