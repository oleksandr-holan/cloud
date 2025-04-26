locals {
  _url_without_protocol_list = split("://", var.github_repo)
  _host_and_path             = element(local._url_without_protocol_list, 1)
  _path_parts                = split("/", local._host_and_path)

  github = {
    host  = element(local._path_parts, 0)
    owner = element(local._path_parts, 1)
    repo  = element(local._path_parts, 2)
  }
}

locals {
  user_data = <<-EOT
#!/bin/bash
set -Eeuo pipefail

sudo dnf update

# Install necessary tools
dnf install -y jq git libicu docker

# Create a dedicated user for the GitHub runner
useradd -m github-runner

# Create a folder
mkdir -p /home/github-runner/actions-runner
cd /home/github-runner/actions-runner

# Download the latest runner package
curl -o actions-runner-linux-x64-2.323.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.323.0/actions-runner-linux-x64-2.323.0.tar.gz

# Optional: Validate the hash
echo "0dbc9bf5a58620fc52cb6cc0448abcca964a8d74b5f39773b7afcad9ab691e19  actions-runner-linux-x64-2.323.0.tar.gz" |  sha256sum -c
# Extract the installer
tar xzf ./actions-runner-linux-x64-2.323.0.tar.gz
# Set ownership
chown -R  github-runner:github-runner /home/github-runner/actions-runner

REG_TOKEN=$(curl -sX POST -H "Authorization: Bearer ${var.github_token}" https://api.${local.github.host}/repos/${local.github.owner}/${local.github.repo}/actions/runners/registration-token | jq .token --raw-output)
sudo -u github-runner ./config.sh \
  --unattended \
  --url "${var.github_repo}" \
  --token "$REG_TOKEN" \
./svc.sh install github-runner
./svc.sh start

# Start the Docker service
systemctl start docker
systemctl enable docker

# Add the ec2-user and github-runner users to the docker group to run Docker commands without using sudo.
sudo usermod -a -G docker ec2-user
sudo usermod -a -G docker github-runner

# Create the directory for Docker CLI plugins
sudo mkdir -p /usr/local/lib/docker/cli-plugins

# Download the latest Docker Compose plugin for your architecture
sudo curl -sL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-$(uname -m) -o /usr/local/lib/docker/cli-plugins/docker-compose

# Set ownership and permissions
sudo chown root:root /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
EOT
}
