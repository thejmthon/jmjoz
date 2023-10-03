FROM thejmthon/jmbd:slim-buster

RUN git clone https://github.com/thejmthon/jmbd.git /root/jmsource

WORKDIR /root/jmsource

RUN pip3 install --no-cache-dir -r requirements.txt

ENV PATH="/home/jmsource/bin:$PATH"

CMD ["python3","-m","jmsource"]
