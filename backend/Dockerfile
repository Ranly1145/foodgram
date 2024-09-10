FROM python:3.9

WORKDIR /app
RUN python -m pip install --upgrade pip && pip3 install gunicorn==20.1.0 --no-cache-dir

COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /app


CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]