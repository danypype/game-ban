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

### Authentication

All requests sent to the API must provide an `api_key` parameter. When this parameter is not provided or is invalid, the server will reply with `401 Unauthorized`

Example **valid** request
```
GET http://host:port/games?api_key=ab3f10
```

### Routes

#### POST /games
Crates a game
```commandline
$ curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"name": "Halo Guardians"}' \
    http://host:port/games?api_key\=<api_key>
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
$ curl http://host:port/games\?api_key\=<api_key>
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
    http://host:port/blacklist\?api_key\=<api_key>
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
$ curl curl -X GET http://host:port/blacklist/check\?email\=john.doe@example.com\&api_key\=<api_key>
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
To successfully deploy this application on AWS, follow these guidelines

### Set up AWS account
1. Create an AWS account. See [here](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/) for details on how
2. As the AWS root user, [Create an IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html), let's call it `deployments-agent`
3. Grant full access*(1)* for the following services to the `deployments-agent` user
   - ECR (to push Docker images)
   - ECS (to deploy services as containers)
   - RDS (to deploy the database)
4. Create an CLI [Access Key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html?icmpid=docs_iam_console#Using_CreateAccessKey) for the `deployments-agent` user, and store it safely

### Install the AWS CLI
Install the AWS CLI to perform operations on AWS. For most operations you can use the AWS console, but for some services like ECR, the CLI is needed. Follow the instructions given your OS: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html

### Crate a VPC
[create a VPC](https://docs.aws.amazon.com/directoryservice/latest/admin-guide/gsg_create_vpc.html) let's call it `production`

When creating the VPC, select
- VPC only
- IPv4 CIDR manual input
    + Type in `10.0.0.0/24`*(2)*
- No IPv6 CIDR block
- Default Tenacy

### Create and RDS instance
[create an AWS RDS instance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Tutorials.WebServerDB.CreateDBInstance.html) with the following specs:
- Engine type: MySQL
- Engine version: 8.0.28
- Availability and durability: Single DB instance
- Choose a good instance identifier like `gameban-prod` or `gameban-production`  
- Choose a secure set of credentials for the Master user. To generate a safe password, feel free to run `$ ./scripts/keygen.sh` in this directory
- Storage type: General Purpose SSD
- Allocated storage: as needed, we can start with 128GB and scale later
- Public access: No*(3)*
- DB instance class: db.m6i.xlarge (*)
- VPC: Choose `production`, the VPC from the previous step

### Crate a .env.aws file
We use .env for development and .env.test for testing. In order to deploy to AWS, let's create a .env.aws file in this directory
```commandline
$ cp .env.test .env.aws
```
You should change all pertient env vars
- `SQLALCHEMY_DATABASE_URI` Should be updated using the user, password, hostname, port, and database name of the previously created RDS instance
    + The format is `mysql://user:password@hostname:port/database_name`
- `SQLALCHEMY_ECHO` Set as you prefer. I recommend setting it to `0` or `"False"` in order to avoid logging all queries on production
- `API_KEY` Set to a secure and secret value. Feel free to run `$ ./scripts/keygen.sh` to ge a new secure value

### Build the deployment Docker image
From this directory execute
```commandline
$ docker build . -t gameban:latest
```
The command from above will build a Docker image with all app dependencies + Gunicorn installed. This image will later be pushed to [AWS ECR](https://aws.amazon.com/ecr/)

### Push Docker image to ECR
1. Create a private(4) ECR repository, let's call it `gameban-ecr`
2. Using the AWS CLI and the Access Key for the `deployments-agent` user, push the Docker image to ECR. See instructions at: https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html

### Set up ECS for the API

1. Create an [ECS Task Definition](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/create-task-definition.html) with the following settings
   - 

### Security Notes

- (1) Granting an IAM user full access to AWS services is not ideal, but is a good enough starting point. Ideally, the [Principle of least privilege](https://en.wikipedia.org//wiki/Principle_of_least_privilege) should be followed
- (2) A CIDR block of class `/24` establishes a range of 256 (`10.0.0.0` to `10.0.0.255`) available IP addresses (enough for the purposes of this VPC)
- (3) We don't want the instance to be publicly accessible (i.e, obtain its own public IP address), unless this is a development instance. Production instances should *always* be not publicly accessible
- (4) ECR repositories containing production images should be made private so only people in our AWS account and with the right permissions can pull them

### Performance Notes

- * A single *db.m6i.xlarge* RDS instance provides 4 vCPUs; 16GB RAM; 10,000Mbps. Enough to sustain 100 concurrent requests, and provide an average response time of less than one second
    + Keep in mind this is a rough initial estimate for performance
    + A proper benchmarking of the API should be done once deployed in order to see if we can reduce the DB instance size to reduce costs
    + To help with database performance, careful indexing of the tables was done
    + Database indexes should be tuned as requirements change and the API increases in functionality
- **