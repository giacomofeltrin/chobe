# docker build -t animeita:latest .
# docker run animeita:latest
FROM python:latest
LABEL maintainer="feltrin.gi@gmail.com"

WORKDIR /usr/src/app

COPY animeita.py ./
COPY resources ./
#COPY requirements.txt
#RUN pip install -r requirements.txt
RUN pip install requests
RUN pip install beautifulsoup4

CMD [ "python", "./animeita.py" ]