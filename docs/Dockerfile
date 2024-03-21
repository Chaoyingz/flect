FROM python:3.11-alpine

WORKDIR /app

ENV PYTHONPATH=src

# Install dependencies
COPY ./requirements.lock .
RUN sed '/-e/d' requirements.lock > requirements.txt
RUN pip install -r requirements.txt

# Copy source
COPY . .

CMD uvicorn src.documentation.main:app --host 0.0.0.0 --port 8080
