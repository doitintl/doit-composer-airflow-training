#! /bin/bash

# Variables to set
PROJECT_ID=$(gcloud config get-value project)
#echo "Setting default GCP project to ${PROJECT_ID}"
#gcloud config set project ${PROJECT_ID}
COMPOSER_SERVICE_ACCOUNT_NAME="composer-training"

echo "Creating a service account for Composer environment to use"
gcloud iam service-accounts create ${COMPOSER_SERVICE_ACCOUNT_NAME} \
    --description="composer training service account" \
    --display-name="composer training service account"

COMPOSER_SERVICE_ACCOUNT_ID="${COMPOSER_SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
echo "Created service account: ${COMPOSER_SERVICE_ACCOUNT_ID}"

# https://cloud.google.com/composer/docs/how-to/access-control#service-account
echo "Adding composer.worker roles to the service account"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${COMPOSER_SERVICE_ACCOUNT_ID}" \
    --role="roles/composer.worker"

echo "Adding GCS and BigQuery admin roles for the service account to run this tutorial"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${COMPOSER_SERVICE_ACCOUNT_ID}" \
    --role="roles/storage.admin"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${COMPOSER_SERVICE_ACCOUNT_ID}" \
    --role="roles/bigquery.admin"

echo "Enabling Composer API, this will take a few minutes..."
gcloud services enable composer.googleapis.com

echo "Creating Cloud Composer, this will take ~25 minutes..."
gcloud composer environments create composer-training \
    --location us-central1 \
    --node-count 3 \
    --scheduler-count 1 \
    --disk-size 100 \
    --machine-type n1-standard-1 \
    --cloud-sql-machine-type db-n1-standard-2 \
    --web-server-machine-type composer-n1-webserver-2 \
    --image-version "composer-1.17.5-airflow-2.1.4" \
    --service-account ${COMPOSER_SERVICE_ACCOUNT_ID} \
    --zone us-central1-c
