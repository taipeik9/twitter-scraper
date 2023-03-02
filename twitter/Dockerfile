FROM python:3.9-alpine

RUN mkdir /app
WORKDIR /app

# Install system dependencies
RUN apk update && apk add --no-cache gcc musl-dev openssl-dev libffi-dev

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .