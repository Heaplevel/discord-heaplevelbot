FROM python:3.7

# set the working directory in the container
WORKDIR /app

COPY requirements.txt .
# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy src
COPY *.py discord_bot/
WORKDIR discord_bot/
#COPY bot_cmd.py .

ENV PYTHONPATH .
CMD ["python", "-u", "bot_cmd.py"]

