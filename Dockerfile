FROM python:3.8
ADD . /pythonn-d
WORKDIR /pythonn-d
RUN apt update; apt install -y libgl1
RUN apt-get install python3-tk -y
RUN pip install -r requirements.txt
# ENV DISPLAY=host.docker.internal:0.0
CMD ["python", "./main.py"]