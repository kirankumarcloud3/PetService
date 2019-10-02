**Setup**
create virtual environment

`virtualenv env_name`

Activate virtualenv

`source env_name/bin/activate`

Install requirements

`pip install -r requirements.txt`

for Creating db and table

`python db_setup.py`

run server

`python main.py`

Available URLS:

1) Listing all data
	url: http://127.0.0.1:5000/
	method: get

2) Add Data
	form data sample: {'name': 'lo', 'age': '3', 'sex': 'male', 'description': 'hello'}
	url: http://127.0.0.1:5000/add
	method: post

3) Update Data
	form data sample: {'name': 'cat'}
	url: http://127.0.0.1:5000/edit/<id>
	method: put

4) Delete Data
	url: http://127.0.0.1:5000/delete/<id>
	method: delete

5) Global Search Data:
	url: http://127.0.0.1:5000/?q=<query String>
	method: get

5) Search Data with seprcific:
	url: http://127.0.0.1:5000/?name=<query String>
	method: get

7) Add multiple entry
	raw data: [{'name': 'lo', 'age': '3', 'sex': 'male', 'description': 'hello'}, {'name': 'uu', 'age': '3', 'sex': 'male', 'description': 'hello'}]
	url: http://127.0.0.1:5000/addmulti
	method: post

8) update multiple entry
	raw data: [{'name': 'lo', 'id': 2}, {age': '13', 'id': 5}]
	url: http://127.0.0.1:5000/updatemulti
	method: put


Running Test Cases

`python test_db.py`
