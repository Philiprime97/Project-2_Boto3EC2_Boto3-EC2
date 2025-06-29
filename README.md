<<<<<<< HEAD
# AWS EC2 Instance Automation with Boto3

This project is a Python-based automation script designed to launch, monitor, and terminate an Amazon EC2 instance using the AWS SDK for Python (`boto3`). It demonstrates foundational skills in infrastructure automation and DevOps workflows on AWS.

---

## 🚀 What It Does

The script:
- Launches a new EC2 instance in a specified AWS region (e.g., `eu-north-1`)
- Tags the instance with custom metadata
- Waits until the instance reaches the `running` state
- Displays instance details: Public IP, DNS, state, and tags
- (Optional) Terminates the instance automatically

---

## 📁 File Structure

```
aws-ec2-launch/
│
├── launch_ec2.py   # Main Python script
├── README.md       # Project overview and usage guide
└── requirements.txt (optional)
```

---

## 🧰 Technologies Used

- Python 3.x
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- AWS EC2

---

## ✅ Prerequisites

Before running the script:

1. **AWS CLI must be configured**  
   Run:
   ```bash
   aws configure
   ```
   and provide:
   - AWS Access Key ID
   - AWS Secret Access Key
   - Default region name (e.g., `eu-north-1`)
   - Output format (`json`, `table`, or `text`)

2. **Ensure you have the necessary AWS resources**:
   - A valid **Key Pair** name (`KEY_NAME`)
   - A valid **Security Group ID**
   - A valid **Subnet ID**
   - A region-specific **AMI ID** (Amazon Linux 2023 recommended)

3. **Permissions**  
   The IAM user or role must have the following EC2 permissions:
   - `ec2:RunInstances`
   - `ec2:DescribeInstances`
   - `ec2:TerminateInstances`

---

## 🧪 How to Use

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/aws-ec2-launch.git
   cd aws-ec2-launch
   ```

2. **Install required packages:**
   ```bash
   pip install boto3
   ```

3. **Edit the `launch_ec2.py` script** to set:
   - `AMI_ID`
   - `KEY_NAME`
   - `SECURITY_GROUP_ID`
   - `SubnetId` (inside the `run_instances()` call)

4. **Run the script:**
   ```bash
   python3 launch_ec2.py
   ```

5. **SSH into the EC2 instance** using the command printed in the output:
   ```bash
   ssh -i your-ssh-key.pem ec2-user@<PublicDnsName>
   ```

6. **Terminate the instance** to avoid charges:
   - Manually in the AWS Console, or
   - Uncomment and use the `terminate_instance()` function in the script

---

## 🔑 Key Features

- ✅ EC2 Launch with Tags
- ✅ Waits for `running` state
- ✅ Shows connection info
- ✅ Safe termination with wait loop
- 🔄 Modular functions (`launch_instance`, `wait_for_instance`, `display_instance_details`, `terminate_instance`)

