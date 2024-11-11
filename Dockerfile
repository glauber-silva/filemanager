FROM python:3.12.0-slim-bullseye

LABEL "maintainer"="Glauber Silva <glauber.lucio.silva@gmail.com>"
LABEL "service-name"="file-manager"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOME=/home/filemanager

RUN apt-get update && apt-get install -y libpq-dev gcc curl netcat && \
    groupadd filemanager && useradd -m -d /home/filemanager -g filemanager filemanager

WORKDIR ${HOME}

COPY . .
RUN pip install poetry
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes \
    --without=dev 
RUN python -m pip install --no-cache-dir --upgrade -r requirements.txt && \
    chown -R filemanager:filemanager ${HOME}

RUN find /home/filemanager -type d -exec chmod -v 775 {} \;
RUN find /home/filemanager -type f -exec chmod -v 755 {}  \;

RUN chmod +x entrypoint.sh
RUN chmod +x mongo-init/init-mongo.sh

USER filemanager

CMD ["sh", "/home/filemanager/entrypoint.sh"]