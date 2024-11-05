FROM python:3.8

WORKDIR /app

COPY . /app/

RUN pip install mage-ai

RUN chmod +x mage.sh

EXPOSE 6789

CMD [ "mage", "start" ]