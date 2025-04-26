variable "aws_region" {
  description = "The AWS region where resources will be created."
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "The EC2 instance type."
  type        = string
  default     = "t2.micro" # Free Tier eligible instance type
}

variable "key_name_prefix" {
  description = "Prefix for the AWS Key Pair name."
  type        = string
  default     = "lab6-deployer-key"
}

variable "common_tags" {
  description = "Common tags to apply to all resources."
  type        = map(string)
  default = {
    Project   = "CloudComputingLabs"
    ManagedBy = "Terraform"
  }
}

variable "ssh_location" {
  description = "The source CIDR block allowed for SSH access. Use '0.0.0.0/0' for anywhere (less secure)."
  type        = string
  default     = "0.0.0.0/0"
  # For better security, replace with your specific IP address followed by /32
  # Example: "YOUR_PUBLIC_IP/32". You can find your IP by searching "what is my ip" on Google.
}

variable "private_key_filename" {
  description = "Filename for the generated private key to be saved locally."
  type        = string
  default     = "generated-key.pem" # Will be saved in the same directory as the Terraform files
}

variable "github_token" {
  description = "GitHub Personal Access Token with repo permissions."
  type        = string
  sensitive   = true
}

variable "github_repo" {
  description = "GitHub Repository URL with CI/CD Workflows."
  type        = string
}
