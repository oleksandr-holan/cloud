# Lab 6: AWS Setup and EC2 Instance Creation with Terraform using IAM Identity Center (SSO)

## Introduction

In this lab, we will register for AWS, configure AWS IAM Identity Center (SSO) for secure access, and use Terraform to provision an EC2 (Elastic Compute Cloud) instance with SSH access configured. Using IAM Identity Center provides short-lived credentials through a user-friendly login portal, enhancing security compared to long-lived access keys.

**Important Notes on AWS Usage:**

* AWS offers a Free Tier for new accounts for one year, which is sufficient for these labs. You will need to provide credit card details for account verification, but you won't be charged unless you exceed the Free Tier limits.
* **Resource Management:** Be mindful of resource usage. **Stop** EC2 instances when you are not actively using them to conserve compute hours. **Terminate** instances and **delete** associated storage volumes (EBS) when they are no longer needed to avoid unexpected costs. AWS will send email notifications if you approach the monthly Free Tier limits.

## 1. AWS Registration and IAM Identity Center (SSO) Setup

1. **Sign Up for AWS:** Go to the AWS Free Tier page (<https://aws.amazon.com/free/>) and click "Create a Free Account". Follow the registration process, providing the required details (email, password, contact information, credit card details for verification). Log in to the AWS Management Console: <https://aws.amazon.com/console/> using your **root user** credentials for the initial setup.
2. **Enable IAM Identity Center (SSO):**
    * In the AWS Management Console, search for and navigate to "IAM Identity Center".
    * If it's not already enabled, click "Enable".
    * You'll be guided through a setup process. For the identity source, the default "Identity Center directory" is usually suitable for these labs unless you have an existing identity provider. Choose this option and proceed.
    * Note the **AWS access portal URL** displayed on the IAM Identity Center dashboard. You will need this later.
3. **Create an SSO User:**
    * In the IAM Identity Center console, navigate to "Users" in the left-hand menu.
    * Click "Add user".
    * Enter user details (e.g., username, email address, name). Click "Next".
    * You can add the user to groups (optional for now). Click "Next".
    * Review and click "Add user". You will need to set an initial password for this user (often via an email sent to the user's address).
4. **Create a Permission Set:** This defines what the SSO user can do within an AWS account.
    * Navigate to "Permission sets" under "Multi-account permissions".
    * Click "Create permission set".
    * Choose "Predefined permission set". For simplicity in this lab, you can select `AdministratorAccess`. **Note:** For real-world scenarios, always follow the principle of least privilege and create custom permission sets with only the necessary permissions (e.g., EC2 Full Access, VPC Full Access).
    * Click "Next". Leave defaults on the next screen unless you have specific requirements (like session duration). Click "Next".
    * Review and click "Create".
5. **Assign User to AWS Account:** Grant the SSO user access to your AWS account using the permission set.
    * Navigate to "AWS accounts" under "Multi-account permissions".
    * Select the checkbox next to your AWS account ID (likely the only one listed under your Organization).
    * Click "Assign users or groups".
    * Select the "Users" tab, check the box next to the SSO user you created, and click "Next".
    * Select the checkbox next to the Permission Set you created (e.g., `AdministratorAccess`), and click "Next".
    * Review the assignment and click "Submit".

## 2. AWS CLI v2 and Terraform Installation

1. **Install/Update AWS CLI v2:** The `aws configure sso` command requires AWS CLI version 2.
    * **Using Scoop (Windows):**

        ```sh
        # Remove old version if necessary
        # scoop uninstall aws
        scoop bucket add main
        scoop install main/aws # Installs v2
        ```

    * **Other Methods:** Follow the official AWS CLI installation guide: <https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html>
    * **Verify Installation:**

        ```sh
        aws --version
        # Ensure it shows aws-cli/2.x.x
        ```

2. **Install Terraform:** If you haven't already, install the Terraform CLI.
    * **Using Scoop (Windows):**

        ```sh
        scoop bucket add main # If not already added
        scoop install main/terraform
        ```

    * **Other Methods:** Follow the official Terraform installation guide: <https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli>
    * **Verify Installation:**

        ```sh
        terraform --version
        ```

## 3. Configure AWS CLI for SSO Access

Instead of using long-lived access keys, you'll configure the AWS CLI to use your IAM Identity Center user. Terraform will automatically leverage this configuration.

1. **Run AWS Configure SSO:** Open your terminal or command prompt. Use a profile name to keep configurations separate (e.g., `lab6-sso`).

    ```sh
    aws configure sso --profile lab6-sso
    ```

2. **Follow the Prompts:**
    * `SSO start URL`: Enter the **AWS access portal URL** you noted during the IAM Identity Center setup.
    * `SSO Region`: Enter the AWS Region where you enabled IAM Identity Center (this might be different from the region where you want to create resources, e.g., `us-east-1`). You can find this on the IAM Identity Center dashboard settings.
    * **Browser Authentication:** Your default web browser should open automatically, prompting you to log in. Click "Allow" to grant the AWS CLI access. Use the **SSO user credentials** (email/username and password) you created in Step 1.3.
    * **Account Selection:** The CLI will list the AWS accounts and roles (Permission Sets) available to you. Select the account and role (e.g., `AdministratorAccess`) you configured earlier.
    * `CLI default client Region`: Enter the AWS Region where you want Terraform to create resources (e.g., `us-east-1`, `eu-west-1`). This *can* be different from the SSO Region.
    * `CLI default output format`: Enter `json` (or leave blank).
    * `CLI profile name`: It should default to the name you provided (`lab6-sso`). Press Enter.
3. **Configuration Result:** This command updates your AWS configuration files (`~/.aws/config` and potentially `~/.aws/credentials`) with the necessary details to obtain temporary credentials via SSO for the `lab6-sso` profile.

## 4. Provisioning the EC2 Instance with Terraform

The Terraform configuration files (`.tf` files) define the infrastructure. These files are provided separately.

1. **Set AWS Profile Environment Variable:** Before running Terraform commands, tell Terraform which AWS profile to use.
    * **Linux/macOS:**

        ```bash
        export AWS_PROFILE="lab6-sso"
        ```

    * **Windows (PowerShell):**

        ```powershell
        $env:AWS_PROFILE="lab6-sso"
        ```

    *(Alternatively, you can add `profile = "lab6-sso"` within the `provider "aws" {}` block in your `main.tf` file).*
2. **Navigate to Terraform Directory:** Change to the directory containing the `.tf` configuration files.

    ```sh
    cd ./terraform
    ```

3. **Initialize Terraform:** Download necessary provider plugins.

    ```sh
    terraform init
    ```

4. **Review the Plan:** (Optional but recommended) Preview the actions.

    ```sh
    terraform plan
    ```

5. **Apply the Configuration:** Create the resources on AWS.

    ```sh
    terraform apply
    ```

    * **SSO Login Prompt:** If your SSO session has expired, Terraform (via the AWS CLI) might automatically open your browser again for you to re-authenticate with your SSO user credentials. Allow the access request.
    * **Terraform Confirmation:** Terraform will show the plan and ask for confirmation. Type `yes` and press Enter. Terraform will output the public IP address of the EC2 instance if configured.

## 5. Connecting to the EC2 Instance via SSH

1. **Identify the Public IP:** Note the public IP address of your EC2 instance from the `terraform apply` output or the AWS EC2 Console.
2. **Locate Your Private Key:** The Terraform configuration should have created an AWS key pair and saved the private key locally (e.g., `my-key.pem`). Ensure correct permissions.
    * **Linux/macOS:** `chmod 400 path/to/your/private-key.pem`
    * **Windows (Powershell):** `icacls path/to/your/private-key.pem /inheritance:r /grant:r "$($env:USERNAME):R"`
3. **Connect using SSH:** Use an SSH client. The default username depends on the AMI (e.g., `ec2-user` for Amazon Linux 2, `ubuntu` for Ubuntu).

    ```sh
    ssh -i path/to/your/private-key.pem <default-user>@<public-ip-address>
    ```

    * Replace placeholders with your key path, default user, and public IP.

    If you are using ssh-agent and have a lot of entries, use this command
    ```sh
    ssh -i path/to/your/private-key.pem -o IdentityAgent=none <default-user>@<public-ip-address>
    ``

## 6. Cleaning Up Resources

**Crucially, destroy the AWS resources when finished.**

1. **Ensure AWS Profile is Set:** Make sure the `AWS_PROFILE` environment variable is still set in your current terminal session:
    * **Linux/macOS:** `export AWS_PROFILE="lab6-sso"`
    * **Windows (PowerShell):** `$env:AWS_PROFILE="lab6-sso"`
2. **Destroy Resources:** Navigate back to the Terraform configuration directory and run:

    ```sh
    terraform destroy
    ```

    * **SSO Login Prompt:** You might be prompted to log in via the browser again if your session expired.
    * **Terraform Confirmation:** Type `yes` and press Enter to confirm deletion.
3. **Verify Deletion:** Check the AWS Management Console (EC2 section) to ensure resources are terminated/deleted.

You have now successfully set up AWS with IAM Identity Center (SSO), configured your local environment, provisioned an EC2 instance using Terraform with SSO authentication, connected to it, and destroyed the resources.
