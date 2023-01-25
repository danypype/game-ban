# game-ban
This is a take-home assignment by Trebu

## Development environment set up guide
Follow these instructions to set up your development environment

### 1. Pre-requisites
Make sure the following software is installed in your OS

- MySQL v8.0.x
- Python v3.9.x
- Pip v21.2.x

### 2. Create your .env files
After cloning this repo, create a .env file
```commandline
$ cp .env.test .env
```
The command from above will create a .env file in this directory. On this file, locate the env var named `SQLALCHEMY_DATABASE_URI` and remove `_test` from the dabase name, leaving it as `gameban`

### 3. Install dependencies
```commandline
$ pip install -r requirements.txt
```

### 4. Set up the dev and test databases
Make sure you can connect to MySQL using the *root* user. Then, connect and create the development and test databases
```sql
mysql> CREATE DATABASE gameban;
Query OK, 1 row affected (0.03 sec)
mysql> CREATE DATABASE gameban_test;
Query OK, 1 row affected (0.02 sec)
```

After creating the database, from the root directory of this repo execute
```commandline
$ ./scripts/initdb.sh
```
This command should create all necessary tables and indices on both databases. After this, the databases are ready to go

### 5. Run the app
After setting up your databases, to run this back-end app execute
```commandline
$ ./scripts/runapp.sh
```
This command will start the Flask app, and it will be listening on port `5000`

## Running tests
To run all tests execute
```commandline
$ ./scripts/runtests.sh
```

## API Docs

### Routes

#### POST /games
Crates a game
```commandline
$ curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"name": "Halo Guardians"}' \
    http://127.0.0.1:5000/games
```
The response includes the Game ID. Example
```json
{
  "id": 1,
  "name": "Halo Guardians"
}
```

#### GET /games
Retrieve all games
```commandline
$ curl http://127.0.0.1:5000/games
```
The response contains a list of all games. Example
```json
[
  {
    "id": 1,
    "name": "Halo Guardians"
  },
  {
    "id": 2,
    "name": "Call of Duty"
  },
  { 
    "id": 3,
    "name": "God of War"
  }
]
```

#### POST /blacklist
Create a blacklist entry for the given game and player
```commandline
$ curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"game_id": 1, "email": "john.doe@example.com", "reason": "offensive_language"}' \
    http://127.0.0.1:5000/blacklist
```
Response example
```json
{
  "email": "john.doe@example.com",
  "game_id": 1,
  "reason": "offensive_language"
}
```

#### GET /blacklist/check
Retrieve information about a given player in the blacklist
```commandline
$ curl curl -X GET http://127.0.0.1:5000/blacklist/check\?email\=john.doe@example.com
```
Response example
```json
{
  "most_common_reason": "cheating",
  "number_of_games_reported": 3,
  "times_reported_last_90_days":3
}
```

## Deployment process
This README section aims to document the deployment process as good as possible. To successfully deploy this application on AWS, follow these guidelines
