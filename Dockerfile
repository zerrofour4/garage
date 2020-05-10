FROM python:3.8.2-alpine
RUN apk add gcc python-dev linux-headers

WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python" , "./garage.py" ]
