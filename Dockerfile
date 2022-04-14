FROM debian:stable-slim
RUN apt update && apt install python3-pip -y
ADD . /root/education_bot
WORKDIR /root/education_bot
RUN pip3 install -r requirements.txt
CMD python3 main.py 

