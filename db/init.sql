use local_database;

CREATE TABLE recipes_popularity (
  id int NOT NULL AUTO_INCREMENT, 
  recipe_key VARCHAR(120),
  total_hit TINYINT,
  PRIMARY KEY (id)
);