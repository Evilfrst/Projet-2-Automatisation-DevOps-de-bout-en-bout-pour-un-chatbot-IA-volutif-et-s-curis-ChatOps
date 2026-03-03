![devops_flowchart](https://github.com/user-attachments/assets/e73bb0c0-9062-42ab-837b-dfa2a9e06460)
# ChatOps
📁 Structure finale du projet

```
End-to-End-DevOps-Automation-AI-Chatbot
├── .github/
│ └── workflows/
│ └── ci-cd.yml # Main CI/CD automation pipeline
├── app/
│ └── main.py # FastAPI application source code
├── kubernetes/
│ ├── deployment.yaml # Kubernetes Deployment manifest
│ ├── service.yaml # Kubernetes Service manifest
│ ├── hpa.yaml # Horizontal Pod Autoscaler manifest
│ ├── ingress.yaml # Nginx Ingress manifest
│ └── kustomization.yaml # Kustomize file to manage all K8s manifests
├── tests/
│ └── test_main.py # Unit tests for the application
├── k6/
│ └── load-test.js # k6 script for performance testing
├── .gitignore # Files and directories to be ignored by Git
├── Dockerfile # Instructions to build the container image
├── README.md # This file - project documentation
└── requirements.txt # Python dependencies

```

# 🤖 ChatOps DevOps – Chatbot Interne

Projet DevOps démontrant un **chatbot interne pour équipes DevOps** avec **CI/CD + Docker + Kubernetes**.

---

## 🎯 Objectif
Permettre aux équipes techniques de :

- 🚀 Lancer un déploiement
- 📊 Consulter l’état des clusters Kubernetes
- 🚨 Voir les alertes et incidents

Le tout via une API accessible pour l’intégration dans Slack ou autres plateformes collaboratives.

---

## 🏗️ Architecture

```text
Utilisateur (Slack / API Client)
        ↓
Chatbot API (FastAPI)
        ↓
Docker
        ↓
Docker Hub
        ↓
Kubernetes Deployment & Service
        ↓
CI/CD GitHub Actions
```

## 🚀 Technologies utilisées

- **Backend**: Python with FastAPI
  
- **AI**: OpenAI GPT API
  
- **Containerization**: Docker
  
- **Orchestration**: Kubernetes
  
- **CI/CD**: GitHub Actions
  
- **Caching**: Redis
  
- **Security Scanning**: CodeQL, Trivy
  
- **Monitoring**: Prometheus
  
- **Performance Testing**: k6

## 📋 Fonctionnalités

###Commandes ChatOps :

-/deploy <service> <env> – déclenche un déploiement

-/cluster status – vérifie le cluster

-/alerts – affiche les alertes critiques

###Health checks Kubernetes (liveness / readiness)

###Conteneurisation et déploiement automatique via CI/CD

🚀 Lancer le projet en local

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Consultantsrihari/End-to-End-DevOps-Automation-AI-Chatbot.git
    cd <repo-name>
    ```

2.  **Set up environment variables:**
    Create a `.env` file in the root directory and add your OpenAI API key:
    ```
    OPENAI_API_KEY="your-openai-api-key"
    ```

3.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

4.  **Run the application locally:**
    The application will be available at `http://127.0.0.1:8000`.
    ```bash
    uvicorn app.main:app --reload
    ```

### Docker
1.  **Build the Docker image:**
    ```bash
    docker build -t chatbot-api:latest .
    ```

2.  **Run the Docker container:**
    ```bash
    docker run -d -p 8000:8000 --env-file .env --name chatbot-container chatbot-api:latest
    ```

### Kubernetes Deployment
1.  **Create a Kubernetes Secret** for your API key. Remember to base64 encode it.
    ```bash
    echo -n "your-openai-api-key" | base64
    ```
    Create a `secret.yaml` file (DO NOT commit this file if it contains real secrets):
    ```yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: chatbot-secrets
    type: Opaque
    data:
      OPENAI_API_KEY: "your-base64-encoded-key"
    ```
    Apply the secret: `kubectl apply -f secret.yaml`

2.  **Deploy the application:**
    The `kustomization.yaml` file groups all our Kubernetes manifests.
    ```bash
    kubectl apply -k ./kubernetes
    ```

3.  **Access the service:**
    If using Minikube, you can expose the service:
    ```bash
    minikube service chatbot-service
    ```
    If using a cloud provider, the `LoadBalancer` will provision a public IP address.

## CI/CD Pipeline
The pipeline is defined in `.github/workflows/ci-cd.yml` and automates the following steps on every push to `main`:
1.  **Test & Lint**: Runs `pytest`.
2.  **Security Scan**: Scans the code with GitHub CodeQL.
3.  **Build & Push**: Builds the Docker image and pushes it to Docker Hub.
4.  **Scan Image**: Scans the pushed Docker image for vulnerabilities with Trivy.
5.  **Deploy**: Deploys the new image to the Kubernetes cluster.

### Required GitHub Secrets
To make the CI/CD pipeline work, you must configure the following secrets in your GitHub repository settings:
- `DOCKER_USERNAME`: Your Docker Hub username.
- `DOCKER_PASSWORD`: Your Docker Hub password or access token.
- `KUBE_CONFIG`: Base64 encoded content of your `kubeconfig` file to allow GitHub Actions to access your cluster.
- `SLACK_WEBHOOK`: The webhook URL for sending Slack notifications.

## Performance Testing
To run the load test script:
```bash
# Make sure your service is accessible at the URL in the script
k6 run k6/load-test.js
```









