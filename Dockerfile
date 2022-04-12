FROM python:3.9
RUN mkdir "app"
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 5000
CMD ["python", "main.py"]