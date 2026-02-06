#!/usr/bin/env bash
# Full deployment: backend → frontend → CORS update
# Run: ./deploy-all-europe.sh
# Requires: gcloud, firebase CLI, and authentication

set -e

PROJECT_ID="${GCP_PROJECT_ID:-video-image-processing-eu}"
REGION="europe-west1"
SERVICE_NAME="video-image-api"

echo "=== 1/4 Deploying backend to Cloud Run ($REGION) ==="
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars "CORS_ORIGINS=*" \
  --quiet

BACKEND_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)')
echo "Backend URL: $BACKEND_URL"

echo ""
echo "=== 2/4 Building frontend with VITE_API_URL=$BACKEND_URL ==="
cd frontend
VITE_API_URL="$BACKEND_URL" npm run build
cd ..

echo ""
echo "=== 3/4 Deploying frontend to Firebase Hosting ==="
firebase deploy --only hosting --non-interactive

FRONTEND_URL=$(firebase hosting:channel:list 2>/dev/null | head -1 || echo "https://$PROJECT_ID.web.app")
echo "Frontend URL: https://$PROJECT_ID.web.app"

echo ""
echo "=== 4/4 Updating backend CORS with frontend URL ==="
gcloud run services update $SERVICE_NAME \
  --region $REGION \
  --set-env-vars "CORS_ORIGINS=https://$PROJECT_ID.web.app,https://$PROJECT_ID.firebaseapp.com" \
  --quiet

echo ""
echo "=== Deployment complete ==="
echo "Backend:  $BACKEND_URL"
echo "Frontend: https://$PROJECT_ID.web.app"
echo ""
echo "Open: https://$PROJECT_ID.web.app"
