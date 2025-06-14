FROM python:3.12
WORKDIR /app
COPY requirements.txt .
COPY . .
RUN apt-get update && \
    apt-get install -y git && \
    git submodule update --init --recursive && \
    git submodule foreach 'git checkout main || :'
    # git submodule foreach 'cd $toplevel'
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]