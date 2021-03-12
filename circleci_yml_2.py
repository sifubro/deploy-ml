version: 2
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

    test_ml_api:
        working_directory: ~/project  #~/project/packages/ml_api
        docker:
            - image: circleci/python:3.7.2 #3.8.1
        steps:
            - checkout
            #- checkout:
            #    path: ~/project
            - run:
                name:  Running tests         #   Run API tests with Python 3.8
                command: |
                        virtualenv env  #creating a virtual environment
                        . venv/bin/activate #activating the virtual environment
                        pip install --upgrade pip #upgrade pip
                        pip install -r packages/ml_api/requirements.txt #install requirements for regression model
                        py.test -vv packages/ml_api/tests # we are doing pytests and running the ml_api tests


    train_and_upload_regression_model:
        working_directory: ~/project  
        docker:
            - image: circleci/python:3.7.2 
        steps:
            - checkout
            - run: 
                name: Setup env
                command: |
                    virtualenv env  #creating a virtual environment
                    . venv/bin/activate
                    pip install -r packages/regression_model/requirements.txt
            - run: 
                name: Publish model
                command: |
                    . venv/bin/activate
                    chmod +x ./scripts/fetch_kaggle_dataset.sh ./scripts/publish_model.sh #we prepare scripts
                    ./scripts/fetch_kaggle_dataset.sh

                    # we set the PYTHONPATH so that we can call the train_pipeline.py script from our regression model package, so we train the model
                    PYTHONPATH=./packages/regression_model python3 packages/regression_model/regression_model/train_pipeline.py
                    # one the model is trained we upload to gemfury with with out publish_model.sh script.
                    # We specify where the setup.py file is ./packages/regression_model/   (see also publish_model.sh)
                    ./scripts/publish_model.sh ./packages/regression_model/
            

workflows:  # workflows is a way of organizing jobs, depending if jobs depend on each other, or if some of them run on particular branches
    version: 2
    test-all:
        jobs:  #here we specify all 3 jobs
            - test_regression_model
            - test_ml_api
            - train_and_upload_regression_model

            # testing the ml_api requires first training and uploading the model. Because otherwise, when we try and
            # install the dependencies for test_ml_api it won't be able to find somethin in gemfury because it will be empty
            # !!!However!!! once we've done it for the first time, we swap it back because we don't want to publish before
            # we run the tests. So this is one off thing.
            - test_ml_api: 
                requires:
                    - train_and_upload_regression_model
