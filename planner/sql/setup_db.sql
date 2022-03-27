DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS tasks CASCADE;
DROP TABLE IF EXISTS shoppinglist CASCADE;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
  );
  
CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  oid INTEGER,
  decription TEXT,
  deadline DATE,
  shopping TEXT NOT NULL,
  FOREIGN KEY (oid) references users(id) ON DELETE CASCADE
  );
  
CREATE TABLE shoppinglist (
  item TEXT NOT NULL,
  qty TEXT NOT NULL,
  tid INTEGER,
  FOREIGN KEY (Tid) references tasks(id) ON DELETE CASCADE
  );
