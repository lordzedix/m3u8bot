FROM debian:latest

RUN apt update && apt upgrade
RUN apt install ffmpeg -y
CMD ["python3", "bot.py"]
