# Add output variables
output "eip" {
  value = aws_eip.CLO835_final_project_static_eip.public_ip
}