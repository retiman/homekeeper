ARG VARIANT="1.18-bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/go:0-${VARIANT}

# Add a custom prompt to the image because the default one is a bit too noisy.
WORKDIR /home/vscode
ADD .devcontainer/prompt.sh prompt.sh
RUN cat prompt.sh >> .bashrc && rm prompt.sh
