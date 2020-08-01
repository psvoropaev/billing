FROM python:3.8

RUN apt-get update && apt-get -y install netcat
COPY . /opt/billing
WORKDIR /opt/billing

##RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile
RUN pip install -U setuptools pip pipenv \
    && pipenv lock -r --keep-outdated > requirements.txt \
    && pipenv lock -r -d --keep-outdated >> requirements.txt \
    && pip install -r requirements.txt --retries=1

RUN mkdir -p logs \
 && chmod a+w logs \
 && chmod +x ./scripts/entrypoint.sh

EXPOSE 5000 5555
ENTRYPOINT ["./scripts/entrypoint.sh"]
