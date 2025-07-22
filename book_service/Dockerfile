FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

COPY db_migrations.sh /usr/local/bin/db_migrations.sh
RUN chmod +x /usr/local/bin/db_migrations.sh

EXPOSE 8080

ENTRYPOINT ["db_migrations.sh"]

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
