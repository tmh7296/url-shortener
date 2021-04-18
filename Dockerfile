FROM python:3.6.5-alpine3.7

WORKDIR /app

COPY . .

RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    apk add --no-cache build-base && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
