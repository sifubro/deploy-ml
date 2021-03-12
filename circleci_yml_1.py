version:2
jobs:  # here we define jobs for circleci to run
    test_regression_model:  # here we define our first (and only) job
        working_directory: ~/project  # here we tell circleci from where it should run the commands
        docker: # we specify which docker image we want to run the command in
            - image: circleci/python:3.7.2   #python 3.7.2 will be available when it comes time to run our commands 
        steps: # we define a series of steps to run as part of this job. They all fall into the command section
            - checkout
            - run:
                name: Running test_regression_model
                command: |
                    virtualenv env  #creating a virtual environment
                    . venv/bin/activate #activating the virtual environment
                    pip install --upgrade pip #upgrade pip
                    pip install -r packages/regression_model/requirements.txt #install requirements for regression model
                    chmod +x ./scripts/fetch_kaggle_dataset.sh #setting the permission so that we are allowed to run the fetch_kaggle_dataset.sh script
                    ./scripts/fetch_kaggle_dataset.sh  #now we are running the script
                    py.test -vv packages/regression_model/test_regression_model # we are doing pytests and running the regression model tests
        

workflows:  # workflows is a way of organizing jobs, depending if jobs depend on each other, or if some of them run on particular branches
    version: 2
    test-all:
        jobs:  #here we only specify one job
            - test_regression_model