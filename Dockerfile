FROM python: 3.9-slim-buster

WORKDIR /app

COPY requirements.txt 
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

EXPOSE 8089

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8089"]