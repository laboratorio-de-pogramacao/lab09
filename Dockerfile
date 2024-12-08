FROM jenkins/jenkins:lts

USER root
RUN apt update && apt install -y python3 python3-pip python3-venv
RUN mkdir -p /nix && bash -c "sh <(curl -L https://nixos.org/nix/install) --daemon"
ENV PATH="/root/.nix-profile/bin:${PATH}"
RUN nix-channel --add https://nixos.org/channels/nixpkgs-unstable nixpkgs && nix-channel --update
RUN nix-env -iA nixpkgs.firefox nixpkgs.geckodriver
USER jenkins
EXPOSE 8080
EXPOSE 50000