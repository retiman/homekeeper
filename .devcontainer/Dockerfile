# syntax=docker/dockerfile:1.4
ARG VARIANT="1.18-bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/go:0-${VARIANT}

USER vscode
WORKDIR /home/vscode
COPY .bash_aliases .bash_aliases
COPY .bash_local .bash_local
RUN <<EOF
echo "source ~/.bash_aliases" >> .bashrc
echo "source ~/.bash_local" >> .bashrc

# See https://golangci-lint.run/usage/install/
# See https://goreleaser.com/install/
curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sudo sh -s -- -b $(go env GOPATH)/bin v1.46.2
echo 'deb [trusted=yes] https://repo.goreleaser.com/apt/ /' | sudo tee /etc/apt/sources.list.d/goreleaser.list
sudo apt-get -y update
sudo apt-get -y install goreleaser
sudo apt-get -y remove subversion
sudo apt-get -y autoremove
EOF
