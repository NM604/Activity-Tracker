DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS tasks CASCADE;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
  );
  
CREATE TABLE tasks (
  name TEXT NOT NULL,
  oid INTEGER,
  decription TEXT,
  deadline DATE,
  FOREIGN KEY (oid) references users(id) ON DELETE CASCADE
  );
