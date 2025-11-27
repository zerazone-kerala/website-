#!/bin/bash

# ====== CONFIGURE THIS ======
GITLAB_USER="zerazone2025"
PROJECT_PATH="zerazone2025-group/zerazone2025-project"
IMAGE_NAME="app"
TAG="latest"

GITLAB_TOKEN='glpat-GbcqQK0ZWXGqESVrQ3ZSVG86MQp1Oml2eW93Cw.01.1202axdjj'

# Full image path
IMAGE_FULL="registry.gitlab.com/$PROJECT_PATH/$IMAGE_NAME:$TAG"

echo "==== Building Docker Image ===="
docker buildx build --platform linux/amd64,linux/arm64 -t $IMAGE_FULL --push .

echo "==== Logging in to GitLab Registry ===="
echo $GITLAB_TOKEN | docker login registry.gitlab.com -u $GITLAB_USER --password-stdin

echo "==== Pushing Image ===="
docker push $IMAGE_FULL

echo "==== DONE ===="
echo "Image pushed to: $IMAGE_FULL"




# glpat-GbcqQK0ZWXGqESVrQ3ZSVG86MQp1Oml2eW93Cw.01.1202axdjj