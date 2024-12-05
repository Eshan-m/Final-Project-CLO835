# # # # # # # # # # # # # # # # #
# CLO835 final_project          #
# Group 05                      #
# # # # # # # # # # # # # # # # #

#Define the provider
provider "aws" {
  region = "us-east-1"
}


terraform {
  required_version = ">= 0.12.0"
}

# Data source for availability zones in us-east-1
data "aws_availability_zones" "available" {
  state = "available"
}

# Data block to retrieve the default VPC id 
data "aws_vpc" "default" {
  default = true

  # tags = {
  #   Name = "default vpc"
  # }
}
