FROM rapidfort/python-chromedriver

WORKDIR /usr/src/main_app
COPY requirements.txt /usr/src/main_app
RUN pip install -r requirements.txt

COPY . /usr/src/main_app

CMD ["python", "main.py"]
