## Deploying Django to ECS with Terraform

### Overview
This section provides a step-by-step guide for deploying Django applications to AWS ECS using Terraform, specifically tailored for FRAME projects.

---

### Deployment Steps

#### Step 1: Install AWS CLI
Ensure the AWS CLI is installed and configured with appropriate credentials.

```bash
aws configure
```

#### Step 2: Dockerize the Application
The Dockerfile for the Django application is already included in the project root. Build the Docker image.

```bash
docker build -t my-django-app .
```

#### Step 3: Push Django Application to ECR
Authenticate with AWS ECR and push the Django image to the repository.

```bash
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account_id>.dkr.ecr.<region>.amazonaws.com

docker tag my-django-app:latest <account_id>.dkr.ecr.<region>.amazonaws.com/my-django-app:latest
docker push <account_id>.dkr.ecr.<region>.amazonaws.com/my-django-app:latest
```

#### Step 4: Push Nginx Image to ECR
The Nginx Dockerfile is located at `./nginx/Dockerfile`. Build and push the image.

```bash
docker build -t my-nginx ./nginx

docker tag my-nginx:latest <account_id>.dkr.ecr.<region>.amazonaws.com/my-nginx:latest
docker push <account_id>.dkr.ecr.<region>.amazonaws.com/my-nginx:latest
```

#### Step 5: Update Variables in `variables.tf`

Open the `variables.tf` file in the `terraform` directory and adjust the necessary variables for your project. Below are some key variables:

- **Region**: Update `region` to your desired AWS region.
- **Django Configurations**: Set `django_secret_key`, `django_allowed_hosts`, and `django_settings_module` as per your application.
- **Subnets and Networking**: Modify subnet CIDRs and availability zones if needed.
- **Docker Image URLs**: Ensure `docker_image_url_django` and `docker_image_url_nginx` match your ECR image URLs.
- **Autoscaling Settings**: Adjust `autoscale_min`, `autoscale_max`, and `autoscale_desired` for ECS services.

#### Step 6: Deploy Using Terraform
Navigate to the `terraform` directory and apply the configurations.

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

#### Step 7: Updating the Production Build
1. Make necessary changes to the Django application or Nginx configurations.
2. Rebuild and push the updated Docker images to ECR.
3. Use the `update-ecs.py` script in the `deploy` folder to update the ECS service with the new images.

```bash
python deploy/update-ecs.py \
  --cluster=production-cluster \
  --service=production-service \
  --image="<AWS_ACCOUNT_ID>.dkr.ecr.<region>.amazonaws.com/django-app:latest"
```

This script fetches the current task definition, creates a new revision with the updated image, and updates the ECS service.

---

### Notes

- Ensure all sensitive data is managed securely via AWS Secrets Manager.
- Monitor ECS tasks using AWS CloudWatch.
- Use the Terraform state backend configured in the `terraform` folder to manage state consistency.

### References

- [Terraform AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS ECS Developer Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

