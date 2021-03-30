# create enviornment  
.PHONY : env
env:
	pip install virtualenv
	virtualenv venv -p `which python3`
	pipenv shell 

# install dependencies 
.PHONY : install
install :
	pipenv install

#lint code 
.PHONY : lint
lint :
	python -m pylint ./src

#test code 


# lock the requirements
.PHONY : lock
lock :
	pipenv run pip freeze > requirements.txt

#build code 
.PHONY : build
build :
	docker-compose build

# deploy the code 
.PHONY : deploy
deploy:
	docker-compose up

# deactivate enviorment 
.PHONY : run
run:
	make build & make deploy

# deactivate enviorment 
.PHONY : exit
exit:
	deactivate
