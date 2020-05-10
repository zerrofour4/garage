FROM python:3.8.2-slim-buster
RUN apt-get install gcc python3-devel
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python" , "./garage.py" ]
