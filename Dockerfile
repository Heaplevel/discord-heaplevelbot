FROM python:3.7

# set the working directory in the container
WORKDIR /app

COPY requirements.txt .
# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy src and yaml
COPY *.py *.yaml discord_bot/

WORKDIR discord_bot/
#COPY bot_cmd.py .

ENV PYTHONPATH .
CMD ["python", "-u", "bot_cmd.py"]

