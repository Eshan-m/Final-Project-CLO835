# final_project_terraform
Terraform code for the final project

Step 1: Open the terminal in dev/instances.
Step 2: Generate an SSH key: ssh-keygen -t rsa -f final_project_dev
Step 3: Type below commands:
- alias tf=terraform
- tf init
- tf fmt
- tf validate
- tf plan
- tf apply --auto-approve
Step 4: Copy the EIP. (At the end of the output).
Step 5: SSH into EC2: ssh -i final_project_dev <EIP>
