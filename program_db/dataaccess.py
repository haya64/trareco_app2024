from var import Var
from db import DB 

class DataAccess:

	def get_users(self):
		query = "SELECT * FROM sample"
		data = ()
		db = DB(Var.hostname, Var.port, Var.dbname, Var.username, Var.password)
		return db.execute(query, data)

	def get_user_by_username(self,username):
		query = "SELECT * FROM data_user WHERE username = %s "
		data = (str(username), )
		db = DB(Var.hostname, Var.port, Var.dbname, Var.username, Var.password)
		return db.execute(query, data)

	# images_colors (train, test)
	def save_data_1(self, query, path, red, blue, green, yellow, purple, orange, black, gray, white):
		data = (str(path), int(red), int(blue), int(green), int(yellow), int(purple), int(orange), int(black), int(gray), int(white))
		db = DB(Var.hostname, Var.port, Var.dbname, Var.username, Var.password)
		return db.update(query, data)

	# images_details (train, test)
	def save_data_2(self, query, path, name, category, subject, time, location_x, location_y):
		data = (str(path), str(name), str(category), str(subject), str(time), float(location_x), float(location_y))
		db = DB(Var.hostname, Var.port, Var.dbname, Var.username, Var.password)
		return db.update(query, data)

	# impressions_colors
	def save_data_impression(self, query, impression, red, blue, green, yellow, purple, orange, black, gray, white):
		data = (str(impression), int(red), int(blue), int(green), int(yellow), int(purple), int(orange), int(black), int(gray), int(white))
		db = DB(Var.hostname, Var.port, Var.dbname, Var.username, Var.password)
		return db.update(query, data)

	def create_table(self, query):
		db = DB(Var.hostname, Var.port, Var.dbname, Var.username, Var.password)
		return db.create(query)

