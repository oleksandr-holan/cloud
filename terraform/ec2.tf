
# Generate an SSH key pair using the TLS provider
resource "tls_private_key" "generated_ssh_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# Create an AWS Key Pair resource using the public key from the generated pair
resource "aws_key_pair" "generated_deployer_key" {
  key_name   = "${var.key_name_prefix}-${var.aws_region}"
  public_key = tls_private_key.generated_ssh_key.public_key_openssh

  tags = var.common_tags
}

# Save the generated private key to a local file
resource "local_file" "save_private_key" {
  content         = tls_private_key.generated_ssh_key.private_key_pem
  filename        = var.private_key_filename
  file_permission = "0600" # Set appropriate permissions for the private key
}

# Find the latest Amazon Linux 2023 AMI for the specified region
data "aws_ami" "amazon_linux_2023" {
  most_recent = true
  owners      = ["amazon"] # AWS account ID for Amazon Linux AMIs

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-kernel-6.*-x86_64"] # Pattern for Amazon Linux 2023
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }
}

# Create a Security Group to allow SSH ingress and all egress
resource "aws_security_group" "allow_rules" {
  name        = "lab6-allow-ssh-http-sg"
  description = "Allow SSH and HTTP inbound traffic and all outbound traffic"

  # Ingress rule for SSH (Port 22)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_location]
    description = "Allow SSH access"
  }

  # Ingress rule for HTTP (Port 80)
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTP access from anywhere"
  }

  # Egress rule to allow all outbound traffic (common default)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1" # -1 signifies all protocols
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = merge(var.common_tags, {
    Name = "lab6-allow-ssh-http-sg" # Update tag to match resource name
  })

  lifecycle {
    create_before_destroy = true
  }
}

# Create the EC2 Instance
resource "aws_instance" "lab_instance" {
  ami           = data.aws_ami.amazon_linux_2023.id
  instance_type = var.instance_type

  # Associate the Key Pair created earlier
  key_name = aws_key_pair.generated_deployer_key.key_name

  # Associate the Security Group created earlier
  # Needs to be a list of security group IDs
  vpc_security_group_ids = [aws_security_group.allow_rules.id]

  # Apply common tags and a specific Name tag
  tags = merge(var.common_tags, {
    Name = "Lab6-EC2-Instance"
  })

  user_data = local.user_data
}
