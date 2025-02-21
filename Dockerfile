FROM python:3.9-alpine
ENV ENVIRONMENT=""
ENV DB_HOST=""
ENV DB_PORT=""
ENV DB_USER=""
ENV DB_PWD=""
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]