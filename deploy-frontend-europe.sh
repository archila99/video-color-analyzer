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

FIREBASE_PROJECT_ID="${FIREBASE_PROJECT_ID:-video-image-processing-e-30530}"
echo "Deploying to Firebase Hosting (project: $FIREBASE_PROJECT_ID)..."
firebase deploy --only hosting --project "$FIREBASE_PROJECT_ID"

echo ""
echo "Frontend deployed to https://${FIREBASE_PROJECT_ID}.web.app"
echo "To update backend CORS, run: ./deploy-all-europe.sh (or re-run step 4)"
