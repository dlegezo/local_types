CREATE TABLE types (
	id SERIAL PRIMARY KEY,
	name VARCHAR(128),
	file_path VARCHAR(260),
	typedef TEXT
);
CREATE UNIQUE INDEX type_file ON types(file_path, name);