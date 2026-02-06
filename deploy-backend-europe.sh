#!/usr/bin/env bash
# Deploy backend to Cloud Run (Europe)
# Run: ./deploy-backend-europe.sh

set -e

PROJECT_ID="${GCP_PROJECT_ID:-video-image-processing-eu}"
REGION="europe-west1"
SERVICE_NAME="video-image-api"

# CORS - set after first frontend deploy, or use * for testing
CORS_ORIGINS="${CORS_ORIGINS:-*}"

echo "Building and deploying to $REGION..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME --project $PROJECT_ID

gcloud run deploy $SERVICE_NAME \
  --project $PROJECT_ID \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars "CORS_ORIGINS=$CORS_ORIGINS" \
  --memory 1Gi \
  --cpu 2 \
  --timeout 300 \
  --cpu-boost

echo ""
echo "Backend deployed. Get URL with:"
echo "  gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)'"
