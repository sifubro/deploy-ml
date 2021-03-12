#!/usr/bin/env bash
# In regression model requirements we added the kaggle command to be installed
# Here we download the dataset house-prices-advanced-regression-techniques and saving the dataset in to the directory packages/regression_model/regression_model/datasets/
# This was the directory that we manually saved the train.csv and test.csv. However, these are not stored in the version control,
# hence circleci will not be able to find them. That's why we run this script, to place those files into our version the cloud.
# This ensures we have these files available for circleci so that we can run the tests that rely on test data.

# This kaggle command line interface requires a kaggle key. Find it from your kaggle account. Create new API Token.
# then use circleci environmental variables and save them as KAGGLE_USERNAME and KAGGLE_KEY in the setting -> enviromental variables
# in order to run the jobs. These jobs will run everytime we open a pull request, we merge to master etc. W
# We start to automate the process of testing.

kaggle competitions download -c house-prices-advanced-regression-techniques -p packages/regression_model/regression_model/datasets/