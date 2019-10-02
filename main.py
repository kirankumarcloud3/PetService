import ast
from flask import Flask, request, jsonify
from flask_restful import Resource, Api

from db_setup import Pets, app, db

api = Api(app)

class PetDetailsList(Resource):
    def get(self):
    	query_dict = request.args.to_dict(flat=False)
    	query_string = None
    	if 'q' in query_dict:
    		query_string = query_dict.pop('q')
    	data = list()
    	if query_string:
    		pets = Pets.query.filter(Pets.name.like(query_string[0]) | Pets.age.like(query_string[0]) | Pets.sex.like(query_string[0]) | Pets.description.like(query_string[0])).all()
    	elif query_dict:
    		res = dict()
    		[res.update({k:v[0]}) for k,v in query_dict.items()]
    		pets = Pets.query.filter_by(**res).all()
    	else:
    		pets = Pets.query.all()
    	for each_pets in pets:
    		pets_data_dict = each_pets.__dict__
    		pets_data_dict.pop('_sa_instance_state')
    		data.append(pets_data_dict)
    	data_count = len(data)
    	return_data = {"status": True, "count": data_count, "data": data}
    	return return_data

class PetAdd(Resource):
	def post(self):
		try:
			data = request.form
			if data:
				pet = Pets(**data.to_dict())
				db.session.add(pet)
				db.session.commit()
				return_data = {'status': True, 'message': 'Data Created Successfully'}
			else:
				return_data = {'status': False, 'message': 'Data missing'}
		except Exception as error:
			return_data = {'status': False, 'message': 'Data Creation Failed'}
		return return_data

	def put(self, id):
		try:
			pet_obj = Pets.query.get(id)
			data = request.form
			for k,v in data.items():
				if k == 'name':
					pet_obj.name = v
				if k == 'age':
					pet_obj.age = v
				if k == 'sex':
					pet_obj.sex = v
				if k == 'description':
					pet_obj.description = v			
			db.session.commit()
			return_data = {'status': True, 'message': 'Data Updated Successfully'}
		except Exception as error:
			return_data = {'status': False, 'message': 'Data Update Failed'}
			print(error)
		return return_data

	def delete(self, id):
		try:
			pet_obj = Pets.query.get(id)
			db.session.delete(pet_obj)
			db.session.commit()
			return_data = {'status': True, 'message': 'Data deleted Successfully'}
		except Exception as error:
			return_data = {'status': False, 'message': 'Data deletion Failed'}
			print(error)
		return return_data	

class PetAddMulti(Resource):
	def post(self):
		try:
			data = request.data.decode("utf-8")
			if data:
				for i in ast.literal_eval(data):
					print(type(i))
					pet = Pets(**i)
					db.session.add(pet)
					db.session.commit()
				return_data = {'status': True, 'message': 'Data Created Successfully'}
			else:
				return_data = {'status': False, 'message': 'Data missing'}
		except Exception as error:
			return_data = {'status': False, 'message': 'Data Creation Failed'}
			print(error)
		return return_data


class PetUpdateMulti(Resource):
	def put(self):
		try:
			data = request.data.decode("utf-8")
			if data:
				for i in ast.literal_eval(data):
					if i.get('id'):
						pet_obj = Pets.query.get(i.get('id'))
						for k,v in i.items():
							if k == 'name':
								pet_obj.name = v
							if k == 'age':
								pet_obj.age = v
							if k == 'sex':
								pet_obj.sex = v
							if k == 'description':
								pet_obj.description = v			
						db.session.commit()	
				return_data = {'status': True, 'message': 'Data Updated Successfully'}
			else:
				return_data = {'status': False, 'message': 'Data missing'}
		except Exception as error:
			return_data = {'status': False, 'message': 'Data Creation Failed'}
			print(error)
		return return_data	
			
		
routes = ['/add', '/edit/<id>', '/delete/<id>']
api.add_resource(PetDetailsList, '/')
api.add_resource(PetAdd, *routes)
api.add_resource(PetAddMulti, '/addmulti')
api.add_resource(PetUpdateMulti, '/updatemulti')

if __name__ == '__main__':
    app.run(debug=True)