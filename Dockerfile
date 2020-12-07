FROM python:3.7

# set the working directory in the container
WORKDIR /app

COPY requirements.txt .
# install dependencies
RUN pip install -r requirements.txt

# copy src
COPY *.py discord_bot/
#COPY bot_cmd.py .

ENV PYTHONPATH /app/discord_bot
CMD ["python", "discord_bot/bot_cmd.py"]

