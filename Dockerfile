FROM python:3.10-slim

WORKDIR /app

# install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app
COPY . .

EXPOSE 5001

CMD ["python", "app.py"]
