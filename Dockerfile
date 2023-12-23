# Use an official Python runtime as a parent image
FROM python:3.8

WORKDIR /usr/src/django
COPY . /usr/src/django

RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000

# Define environment variable
ENV NAME iotAppFinal

# Run app.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
