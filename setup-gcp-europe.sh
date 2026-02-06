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
if ! gcloud services enable cloudbuild.googleapis.com run.googleapis.com artifactregistry.googleapis.com firebase.googleapis.com firebasehosting.googleapis.com 2>/dev/null; then
  echo ""
  echo "ERROR: Could not enable APIs. Billing must be enabled for this project."
  echo ""
  echo "Fix:"
  echo "  1. Open https://console.cloud.google.com/billing"
  echo "  2. Select project: $PROJECT_ID"
  echo "  3. Link a billing account (or create one)"
  echo "  4. Run this script again: ./setup-gcp-europe.sh"
  echo ""
  exit 1
fi

echo "Setting default region to $REGION (Europe)..."
gcloud config set run/region "$REGION"
gcloud config set compute/region "$REGION"

SA_NAME="github-actions"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
echo ""
echo "Creating service account for GitHub Actions: $SA_NAME"
gcloud iam service-accounts create "$SA_NAME" \
  --description="Deploy from GitHub Actions" \
  --display-name="GitHub Actions Deploy" \
  --project="$PROJECT_ID" 2>/dev/null || echo "Service account may already exist"

echo "Granting roles to $SA_EMAIL..."
for role in roles/cloudbuild.builds.builder roles/run.admin roles/iam.serviceAccountUser roles/storage.admin; do
  gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="$role" \
    --quiet 2>/dev/null || true
done

echo ""
echo "Project $PROJECT_ID is ready."
echo "Region: $REGION (Europe)"
echo ""
echo "For Firebase Hosting (frontend):"
echo "  firebase use video-image-processing-e-30530   # or create project at https://console.firebase.google.com/"
echo ""
echo "For GitHub Actions CI/CD, create a key and add as GCP_SA_KEY secret:"
echo "  gcloud iam service-accounts keys create key.json --iam-account=${SA_EMAIL}"
echo "  # Copy key.json contents to GitHub Settings → Secrets → GCP_SA_KEY"
echo ""
echo "Next: Deploy with ./deploy-all-europe.sh"
