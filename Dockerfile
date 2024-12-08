FROM jenkins/jenkins:lts

USER root
RUN apt update && apt install -y python3 python3-pip python3-venv firefox-esr wget
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz \
    && tar -xzf geckodriver-v0.35.0-linux64.tar.gz \
    && chmod +x geckodriver \
    && mv geckodriver /usr/local/bin/ \
    && rm geckodriver-v0.35.0-linux64.tar.gz
USER jenkins
EXPOSE 8080
EXPOSE 50000