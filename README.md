**Social Network**

# Installation

```sh
git clone https://github.com/ye11ow-banana/SocialNetwork.git
```

Install dependencies to your virtual environment
```sh
pip install -r requirements.txt
```

Set environment variables to .env file
```sh
SECRET_KEY=
```

### Run Django
```sh
python3 manage.py migrate
```
```sh
python3 manage.py test apps
```
```sh
python3 manage.py runserver
```

---

### Run automated bot
```sh
cd bot
```
Set config file
```sh
config.yaml
```
Run bot
```sh
python3 main.py
```

---

## Tasks

user signup
```sh
data: {"username": "username", "password": "!@#QWE!@#QWE"}
```
```sh
POST http://127.0.0.1:8000/api/accounts/auth/users/
```

user login
```sh
data: {"username": "username", "password": "!@#QWE!@#QWE"}
```
```sh
POST http://127.0.0.1:8000/api/accounts/auth/jwt/create/
```

post creation
```sh
HEADERS
Authorization: Bearer <ACCESS_TOKEN>
```
```sh
Example data: {"text": "Super text"}
```
```sh
POST http://127.0.0.1:8000/api/posts/create/
```

media creation
```sh
HEADERS
Authorization: Bearer <ACCESS_TOKEN>
Content-Disposition: attachment; filename=filename.jpg
```
```sh
Example data: file
```
```sh
POST http://127.0.0.1:8000/api/posts/<post_id>/media/add/
```

post like
```sh
HEADERS
Authorization: Bearer <ACCESS_TOKEN>
```
```sh
Example data: {"date_created": "2023-04-23"}
```
```sh
POST http://127.0.0.1:8000/api/posts/<post_id>/likes/add/
```

post unlike
```sh
HEADERS
Authorization: Bearer <ACCESS_TOKEN>
```
```sh
DELETE http://127.0.0.1:8000/api/posts/<post_id>/likes/remove/
```

analytics about how many likes was made
```sh
HEADERS
Authorization: Bearer <ACCESS_TOKEN>
```
```sh
GET http://127.0.0.1:8000/api/posts/likes/analytics/?date_from=2011-03-14&date_to=2024-12-12&limit=1&offset=1
```

user activity an endpoint which will show when user was login last time and when he makes a last
request to the service
```sh
HEADERS
Authorization: Bearer <ACCESS_TOKEN>
```
```sh
GET http://127.0.0.1:8000/api/accounts/<user_id>/activity/
```

That's all :)
