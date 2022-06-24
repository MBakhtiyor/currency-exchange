FROM python:3.10

WORKDIR /my_app/

COPY ./app/requirements.txt /my_app
RUN pip install --no-cache-dir -r /my_app/requirements.txt

#COPY . /app
#ENV PYTHONPATH=/app

COPY . /my_app/
RUN chmod +x start.sh

CMD ["./start.sh"]
