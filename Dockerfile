FROM thejmthon/sbb_b0:slim-buster

RUN git clone https://github.com/thejmthon/sbb_b0.git /root/sbb_b0

WORKDIR /root/sbb_b0/

RUN pip3 install -r requirements.txt

ENV PATH="/home/sbb_b/bin:$PATH"

CMD ["python3","-m","sbb_b"]
