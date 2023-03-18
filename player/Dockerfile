FROM python:3.9.6

COPY . /player
WORKDIR /player

# Run requirements.txt
RUN pip3 install -r requirements.txt

# Expose port mentioned in arguments to docker run
EXPOSE 9000 9001

CMD ["python3", "main.py", "--player", "env"]

