# docker build -f serie.Dockerfile -t serie:latest .
# docker run serie:latest
FROM python:latest
LABEL maintainer="feltrin.gi@gmail.com"

WORKDIR /usr/src/app

COPY /kodi20/chobe/serie.py ./
COPY /kodi20/chobe/resources ./
COPY /kodi20/chobe/values.py ./
#COPY requirements.txt
#RUN pip install -r requirements.txt
RUN pip install requests
RUN pip install beautifulsoup4

CMD [ "python", "./serie.py" ]