FROM python:3.7

# set the working directory in the container
WORKDIR /app

COPY requirements.txt .
# install dependencies
RUN pip install -r requirements.txt

# copy src
COPY bot_cmd.py .

CMD ["python", "bot_cmd.py"]

