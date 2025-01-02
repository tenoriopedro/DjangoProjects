FROM python:3.11.3-alpine3.18
LABEL mantainer="pstsouza13@gmail.com"

# Instalar o cliente PostgreSQL
RUN apk update && apk add postgresql-client

# This environment variable is used to control whether Python should
# write bytecode (.pyc) files to disk. 1 = No, 0 = yes
ENV PYTHONDONTWRITEBYTECODE 1

# Defines that Python output will be displayed immediately in the console or in 
# other output devices, without being buffered.
# In short, you will see Python outputs in real time.
ENV PYTHONUNBUFFERED 1

# Copy the "djangoapp" and "scripts" folder into the container.
COPY djangoapp /djangoapp
COPY scripts /scripts

# Enter the django folder in the container
WORKDIR /djangoapp

# Port 8000 will be available for connections external to the container
# It is the port I will use for Django.
EXPOSE 8000

# RUN executes commands in a shell inside the container to build the image. 
# The result of executing the command is stored in the file system 
# image as a new layer.
# Grouping commands into a single RUN can reduce the number of layers in the 
# image and make it more efficient.
RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /djangoapp/requirements.txt && \
  adduser --disabled-password --no-create-home duser && \
  mkdir -p /data/web/static && \
  mkdir -p /data/web/media && \
  chown -R duser:duser /venv && \
  chown -R duser:duser /data/web/static && \
  chown -R duser:duser /data/web/media && \
  chmod -R 755 /data/web/static && \
  chmod -R 755 /data/web/media && \
  chmod -R +x /scripts

# Add the scripts and venv/bin folder 
# in the container's $PATH.
ENV PATH="/scripts:/venv/bin:$PATH"

# Change user to duser
USER duser

# Execute the file scripts/commands.sh
CMD ["/scripts/commands.sh"]