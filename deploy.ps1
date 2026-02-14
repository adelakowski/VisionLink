# Deploy VisionLink to Cloud Run and Firebase Hosting

$PROJECT_ID = "visionlinktriage"
$SERVICE_NAME = "visionlink"
$REGION = "us-east4"

Write-Host "Deploying VisionLink to Cloud Run..." -ForegroundColor Cyan

# Check if logged in to gcloud
gcloud auth list
if ($LASTEXITCODE -ne 0) {
    Write-Host "Please login to gcloud first." -ForegroundColor Red
    exit 1
}

# Set project
gcloud config set project $PROJECT_ID


# Build and Deploy to Cloud Run
# We use source deployment which builds the container via Cloud Build
Write-Host "Building and deploying to Cloud Run (this may take a few minutes)..." -ForegroundColor Yellow

# Note: Using --source . requires the Google Cloud SDK to zip and upload the context.
# Ensure .gcloudignore is set up or excludes large files.
gcloud run deploy $SERVICE_NAME `
    --source . `
    --region $REGION `
    --allow-unauthenticated `
    --project $PROJECT_ID `
    --gpu 1 `
    --memory 16Gi `
    --no-gpu-zonal-redundancy `
    --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "Cloud Run deployment failed." -ForegroundColor Red
    exit 1
}

Write-Host "Cloud Run deployment successful." -ForegroundColor Green

# Deploy Firebase Hosting
Write-Host "Deploying Firebase Hosting..." -ForegroundColor Cyan
firebase deploy --only hosting

if ($LASTEXITCODE -ne 0) {
    Write-Host "Firebase Hosting deployment failed." -ForegroundColor Red
    exit 1
}

Write-Host "Deployment complete!" -ForegroundColor Green
Write-Host "Access your app at the Firebase Hosting URL." -ForegroundColor Green
