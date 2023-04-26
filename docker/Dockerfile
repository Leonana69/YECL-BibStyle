FROM python:3.11-slim-bullseye

RUN pip install Flask python-Levenshtein pybtex

ENV MAIN_PORT=40000

WORKDIR /root
COPY .. ./src
EXPOSE $MAIN_PORT

CMD ["python", "./app.py"]