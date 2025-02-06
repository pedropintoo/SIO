FROM python:3.12-slim-bookworm

WORKDIR /app
COPY app/ ./

RUN pip install -r dev_requirements.txt
RUN python3 setup.py develop

ENTRYPOINT ["pserve", "development.ini"]
