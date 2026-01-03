# Object Identity AI (GCP)
Multi-Branch Visual Fingerprinting & Probabilistic Matching System

A production-ready, multi-branch object identity system deployed on Google Cloud Platform.
The system ingests real-world images and reconstructs persistent object identity using complementary visual signals, uncertainty-aware evidence fusion, and explainable AI.

This is not image search.
This system reasons about physical object continuity over time.


## Core Capabilities

- Robust to angle, lighting, damage, occlusion, and partial views
- Tracks object identity evolution across sightings
- Probabilistic, uncertainty-aware matching
- Fully explainable results (heatmaps + natural language)
- Designed for Cloud Run + Vertex AI production deployment


## System Overview

> “We do not search images. We reconstruct physical object identity using multi-signal intelligence.”

<p align="center">
  <img src="images/01.png" alt="System Overview" width="550"/>
</p>


### Visual Walkthrough (End‑to‑End Pipeline)

<p align="center"><em>From ingestion → identity reconstruction → ranking → explainability</em></p>


### Feature Branches

### Branch A — Manufacturing Signature
- ViT patch variance (latent manufacturing noise)
- CLIP image embeddings
<p align="center"><img src="images/03.png" width="450"/></p>

### Branch B — Multi-Modal Ghost Matching
- Gemini Vision understanding
- MediaPipe geometry
- Custom ghost signals
<p align="center"><img src="images/04.png" width="450"/></p>

### Branch C — Partial Object Completion
- Mask generation
- Edge & depth priors
- Imagen inpainting
- Completion embeddings
<p align="center"><img src="images/05.png" width="450"/></p>

### Branch D — Negative-Space Matching
- Void signatures (128D)
- Structural absence reasoning
<p align="center"><img src="images/06.png" width="450"/></p>

### Branch E — Visual Semantic Grounding
- Vertex AI Multimodal Embeddings
<p align="center"><img src="images/07.png" width="450"/></p>

## Tech Stack

Runtime: FastAPI on Cloud Run  
Storage: GCS, Firestore  
AI/ML: Vertex AI (Gemini, Multimodal Embeddings, Imagen), MediaPipe, PyTorch, TFP
<p align="center">
  <img src="images/image.png" alt="System Overview" width="480"/>
</p>

## API Endpoints and GCP Setup

GET /health  
POST /analyze  
POST /feedback  
Enable:
- Cloud Run
- Cloud Storage
- Firestore
- Vertex AI

## Deployment and Firestore Data Model

Use Cloud Run with environment variables for GCS, Gemini, Imagen, and embeddings.
objects/{object_id}  
sightings/{sighting_id}  
fusion/reliability  

## Performance Notes and Security

- CPU Cloud Run works; GPU optional
- 2–4Gi memory recommended
- Least-privilege IAM
- Signed URLs if private

## License

MIT or Apache-2.0
