# flask-rest-api

### Installing the code 

The code uses venv to run and uses docker and docker compose to setup and requires <br/>

-- python version 3.7 or above <br/>
-- docker engine installed <br/>
-- install make command on linux/ mac  systems <br/>
-- github command line tools <br/>

### clone the repository and checkout the code <br/>

1. clone the repository using the below command <br/>

```
git clone https://github.com/prashunjavero/flask-rest-api.git
```

2. checkout from master 

```
git checkout -b master 
```

3. install the venv with the help of make command 

```
make env
```

this will create a vitual env for you and then enters the shell for you 

4. install all the dependencies that are required by the code 
```
make install
```

this should generate a piplock file for you 

5. auto generate the requirements.txt from the piplock file using 

```
make lock
```
this should auto genearate a requirements.txt file from the piplock file 

6. build the code using 

```
make build
```

this will run docker compose and build the <br>

-- application container <br>
-- redis container<br>
-- mongodb container <br>

for you . please not that the redis and mongodb databases are not installed in cluster mode <br>
so the size of the data that you can work with is limited by the size of the attached docker volume <br>

7. run the code 

```
make deploy
```

single command to start the app server and the redis and mongodb database 


### API Endpoints 

1. the API endpoints are sercured using JWT based authentication <br>
2. in order to insert data into database iti is ne essary that the user logs in and gets the access token <br>
3. once the token is generated it is set in the headder as the authorization token <br>
4. please note that you will not be able to get the API to work without the authentication token <br>
5. currently there is only one user seeded into the database but more users can be added using the create user endpoint <br>
6. the roles are used to handle the enpoint authorization and are seeded on server start <br>

#### 1. login user 

###### enpoint : http://0.0.0.0:8000/login  <br>
###### method: POST   <br>
###### body:

```json
{
    "name": "admin_user",
    "password": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9",
    "email": "dummy@outlook.com",
    "roles":["admin"]
}

```

eg response <br>

```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX25hbWUiOiJhZG1pbl91c2VyIiwiZXhwIjoxNjE3NDEzMzk2LCJzY29wZSI6WyJhZG1pbiJdfQ.KFKqwzjniIiNGArW4-2qlv1s0AMWID7TkJTPZJSP8kU",
    "message": "Login Successful",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX25hbWUiOiJhZG1pbl91c2VyIiwiZXhwIjoxNjE3NDEzMzk2LCJzY29wZSI6WyJhZG1pbiJdfQ.T3XvdwmcJBAdXgaJ8PdrWlCci84KuODYkZiAeoX0Lik",
    "token_type": "Bearer"
}
```

###### if the user does not exist you should get an authorization error 

```json 
{
    "message": "unauthorized user",
    "status": 201
}
```

#### 2. download and process file from endpoint

1. as previously noted please setup the authorization token in the header as a bearer token <br>
2. the codde used mongodb as a database to store the data as it can stored both structures , semistructured and untructured data </br>
in our case the data is mostly structured but may be missing fields these are filled with none and mongodb will be able to handle these </br>
without any extra data validation and cleansing required making the peocess of saving data fairly sinple 

###### headers: <br>

```
"Authorization" : "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX25hbWUiOiJhZG1pbl91c2VyIiwiZXhwIjoxNjE3NDEzMzk2LCJzY29wZSI6WyJhZG1pbiJdfQ.KFKqwzjniIiNGArW4-2qlv1s0AMWID7TkJTPZJSP8kU"

"Content-Type" : " application/json"

```
###### endpoint: <br>

http://0.0.0.0:8000/file/download/admin_user

###### method: POST   <br>
###### body:

```
{"endpoint": "https://crashviewer.nhtsa.dot.gov/CrashAPI/FARSData/GetFARSData"}
```

this should go to the posted endpoint and start loading the data into mongodb in a streaming fashion as a webhook <br>
on sucessfull completion of the dataload you should get response 

```json 
{
   "status" : 200 , 
   "message": "records inserted successfully"
}
```

if the upload fails for any reason you should get response 

```json 
{
   "status" : 500 , 
   "message": "error message returned from code "
}
```

if the authentication and or authorizarion  fails for any reason you should get response 
```json 
{
    "message": "unauthorized user",
    "status": 201
}
```




