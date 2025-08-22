FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /srv

# Bağımlılıklar
COPY requirements.txt /srv/requirements.txt
RUN pip install --no-cache-dir -U pip wheel \
 && pip install --no-cache-dir -r /srv/requirements.txt

# Uygulama + alembic
COPY . /srv/
ENV PYTHONPATH=/srv

# Uygulama çalışma dizini
WORKDIR /srv/app
EXPOSE 8000

# Entrypoint scriptini kopyala
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
