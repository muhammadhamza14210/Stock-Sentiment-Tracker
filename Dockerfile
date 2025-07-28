FROM python:3.10-slim 

WORKDIR /app 

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

COPY . . 

ENV GOOGLE_APPLICATION_CREDENTIALS='/app/gcp_key.json'

CMD ["python", "main.py"]