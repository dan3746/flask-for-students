FROM python:3

MAINTAINER Danila Fedorov 'danilafedorof@yandex.ru'


WORKDIR /usr/src/app


EXPOSE 4000


COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "app.py" ]