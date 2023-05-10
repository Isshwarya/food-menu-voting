# food-menu-voting

An application that provides APIs for the employers of a company to vote for their favorite menu from different food chains.

## Assignment details

### About

Company needs internal service for its’ employees which helps them to make a decision
on lunch place.

Each restaurant will be uploading menus using the system every day over API
Employees will vote for menu before leaving for lunch on mobile app for whom backend has to be implemented
There are users which did not update app to the latest version and backend has to support both versions.
Mobile app always sends build version in headers.

### Needed API’s:

o Authentication
o Creating restaurant
o Uploading menu for restaurant (There should be a menu for each day)
o Creating employee
o Getting current day menu
o Voting for restaurant menu (Old version api accepted one menu, New one accepts top three menus with respective points (1 to 3)
o Getting results for current day

### Requirements:

Solution should be built using Python and preferably Django Rest Framework, but any other framework works
App should be containerised
Project and API Documentation
• Tests

### Extra points

HA Cloud Architecture Schema/Diagram (Preferably Azure)
Usage of Linting and Static typing tools

## Solution details

### Entities in the system

#### Authentication

All the safe operations like list and retrieve doesnt need any authentication. For Create, Update and Delete operations, authentication is typically needed. We support both Basic authentication and JWT authentication.

For Basic authentication, use the same username and password which was used to create the user in the User model.

For JWT authentication, tokens can be obtained by running:

curl \  
 -X POST \
 -H "Content-Type: application/json" \
 -d '{"username": <username>, "password": <password>}' \
 http://localhost:8020/api/token/

This will return access and refresh tokens. This can be used to specify the request header - Authorization: Bearer <access_token>

The access token is provided with one hour expiry and the refresh token can be used to get a new access token. These time limits can be changed by updating the configuration in settings.py

#### Permissions

For all operations requiring authentication, the user sending the request will be allowed to perform the operation if the entity was created by the same user or if the user belongs to admin group.

#### User model

This is Django's user model. A user can be an employee that wants to vote, admin user to manage the system as a whole and creates user, restaurant entities, restaurant owner to post menu, etc.,

#### Restaurant model

All the CRUD actions are supported. For each restaurant supported, one entry should be created

#### Employee model

All the CRUD actions are supported.
For each employee in the company, one entry should be created. Only employees can vote. Each emmployee is associated with one user from User model in one-to-one relationship. Every employee maps to one user. But not every user necessarily maps to an employee.

#### Menu model

All the CRUD actions are supported.
For each restaurant, one new menu can be posted everyday. Menu viewset, additionally provides vote action for the user sending request to vote for their favorite menu with the preference score of 1, 2 or 3.

#### Vote model

Only list and retrieve operations are supported
Each vote submitted by the user creates an entry under this model.

### How to deploy the web server

- First, collect the static files in static folder for Nginx to serve and then build the docker image. Set your current directory to the workspace directory and then run the commands

```console
>>>python manage.py collectstatic
>>>docker build -t voting_app -f deployment/Dockerfile .
```

- Second, deploy the containers by running the command

```console
docker-compose -f deployment/docker-compose.yml up -d
```

- At this point, super user account with username=admin has been created for the django application.

- Go to "http://0.0.0.0:8020/admin" in the browser and login as the created superuser (We use username:admin, password:admin. This can be changed in docker-compose.yml file as needed).

- Then create user accounts from the admin interface like how we do in any typical django application.

- Now CRUD for other entities like "restaurant", "employee", "menu", voting and results actions can be performed through REST APIs.

### Example APIs

- Create a new user from Admin interface. Let's say it created an entry with id=2

- Create a new employee with basic authentication

```
  curl --location --request POST 'http://0.0.0.0:8020/api/employee/' \
  --header 'Authorization: Basic dGVzdDM6dGVzdDNAdGVzdDM=' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "employee_id": 123,
  "user": 2
  }'
```

- Get the access token

```
  curl \
   -X POST \
   -H "Content-Type: application/json" \
   -d '{"username": <username>, "password": <password>}' \
   http://localhost:8020/api/token/
```

- Create a new restaurant with JWT authentication

```
  curl --location --request POST 'http://0.0.0.0:8020/api/restaurant/' \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgzNzA1MTQ5LCJpYXQiOjE2ODM3MDE1NDksImp0aSI6ImRlNjQ3YmRlNGQxYjQ3ZTc4Mjk0MGQ5ZmRiZjg4NWYwIiwidXNlcl9pZCI6Mn0.vFVmtXMfkA3R7KBRnxIYIf-qC9RpHi9BXgY8PEY5-pI' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "name": "rest6",
  "email": "rest6@gmail.com",
  "address": "ggg"
  }'
```

- Get all restuarant list

```
  curl --location 'http://0.0.0.0:8020/api/restaurant/' \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgzNzA1MTQ5LCJpYXQiOjE2ODM3MDE1NDksImp0aSI6ImRlNjQ3YmRlNGQxYjQ3ZTc4Mjk0MGQ5ZmRiZjg4NWYwIiwidXNlcl9pZCI6Mn0.vFVmtXMfkA3R7KBRnxIYIf-qC9RpHi9BXgY8PEY5-pI'
```

- Post a new menu as restaurant owner

```
  curl --location 'http://0.0.0.0:8020/api/menu/' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgzNzA1MTQ5LCJpYXQiOjE2ODM3MDE1NDksImp0aSI6ImRlNjQ3YmRlNGQxYjQ3ZTc4Mjk0MGQ5ZmRiZjg4NWYwIiwidXNlcl9pZCI6Mn0.vFVmtXMfkA3R7KBRnxIYIf-qC9RpHi9BXgY8PEY5-pI' \
  --data '{
  "restaurant": 4,
  "menu_details": "some menu items to be conveyed"
  }'
```

- Vote for a menu as an employee

```
  curl --location 'http://0.0.0.0:8020/api/menu/7/vote/' \
  --header 'Accept: application/json; version="2.0"' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Basic dGVzdDExOnRlc3QxMUB0ZXN0MTE=' \
  --data '{
  "preference_score": 3
  }'
```

- Get the top 3 results

```
  curl --location 'http://0.0.0.0:8020/api/results/' \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgzNzA1MTQ5LCJpYXQiOjE2ODM3MDE1NDksImp0aSI6ImRlNjQ3YmRlNGQxYjQ3ZTc4Mjk0MGQ5ZmRiZjg4NWYwIiwidXNlcl9pZCI6Mn0.vFVmtXMfkA3R7KBRnxIYIf-qC9RpHi9BXgY8PEY5-pI'
```

### Assumptions and TODOs

- For authentication, JWT system is used for its token expiry features and its popularity in mobile environments. The token expiry time can be adjusted in settings.py based on product requirements.

- For selecting top 3 menu's, it's not stated how to perform the selection approach. So the assumed approach is: top three menus are selected based on the menus getting highest no.of votes across any preference_score. This leaves us with the case where a menu getting high no.of votes for preference_score:3 could emerge as the top most finalist. Instead, we could do a weighted score and select top 3 menus based on total score (preference score=1 could be given 5 points, preference score=2 could be given 3 points, preference score=3 could be given 2 points) instead of merely going by counts of votes. This can be improved later based on product requirments.

- Add the ability for the user to change his/her menu preference later. Let's say if the user has voted for Restaurant "Rest1"'s menu as the top most preference and later the user wants to change it to "Rest2". Currently, once voted, we don't allow overrides. This can be decided based on product requirements.

- Implement filtering feature for list type requests as an added feature.
