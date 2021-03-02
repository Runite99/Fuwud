FROM  python:3.8
ENV PYTHONUNBUFFERED 1

COPY ./src/requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

WORKDIR /app

EXPOSE 5000

CMD python pyr_ui.py