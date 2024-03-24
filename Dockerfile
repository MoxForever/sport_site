FROM python:alpine3.16

# Setup application
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE $APP_PORT

ENTRYPOINT ["sh", "docker-entrypoint.sh"]
