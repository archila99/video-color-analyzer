#!/usr/bin/env bash
# Full deployment: backend → frontend → CORS update
# Run: ./deploy-all-europe.sh
# Requires: gcloud, firebase CLI, and authentication

set -e

GCP_PROJECT_ID="${GCP_PROJECT_ID:-video-image-processing-eu}"
FIREBASE_PROJECT_ID="${FIREBASE_PROJECT_ID:-video-image-processing-e-30530}"
REGION="europe-west1"
SERVICE_NAME="video-image-api"

echo "=== 1/4 Deploying backend to Cloud Run ($REGION) ==="
gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/$SERVICE_NAME --project $GCP_PROJECT_ID

gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$GCP_PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --project $GCP_PROJECT_ID \
  --allow-unauthenticated \
  --set-env-vars "CORS_ORIGINS=*" \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --cpu-boost \
  --quiet

BACKEND_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --project $GCP_PROJECT_ID --format 'value(status.url)')
echo "Backend URL: $BACKEND_URL"

echo ""
echo "=== 2/4 Building frontend with VITE_API_URL=$BACKEND_URL ==="
cd frontend
VITE_API_URL="$BACKEND_URL" npm run build
cd ..

echo ""
echo "=== 3/4 Deploying frontend to Firebase Hosting ==="
firebase deploy --only hosting --project "$FIREBASE_PROJECT_ID" --non-interactive

FRONTEND_URL="https://${FIREBASE_PROJECT_ID}.web.app"
echo "Frontend URL: $FRONTEND_URL"

echo ""
echo "=== 4/4 Updating backend CORS with frontend URL ==="
CORS_VAL="${FRONTEND_URL},https://${FIREBASE_PROJECT_ID}.firebaseapp.com"
# Use env-vars-file to handle commas in CORS_ORIGINS (gcloud parses commas as pair delimiters)
ENV_FILE=$(mktemp)
trap "rm -f $ENV_FILE" EXIT
echo "CORS_ORIGINS: \"$CORS_VAL\"" > "$ENV_FILE"
gcloud run services update $SERVICE_NAME \
  --region $REGION \
  --project $GCP_PROJECT_ID \
  --env-vars-file "$ENV_FILE" \
  --quiet

echo ""
echo "=== Deployment complete ==="
echo "Backend:  $BACKEND_URL"
echo "Frontend: $FRONTEND_URL"
echo ""
echo "Open: $FRONTEND_URL"
