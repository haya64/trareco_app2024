from dataaccess import DataAccess 

# tableを作成する

da = DataAccess()

query = [
    'CREATE TABLE train_images_colors (id serial NOT NULL, path text NOT NULL, red integer NOT NULL, blue integer NOT NULL, green integer NOT NULL, yellow integer NOT NULL ,purple integer NOT NULL ,orange integer NOT NULL, black integer NOT NULL, gray integer NOT NULL, white integer NOT NULL, PRIMARY KEY(id));',
    'CREATE TABLE train_images_details (id serial NOT NULL, path text NOT NULL, name text NOT NULL, category text NOT NULL, subject text NOT NULL, time timestamp NOT NULL, location_x numeric(8, 6) NOT NULL, location_y numeric(9, 6) NOT NULL, PRIMARY KEY(id));',
    'CREATE TABLE test_images_colors (id serial NOT NULL, path text NOT NULL, red integer NOT NULL, blue integer NOT NULL, green integer NOT NULL, yellow integer NOT NULL, purple integer NOT NULL, orange integer NOT NULL, black integer NOT NULL, gray integer NOT NULL, white integer NOT NULL, PRIMARY KEY(id));',
    'CREATE TABLE test_images_details (id serial NOT NULL, path text NOT NULL, name text NOT NULL, category text NOT NULL, subject text NOT NULL, time timestamp NOT NULL, location_x numeric(8, 6) NOT NULL, location_y numeric(9, 6) NOT NULL, PRIMARY KEY(id));',
    'CREATE TABLE impressions_colors (impression text NOT NULL, red integer NOT NULL, blue integer NOT NULL, green integer NOT NULL, yellow integer NOT NULL, purple integer NOT NULL, orange integer NOT NULL, black integer NOT NULL, gray integer NOT NULL, white integer NOT NULL);',
]


if __name__ == "__main__":
    for q in query:
    	da.create_table(q)