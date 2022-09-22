FROM python:3

MAINTAINER Danila Fedorov 'danilafedorof@yandex.ru'


WORKDIR /py


EXPOSE 4000


COPY requirements.txt .

RUN pip install -r requirements.txt


COPY . .

CMD [ "python", "api/app.py" ]