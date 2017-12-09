FROM python:alpine

RUN apk add --no-cache \
        build-base \
        postgresql-dev

WORKDIR /usr/src/app

COPY src/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./

CMD [ "python", "logs_analysis.py" ]
