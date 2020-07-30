FROM python:3.8

COPY . /opt/billing
WORKDIR /opt/billing

RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile


ADD ./scripts/init.sql /docker-entrypoint-initdb.d/
RUN chown postgres:postgres /docker-entrypoint-initdb.d/init.sql


RUN mkdir -p logs \
 && chmod a+w logs \
 && chmod +x ./entrypoint.sh

EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]
