# Data source for AMI id
data "aws_ami" "latest_amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# Define tags locally
locals {
  default_tags = merge(module.globalvars.default_tags, { "env" = var.env })
  prefix       = module.globalvars.prefix
  name_prefix  = "${local.prefix}_${var.env}"
}

# Retrieve global variables from the Terraform module
module "globalvars" {
  source = "../../modules/globalvars"
}

resource "aws_instance" "CLO835_final_project_ec2_linux" {
  # ami           = data.aws_ami.amazon_linux_2.id
  ami = data.aws_ami.latest_amazon_linux.id
  # instance_type = "t2.micro"
  instance_type = lookup(var.instance_type, var.env)

  /*user_data = <<-EOF
    #!/bin/bash
    set -ex
    sudo yum update -y
    sudo yum install docker -y
    sudo systemctl start docker
    sudo usermod -a -G docker ec2-user
    curl -sLo kind https://kind.sigs.k8s.io/dl/v0.11.0/kind-linux-amd64
    sudo install -o root -g root -m 0755 kind /usr/local/bin/kind
    rm -f ./kind
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    rm -f ./kubectl
    kind create cluster --config kind.yaml​
  EOF*/

  key_name = aws_key_pair.key_pair_final.key_name
  # subnet_id                   = aws_subnet.CLO835_final_project_subnet_01.id
  # security_groups             = [aws_security_group.CLO835_final_project_sg.id]
  # vpc_security_group_ids      = [aws_security_group.CLO835_final_project_sg.id]

  vpc_security_group_ids = [
    module.ec2_sg.security_group_id,
    module.dev_ssh_sg.security_group_id
  ]

  associate_public_ip_address = false
  iam_instance_profile        = "LabInstanceProfile"

  lifecycle {
    create_before_destroy = true
  }

  root_block_device {
    volume_size = 16
  }

  # tags = {
  #   Name = "EC2 Instance for CLO835_final_project"
  # }

  tags = merge(local.default_tags,
    {
      "Name" = "${local.name_prefix}-Amazon-Linux"
    }
  )

  monitoring              = true
  disable_api_termination = false
  ebs_optimized           = true
}

# Defining the kay pair
resource "aws_key_pair" "key_pair_final" {
  key_name   = "CLO835_final_project"
  public_key = file("${local.name_prefix}.pub")
}

#ECR repositories
resource "aws_ecr_repository" "CLO835_final_project_ecr_APP_repository" {
  name = "clo835_final_project_app"
}

resource "aws_ecr_repository" "CLO835_final_project_ecr_DB_repository" {
  name = "clo835_final_project_db"
}

# Elastic IP
resource "aws_eip" "CLO835_final_project_static_eip" {
  instance = aws_instance.CLO835_final_project_ec2_linux.id
  tags = merge(local.default_tags,
    {
      "Name" = "${local.name_prefix}_eip"
    }
  )
}