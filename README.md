# InstaPic Server

## Production URL

https://protected-temple-53328.herokuapp.com

## Setup
* Ensure Python is installed globally.
* ```bash
  $ pip install virtualenv
  ```
* ```bash
  $ virtualenv --python=python3 env
  ```
* ```bash
  $ source env/bin/activate
  ```
* ```bash
  $ pip install -r requirements.txt
  ```
* ```bash
  $ python manage.py db init
  ```
* ```bash
  $ python manage.py db migrate --message '<Your commit message>'
  ```
* ```bash
  $ python manage.py db upgrade
  ```
## Running the Server
* ```bash
  $ make run
  ```

## API

### Auth

*Endpoint:* `/auth/login`

*Method:* `POST`

*Arguments:*

* password: String (min 6)
* email: String (min 6)

### Registration

*Endpoint:* `/user/`

*Method:* `POST`

*Arguments:*

* username: String (min 6)
* password: String (min 6)
* email: String (min 6)

### List Users

*Endpoint:* `/user/`

*Method:* `GET`

*Authorization*: `token`

### List User

*Endpoint:* `/user/<username>`

*Method:* `GET`

*Authorization*: `token`

### List Posts

*Endpoint:* `/post/`

*Method:* `GET`

*Authorization*: `token`

*Params:*

* user: `<username>` (optional)
* sort_by: `newest || oldest` (optional)
* page: integer (optional)

### Submit Post

*Endpoint:* `/post/`

*Method:* `POST`

*Authorization*: `token`

*Arguments:*

* caption: String
* image: file [.png, .jpg, .jpeg, .gif] max 2MB
