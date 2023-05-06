FROM python:3.9

WORKDIR /app

COPY requirement.txt 
RUN pip install --no-cache-dir -r requirement.txt

COPY . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


