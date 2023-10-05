#!/bin/bash

aws ecr get-login-password --region us-east-1 --profile tracking | docker login --username AWS --password-stdin 131643625257.dkr.ecr.us-east-1.amazonaws.com
docker build -t tracking-app .
docker tag tracking-app:latest 131643625257.dkr.ecr.us-east-1.amazonaws.com/tracking-ecr:latest
docker push 131643625257.dkr.ecr.us-east-1.amazonaws.com/tracking-ecr:latest