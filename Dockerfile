FROM continuumio/miniconda3:4.9.2

# the base image nuclear_data_base_docker is based on continuumio/miniconda3:4.9.2

COPY app.py .
ADD htm_dashboard ./htm_dashboard
COPY requirements.txt .

RUN pip install -r requirements.txt

ENV PORT 8080

EXPOSE 8080

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run
# to handle instance scaling. For more details see
# https://cloud.google.com/run/docs/quickstarts/build-and-deploy/python
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:server