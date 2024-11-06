FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP="app:create_app()"
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

EXPOSE 5002

CMD ["flask", "run", "--host=0.0.0.0", "--port=5002"]
