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



