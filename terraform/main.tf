provider "aws" {
  region = "us-east-1"
}

resource "aws_ecr_repository" "webapp_repo" {
  name = "webapp"
}

resource "aws_ecr_repository" "mysql_repo" {
  name = "mysql"
}

resource "aws_instance" "webapp" {
  ami           = "ami-0ebfd941bbafe70c6"  # Amazon Linux 2 AMI
  instance_type = "t2.micro"
  vpc_security_group_ids = ["sg-0320cce62d06a517f"]  # Correct argument for security groups in a VPC
  key_name      = "a2"                   # Ensure the key exists in your AWS account

  tags = {
    Name = "CLO835-WebApp"
  }
}

# Add inbound rule  to allow all IPv4 traffic from anywhere (Default Security)
resource "aws_security_group_rule" "allow_all_inbound" {
  type            = "ingress"
  from_port       = 0
  to_port         = 0
  protocol        = "-1"  # -1 means all protocols
  cidr_blocks     = ["0.0.0.0/0"]  # All IPv4 addresses
  security_group_id = "sg-0320cce62d06a517f"  # Attach to the default security group
}
