# Course Management System

## Installation
Clone the github repository

```sh
git clone https://github.com/Sebastian-na/course-management-system.git folder
cd folder/
```

You should create an isolated python environment and activate it.

```sh
virtualenv myenv/
source myenv/bin/activate
```

Install dependencies, run migrations and launch the server. 

```sh
pip install -r requirements.txt 
python manage.py migrate
python manage.py runserver
```

Now you should create a superuser user to log into the django admin panel

## Considerations
- The app is using sqlite as its database for the sake of simplicity. (With other databases such as postgresql it would have been necessary to locally and manually create a database). 
- The app uses jwt authentication, so with every request the Authorization header must be set to something like: Bearer {token} to uniquely identify the user who makes the http request. (except for the login endpoint).
- For the sake of simplicity the .env file is included in the repository.

## Endpoints

### POST
`User (Professor and Student) with an active account `[/api/token/](#login)

`Professor only`  [/api/create/assignment/](#create-assignment) 

`Professor only`  [/api/create/course/](#create-course) 

`Student only`  [/api/create/submission/](#create-submission) 

`Student only` [/api/student/enroll/](#enroll-student)

### PUT
`Professor only`  [/api/update/assignment/id/](#update-assignment)

`Professor only`	[/api/update/submission/id/](#update submission)
