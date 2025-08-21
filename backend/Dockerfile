FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

# Kod ve konfigürasyonları /srv altına koyacağız
WORKDIR /srv

# Bağımlılıklar
COPY requirements.txt /srv/requirements.txt
RUN pip install --no-cache-dir -U pip wheel \
 && pip install --no-cache-dir -r /srv/requirements.txt

# Backend’in tamamını kopyala (alembic.ini ve alembic/ dahil)
COPY . /srv/

# app.* importları için
ENV PYTHONPATH=/srv

# Uygulama çalışma dizini
WORKDIR /srv/app
EXPOSE 8000

# Önce migration, sonra Uvicorn
RUN printf '#!/usr/bin/env sh\nset -e\n\necho "==> alembic upgrade head"\nfor i in $(seq 1 20); do\n  if alembic -c /srv/alembic.ini upgrade head; then\n    break\n  fi\n  echo "alembic retry $i/20"; sleep 2\ndone\n\nexec uvicorn app.main:app --host 0.0.0.0 --port 8000\n' > /usr/local/bin/entrypoint.sh \
 && chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
