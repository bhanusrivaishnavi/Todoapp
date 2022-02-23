# 
FROM python:3.9

# 
WORKDIR /TODOAPP

# 
COPY ./requirements.txt /TODOAPP/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /TODOAPP/requirements.txt

# 
COPY ./Server /TODOAPP/Server

# 
CMD ["uvicorn", "Server.main:app", "--host", "0.0.0.0", "--port", "80"]
