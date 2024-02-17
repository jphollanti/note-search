FROM python:3.9-slim

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

ENV NOTES_CONFIG_FILE=/app/.note-search.cfg
ENV NOTES_DIR=/notebooks/

CMD ["python", "server.py"]