FROM thejmthon/jmrzd:slim-buster

RUN git clone https://github.com/thejmthon/jmrzd.git /root/jmisgood

WORKDIR /root/jmisgood

RUN pip3 install --no-cache-dir -r requirements.txt

ENV PATH="/home/jmisgood/bin:$PATH"

CMD ["python3","-m","jmisgood"]
