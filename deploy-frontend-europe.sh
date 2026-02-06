#!/usr/bin/env bash
# Deploy frontend to Firebase Hosting (uses nearest CDN - includes Europe)
# Run: ./deploy-frontend-europe.sh
# Requires: BACKEND_URL env or pass as first arg

set -e

BACKEND_URL="${1:-$BACKEND_URL}"
if [ -z "$BACKEND_URL" ]; then
  echo "Usage: BACKEND_URL=https://your-backend.run.app ./deploy-frontend-europe.sh"
  echo "   or: ./deploy-frontend-europe.sh https://your-backend.run.app"
  exit 1
fi

echo "Building frontend with VITE_API_URL=$BACKEND_URL"
cd frontend
VITE_API_URL="$BACKEND_URL" npm run build
cd ..

echo "Deploying to Firebase Hosting..."
firebase deploy --only hosting

echo ""
echo "Frontend deployed. Update backend CORS with your Firebase URL:"
echo "  gcloud run services update video-image-api --region europe-west1 --set-env-vars CORS_ORIGINS=https://YOUR_PROJECT.web.app"
