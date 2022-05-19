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
- [Here](https://web.postman.co/workspace/e90f4008-b6b4-4c3c-b5ab-12861c561b54) is a postman workspace to see how http requests must be made.
- [Here](https://drawsql.app/platzi-1/diagrams/hi) is the ER diagram of the database.

## Endpoints

### GET
`Professor only`  [/api/professors/submissions/id/](#get-submissions)
`Professor only`  [/api/professors/coursestudents/](#get-submissions)

### POST
`User (Professor and Student) with an active account `[/api/auth/token/](#login)

`Professor only`  [/api/professors/assignment/](#create-assignment) 

`Professor only`  [/api/professors/course/](#create-course) 

`Student only`  [/api/students/submission/](#create-submission) 

`Student only` [/api/students/enroll/](#enroll-student)

### PUT
`Professor only`  [/api/professors/assignment/id/](#update-assignment)

`Professor only`  [/api/professors/submission/id/](#update-submission)

## Endpoints detail

#### POST /api/token/

Through this endpoint a user (professor or student) can log in with his credentials.

**Body**

|          Name | Required |  Type   | Description                                                                                                                                                           |
| -------------:|:--------:|:-------:| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `email` | required | string  | The user account email.                                                                     |
|     `password` | required | string  | The user account password.                                                                     |

If user exists and his credentials are correct

**Response**

```
{
    "access": access_token,
	"refresh": refresh_token
}

```

This access token would be necessary for future requests that require user identification. It should be set in the Authorization header as Bearer token.

