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

# Load .env if it exists
if (Test-Path ".env") {
    Get-Content .env | Where-Object { $_ -match "^([^#].+?)=(.*)$" } | ForEach-Object {
        $name, $value = $_ -split '=', 2
        Set-Item -Path "Env:\$name" -Value $value
    }
}
$HF_TOKEN = $env:HF_TOKEN

# Set image URL using the existing Artifact Registry used by source deployments
$IMAGE_URL = "$REGION-docker.pkg.dev/$PROJECT_ID/cloud-run-source-deploy/$SERVICE_NAME"

Write-Host "Building Docker image using Cloud Build..." -ForegroundColor Yellow
gcloud builds submit --tag $IMAGE_URL .
if ($LASTEXITCODE -ne 0) {
    Write-Host "Image build failed." -ForegroundColor Red
    exit 1
}

gcloud run deploy $SERVICE_NAME --image $IMAGE_URL --region $REGION --allow-unauthenticated --project $PROJECT_ID --memory 16Gi --cpu 4 --gpu 1 --gpu-type nvidia-l4 --max-instances 1 --no-gpu-zonal-redundancy --timeout 3600 --set-env-vars HF_TOKEN=$HF_TOKEN --quiet

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
