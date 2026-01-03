# Object Identity AI on Google Cloud

## Problem
Existing lost-and-found and asset tracking systems fail under real-world noise, scale, and time-based changes in objects.

## Solution
We reconstruct **physical** object identity using probabilistic multimodal vision and Google Cloud, so the system can say “this is the same bag” even after wear, lighting changes, or partial views.

## Google Tech Used
- Cloud Run for scalable ingestion and preprocessing API
- Vertex AI (Gemini Vision + ViT-style embeddings) for multimodal reasoning
- Cloud Storage for raw and normalized image storage

## Architecture
(Insert diagram of: Client → Cloud Run → Storage + Vertex AI branches → Fusion → Identity Graph.)

## How to Run (Local)
- `uvicorn main:app --reload --port 8080`
- `curl -F "file=@sample.jpg" http://localhost:8080/analyze`

## How to Run (Cloud Run)
- `gcloud run deploy object-identity-api --source . --region asia-south1 --platform managed --allow-unauthenticated`
- `curl -F "file=@sample.jpg" YOUR_URL/analyze`

## Demo
- Live endpoint: `https://object-identity-api-xyz.a.run.app/analyze`
- Video link: (to be added)
