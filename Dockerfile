FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirement.txt /app
RUN pip install --no-cache-dir -r requirement.txt

COPY . /app

WORKDIR /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

