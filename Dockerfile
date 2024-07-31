FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh


EXPOSE 8000
ENV DJANGO_SETTINGS_MODULE=myproject.settings
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
