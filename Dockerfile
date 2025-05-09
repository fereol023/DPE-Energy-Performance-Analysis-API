FROM python:3.9-alpine

ENV ENV="LOCAL"
ENV app-name="DPE-API"

ENV API_RUNNING_HOST="your-value"
ENV API_RUNNING_PORT="your-int-value"

ENV POSTGRES_HOST="your-value"
ENV POSTGRES_USER="your-value"
ENV POSTGRES_PWD="your-value"
ENV POSTGRES_PORT="your-int-value"
ENV POSTGRES_DB="your-value"

ENV S3_ACCESS_KEY="your-value"
ENV S3_SECRET_KEY="your-value"
ENV S3_BUCKET_NAME="your-value"
ENV S3_REGION_NAME="your-value"
ENV S3_ENDPOINT_URL="your-value"

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]