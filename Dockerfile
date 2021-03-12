FROM python:3.6.4
# use python 3.6.4 docker image from dcckerhub. Linux based image and comes with python installed

# Create the user that will run the app
RUN adduser --disabled-password --gecos '' ml-api-user

# specify working directory: From where any subsequent commands will be run
WORKDIR /opt/ml_api

ARG PIP_EXTRA_INDEX_URL==https://WnWTphq4mDyhpyMmjej4@pypi.fury.io/rallousita
ENV FLASK_APP run.py

# Install requirements, including from Gemfury
# With the ADD command we are taking everythig in the local ml_api directory and copping it to the container
ADD ./packages/ml_api /opt/ml_api/
RUN pip install --upgrade pip
RUN pip install -r /opt/ml_api/requirements.txt

# given permisions to run
RUN chmod +x /opt/ml_api/run.sh
RUN chown -R ml-api-user:ml-api-user ./

USER ml-api-user

#expose port 5000 for incoming requests for our docker container
EXPOSE 5000

# specify the commands to be run when our containers starts up
CMD ["bash", "./run.sh"]

