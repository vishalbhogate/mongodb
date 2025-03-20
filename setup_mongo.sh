#!/bin/bash

set -e  # Exit on any error

# Function to check if Kind cluster exists
check_kind_cluster() {
    if kind get clusters | grep -q "mongo-cluster"; then
        echo "Kind cluster 'mongo-cluster' already exists. Skipping creation."
        return 0
    else
        return 1
    fi
}

# Install Kind
if ! command -v kind &> /dev/null; then
    echo "Installing Kind..."
    brew install kind
else
    echo "Kind is already installed."
fi

# Install kubectl
if ! command -v kubectl &> /dev/null; then
    echo "Installing kubectl..."
    brew install kubectl
else
    echo "kubectl is already installed."
fi

# Install Helm
if ! command -v helm &> /dev/null; then
    echo "Installing Helm..."
    brew install helm
else
    echo "Helm is already installed."
fi

# Check if Kind cluster exists; create if it doesn't
if ! check_kind_cluster; then
    echo "Creating Kind cluster..."
    kind create cluster --name mongo-cluster
fi

# Confirm cluster is running
kubectl cluster-info --context kind-mongo-cluster

# Add Bitnami Helm repository
echo "Adding Bitnami Helm repository..."
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Deploy MongoDB
echo "Deploying MongoDB..."
helm install mongodb bitnami/mongodb --set auth.rootPassword=secretpassword --set auth.username=admin --set auth.database=mydb

# Wait for MongoDB pod to be ready
echo "Waiting for MongoDB pod to be ready..."
echo "Waiting for MongoDB to be ready..."
kubectl wait --for=condition=available deploy/mongodb --timeout=300s || {
    echo "MongoDB is not ready. Check logs with: kubectl logs -l app.kubernetes.io/name=mongodb"
    exit 1
}

# Port-forward MongoDB service in the background
echo "Exposing MongoDB on localhost:27017..."
nohup kubectl port-forward svc/mongodb 27017:27017 > /dev/null 2>&1 &

# Install MongoDB client if not installed
if ! command -v mongosh &> /dev/null; then
    echo "Installing MongoDB client..."
    brew install mongosh
else
    echo "MongoDB client is already installed."
fi

# Connect to MongoDB
echo "Connecting to MongoDB..."
mongosh --host localhost --port 27017 -u root -p secretpassword --authenticationDatabase admin <<EOF
show dbs;
EOF

echo "Setup complete! MongoDB is running locally on Kind."
