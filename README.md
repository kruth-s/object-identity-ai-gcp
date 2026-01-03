# Object Identity AI (GCP)
Multi-Branch Visual Fingerprinting & Probabilistic Matching System

A production-ready, multi-branch object identity system deployed on Google Cloud Platform.
The system ingests real-world images and reconstructs persistent object identity using complementary visual signals, uncertainty-aware evidence fusion, and explainable AI.

This is not image search.
This system reasons about physical object continuity over time.

---

## Core Capabilities

- Robust to angle, lighting, damage, occlusion, and partial views
- Tracks object identity evolution across sightings
- Probabilistic, uncertainty-aware matching
- Fully explainable results (heatmaps + natural language)
- Designed for Cloud Run + Vertex AI production deployment

---

## System Overview

“We do not search images. We reconstruct physical object identity using multi-signal intelligence.”

---

## High-Level Request Flow

1. Image ingestion & normalization
2. Parallel multi-branch feature extraction
3. Evidence-based probabilistic fusion
4. Top-K identity ranking
5. Explainability generation
6. Self-improving feedback loop

---

## Feature Branches

### Branch A — Manufacturing Signature
- ViT patch variance (latent manufacturing noise)
- CLIP image embeddings

### Branch B — Multi-Modal Ghost Matching
- Gemini Vision understanding
- MediaPipe geometry
- Custom ghost signals

### Branch C — Partial Object Completion
- Mask generation
- Edge & depth priors
- Imagen inpainting
- Completion embeddings

### Branch D — Negative-Space Matching
- Void signatures (128D)
- Structural absence reasoning

### Branch E — Visual Semantic Grounding
- Vertex AI Multimodal Embeddings

---

## Evidence-Based Fusion

- TensorFlow Probability
- Beta distributions per branch
- Reliability-weighted sampling
- Confidence interval estimation

---

## Match Ranking

- Top-K candidates
- Time decay
- Optional location consistency

---

## Explainability

- ViT Grad-CAM heatmaps (stored in GCS)
- Gemini-generated natural language explanations

---

## Tech Stack

Runtime: FastAPI on Cloud Run  
Storage: GCS, Firestore  
AI/ML: Vertex AI (Gemini, Multimodal Embeddings, Imagen), MediaPipe, PyTorch, TFP

---

## Repository Structure

Refer to repository tree in documentation.

---

## API Endpoints

GET /health  
POST /analyze  
POST /feedback  

---

## GCP Setup

Enable:
- Cloud Run
- Cloud Storage
- Firestore
- Vertex AI

---

## Deployment

Use Cloud Run with environment variables for GCS, Gemini, Imagen, and embeddings.

---

## Firestore Data Model

objects/{object_id}  
sightings/{sighting_id}  
fusion/reliability  

---

## Performance Notes

- CPU Cloud Run works; GPU optional
- 2–4Gi memory recommended

---

## Security

- Least-privilege IAM
- Signed URLs if private

---

## License

MIT or Apache-2.0
