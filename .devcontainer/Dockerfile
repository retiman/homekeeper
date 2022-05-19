# syntax=docker/dockerfile:1.4
ARG VARIANT="1.18-bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/go:0-${VARIANT}

WORKDIR /home/vscode
COPY .bash_aliases .bash_aliases
COPY .bash_local .bash_local
RUN <<EOF
chown vscode.vscode .bash_aliases
echo "source ~/.bash_aliases" >> .bashrc

chown vscode.vscode .bash_local
echo "source ~/.bash_local" >> .bashrc

# See https://golangci-lint.run/usage/install/
# See https://goreleaser.com/install/
curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin v1.46.2
echo 'deb [trusted=yes] https://repo.goreleaser.com/apt/ /' | tee /etc/apt/sources.list.d/goreleaser.list
apt-get -y update
apt-get -y install goreleaser
apt-get -y remove subversion
apt-get -y autoremove
EOF
