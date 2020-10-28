# User Transactions API
> API to manage user transactions.

## Documentation
An OpenApi Swagger documentation.
http://localhost:8000/docs/

## Goals

1. Can create users by receiving: name, email and age
2. List all users and also and see the details of a specific user
3. Can save users' transactions.
4. To get some summary reports.

## Usage
You can use the docker container:
```sh
docker build . -t api
docker run -v  $(pwd):/app/ -itp 8000:8000 --name api api
```

Or installing the pipenv library and installing the dependencies.
Make sure you have Python 3.8.
```sh
sudo apt-get update
sudo apt-get install python3.8
```

```sh
pipenv install --dev
python manage.py migrate
python manage.py setup_demo
python manage.py runserver
```
## Tests
To run the tests.
```sh
python manage.py test
coverage run --source='.' manage.py test
coverage report (93% coverage) 
```

## Lint
```sh
pipenv run lint
```

## Examples
The app creates some demo registers.
* Api user: demo / 123

It's necessary a basic authentication.

```sh
curl --user "demo:123" -X GET http://localhost:8000/api/users/ -H "Content-Type: application/json"
curl --user "demo:123" -X GET http://localhost:8000/api/users/1/ -H "Content-Type: application/json"
curl --user "demo:123" -X GET http://localhost:8000/api/users/1/summary-by-account/ -H "Content-Type: application/json"
curl --user "demo:123" -X GET http://localhost:8000/api/users/1/summary-by-category/ -H "Content-Type: application/json"
curl --user "demo:123" -X POST http://localhost:8000/api/users/ -d '{"name": "Jane Doe", "email": "jane@email.com", "age": 23}'  -H "Content-Type: application/json"
curl --user "demo:123" -X POST http://localhost:8000/api/users/1/transactions/ -d '[{"reference": "000055", "account": "C0009", "date": "2020-01-03","amount": "-51.13", "type": "outflow", "category": "groceries", "user": 1}]'  -H "Content-Type: application/json"
```

## Contact
Eduardo Gasser - edugasser@gmail.com

