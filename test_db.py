import ast
import os
import unittest
import json

from db_setup import db, app
from main import api 

TEST_DB = 'test.db'


class BasicTests(unittest.TestCase):

	############################
	#### setup and teardown ####
	############################

	# executed prior to each test
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['DEBUG'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + TEST_DB
		self.app = app.test_client()
		db.drop_all()
		db.create_all()

	def tearDown(self):
		db.drop_all()

	def test_add_pet(self):
		data = {'name': 'cat', 'age': '3', 'sex': 'male', 'description': 'good cat'}
		response = self.app.post('/add', follow_redirects=True, data=data)
		response_data = response.data
		res = json.loads(response_data.decode('utf-8'))
		self.assertEqual(res.get('message'), "Data Created Successfully")

	def test_get_pets_list_with_empty(self):
		response = self.app.get('/', follow_redirects=True)
		response_data = response.data
		res = json.loads(response_data.decode('utf-8'))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(res.get('count'), 0)

	def test_get_pets_list_with_data(self):
		data = {'name': 'cat', 'age': '3', 'sex': 'male', 'description': 'good cat'}
		post_response = self.app.post('/add', follow_redirects=True, data=data)
		response = self.app.get('/', follow_redirects=True)
		response_data = response.data
		res = json.loads(response_data.decode('utf-8'))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(res.get('count'), 1)

	def test_update_pet_data(self):
		data = {'name': 'cat', 'age': '3', 'sex': 'male', 'description': 'good cat'}
		post_response = self.app.post('/add', follow_redirects=True, data=data)
		update_data = {'description': 'bad cat'}
		put_response = self.app.put('/edit/1', follow_redirects=True, data=update_data)
		self.assertEqual(put_response.status_code, 200)
		res = json.loads(put_response.data.decode('utf-8'))
		self.assertEqual(res.get('message'), 'Data Updated Successfully')

	def test_search_globally(self):
		data = {'name': 'cat', 'age': '3', 'sex': 'male', 'description': 'good cat'}
		add_response_1 = self.app.post('/add', follow_redirects=True, data=data)
		data = {'name': 'dog', 'age': '4', 'sex': 'female', 'description': 'good dog'}
		add_response_2 = self.app.post('/add', follow_redirects=True, data=data)
		response = self.app.get('/?q=4', follow_redirects=True)
		response_data = response.data
		res = json.loads(response_data.decode('utf-8'))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(res.get('count'), 1)

	def test_search_with_field(self):
		data = {'name': 'cat', 'age': '3', 'sex': 'male', 'description': 'good cat'}
		add_response_1 = self.app.post('/add', follow_redirects=True, data=data)
		data = {'name': 'dog', 'age': '4', 'sex': 'female', 'description': 'good dog'}
		add_response_2 = self.app.post('/add', follow_redirects=True, data=data)
		response = self.app.get('/?name=dog', follow_redirects=True)
		response_data = response.data
		res = json.loads(response_data.decode('utf-8'))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(res.get('count'), 1)

	def test_delete_record(self):
		data = {'name': 'cat', 'age': '3', 'sex': 'male', 'description': 'good cat'}
		add_response_1 = self.app.post('/add', follow_redirects=True, data=data)
		response = self.app.delete('/delete/1', follow_redirects=True)
		response_data = response.data
		res = json.loads(response_data.decode('utf-8'))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(res.get('message'), 'Data deleted Successfully')

	def test_delete_record_id_not_there(self):
		data = {'name': 'cat', 'age': '3', 'sex': 'male', 'description': 'good cat'}
		add_response_1 = self.app.post('/add', follow_redirects=True, data=data)
		response = self.app.delete('/delete/3', follow_redirects=True)
		response_data = response.data
		res = json.loads(response_data.decode('utf-8'))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(res.get('message'), 'Data deletion Failed')


if __name__ == "__main__":
	unittest.main()