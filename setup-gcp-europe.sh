#!/usr/bin/env bash
# Setup Google Cloud project for Video & Image Processing (Europe regions only)
# Run: ./setup-gcp-europe.sh

set -e

# Change this if the project ID is taken
PROJECT_ID="${GCP_PROJECT_ID:-video-image-processing-eu}"
REGION="europe-west1"  # Belgium - use europe-west4 (Netherlands) or europe-west9 (Paris) as alternatives

echo "Creating project: $PROJECT_ID"
gcloud projects create "$PROJECT_ID" --name "Video Image Processing" 2>/dev/null || echo "Project may already exist"
gcloud config set project "$PROJECT_ID"

echo "Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com

echo "Setting default region to $REGION (Europe)..."
gcloud config set run/region "$REGION"
gcloud config set compute/region "$REGION"

echo ""
echo "Project $PROJECT_ID is ready."
echo "Region: $REGION (Europe)"
echo ""
echo "For Firebase Hosting (frontend):"
echo "  firebase use $PROJECT_ID   # or: firebase use --add (to add/link project)"
echo ""
echo "Next: Deploy backend with ./deploy-backend-europe.sh"
