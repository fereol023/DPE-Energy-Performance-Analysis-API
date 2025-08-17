FROM python:3.12
WORKDIR /app
COPY requirements.txt .
COPY . .
RUN apt-get update && \
    apt-get install -y git && \
    git submodule update --init --recursive && \
    git submodule foreach 'git checkout main || :'
    # git submodule foreach 'cd $toplevel'
RUN pip install --no-cache-dir -r requirements-docker.txt
EXPOSE 8000
CMD ["python3", "main.py"]