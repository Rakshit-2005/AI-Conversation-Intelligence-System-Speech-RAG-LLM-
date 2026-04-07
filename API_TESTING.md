"""
API Testing Examples - Common Use Cases

This file contains curl commands and Python examples for testing the API
"""

# ============================================================================
# 1. HEALTH CHECK
# ============================================================================

"""
Verify the system is running and healthy
"""

# Curl:
curl http://localhost:8000/health

# Python:
import requests
response = requests.get("http://localhost:8000/health")
print(response.json())


# ============================================================================
# 2. TRANSCRIPTION
# ============================================================================

"""
Convert audio file to text
"""

# Curl:
curl -X POST "http://localhost:8000/transcribe" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_path": "data/sample_meeting.wav",
    "language": "en"
  }'

# Python:
import requests

response = requests.post(
    "http://localhost:8000/transcribe",
    json={
        "audio_path": "data/sample_meeting.wav",
        "language": "en"
    }
)
print(response.json())


# ============================================================================
# 3. PROCESS FULL CONVERSATION
# ============================================================================

"""
Complete pipeline: Transcribe → Chunk → Embed → Index
"""

# Curl:
curl -X POST "http://localhost:8000/process-conversation" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_path": "data/sample_meeting.wav"
  }'

# Python:
response = requests.post(
    "http://localhost:8000/process-conversation",
    json={
        "audio_path": "data/sample_meeting.wav"
    }
)
result = response.json()
print(f"Chunks created: {result['chunks_created']}")
print(f"Processing time: {result['processing_time_seconds']:.2f}s")


# ============================================================================
# 4. SEMANTIC SEARCH / RETRIEVAL
# ============================================================================

"""
Find relevant conversation segments for a query
"""

# Curl:
curl -X POST "http://localhost:8000/retrieve" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the budget constraints?",
    "top_k": 5,
    "threshold": 0.3
  }'

# Python:
response = requests.post(
    "http://localhost:8000/retrieve",
    json={
        "query": "What are the budget constraints?",
        "top_k": 5,
        "threshold": 0.3
    }
)
results = response.json()
for result in results['chunks']:
    print(f"Similarity: {result['similarity_score']:.3f}")
    print(f"Text: {result['text'][:150]}...\n")


# ============================================================================
# 5. SUMMARIZATION
# ============================================================================

"""
A) Full Summary
"""

# Curl:
curl -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Customer called about product issues. Performance was slow on their system. We discussed upgrading their plan and scheduling a technical review.",
    "type": "full"
  }'

# Python:
response = requests.post(
    "http://localhost:8000/summarize",
    json={
        "text": "Customer called about product issues...",
        "type": "full"
    }
)
print(response.json()['summary'])


"""
B) Bullet Points
"""

# Curl:
curl -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Conversation text here...",
    "type": "bullet_points"
  }'

# Python:
response = requests.post(
    "http://localhost:8000/summarize",
    json={
        "text": "Conversation text here...",
        "type": "bullet_points"
    }
)
print(response.json()['summary'])


"""
C) Contextual/Business Summary
"""

# Curl:
curl -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Conversation text here...",
    "type": "contextual"
  }'


# ============================================================================
# 6. SENTIMENT ANALYSIS
# ============================================================================

"""
A) Overall Sentiment
"""

# Curl:
curl -X POST "http://localhost:8000/sentiment" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Great meeting! We made good progress. Everyone seems motivated.",
    "analysis_type": "overall"
  }'

# Python:
response = requests.post(
    "http://localhost:8000/sentiment",
    json={
        "text": "Great meeting! We made good progress...",
        "analysis_type": "overall"
    }
)
print(response.json()['analysis'])


"""
B) Per-Speaker Sentiment
"""

# Curl:
curl -X POST "http://localhost:8000/sentiment" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Customer: I'm frustrated with the service.\nAgent: I understand. Let me help you.",
    "analysis_type": "by_speaker"
  }'


"""
C) Issue Detection
"""

# Curl:
curl -X POST "http://localhost:8000/sentiment" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "We have a critical bug in production. Response time is 500ms.",
    "analysis_type": "issues"
  }'


"""
D) Satisfaction Analysis
"""

# Curl:
curl -X POST "http://localhost:8000/sentiment" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Customer is happy with the solution. Quick resolution appreciated.",
    "analysis_type": "satisfaction"
  }'


# ============================================================================
# 7. ACTION ITEM EXTRACTION
# ============================================================================

"""
A) Full Action Items
"""

# Curl:
curl -X POST "http://localhost:8000/action-items" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Manager: I'll send the budget by Friday. Developer: I'll fix the bug by tomorrow.",
    "extraction_type": "full"
  }'

# Python:
response = requests.post(
    "http://localhost:8000/action-items",
    json={
        "text": "Manager: I'll send...",
        "extraction_type": "full"
    }
)
print(response.json()['items'])


"""
B) Decisions Only
"""

# Curl:
curl -X POST "http://localhost:8000/action-items" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "We decided to increase budget by 30%. We also decided to hire a new manager.",
    "extraction_type": "decisions_only"
  }'


"""
C) Deadlines Only
"""

# Curl:
curl -X POST "http://localhost:8000/action-items" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Deadline is next Friday. We need to complete this by next quarter.",
    "extraction_type": "deadlines_only"
  }'


"""
D) Risks Only
"""

# Curl:
curl -X POST "http://localhost:8000/action-items" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Risk: Server might go down. Resource constraint: Only 2 engineers available.",
    "extraction_type": "risks_only"
  }'


# ============================================================================
# 8. QUESTION ANSWERING (Q&A)
# ============================================================================

"""
A) Simple Q&A
"""

# Curl:
curl -X POST "http://localhost:8000/qa" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main goal of this project?",
    "context": "We discussed building an AI system to analyze conversations and extract insights."
  }'

# Python:
response = requests.post(
    "http://localhost:8000/qa",
    json={
        "question": "What is the main goal?",
        "context": "We discussed building..."
    }
)
answer = response.json()
print(f"Answer: {answer['answer']}")
print(f"Confidence: {answer['confidence']:.2f}")


"""
B) Q&A with Context Retrieval (RAG)
"""

# First process conversation:
requests.post(
    "http://localhost:8000/process-conversation",
    json={"audio_path": "data/meeting.wav"}
)

# Then ask question:
response = requests.post(
    "http://localhost:8000/qa",
    json={
        "question": "What were the action items from the meeting?"
    }
)
print(response.json()['answer'])


"""
C) Search and Explain
"""

# Curl:
curl -X POST "http://localhost:8000/search-explain" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "pricing discussion"
  }'


# ============================================================================
# 9. COMPREHENSIVE ANALYSIS
# ============================================================================

"""
All-in-one analysis of a conversation
"""

# Curl:
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Customer meeting transcript here...",
    "include_summary": true,
    "include_sentiment": true,
    "include_action_items": true,
    "include_themes": true,
    "include_risks": true
  }'

# Python:
response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "text": "Customer meeting transcript...",
        "include_summary": true,
        "include_sentiment": true,
        "include_action_items": true,
        "include_themes": true,
        "include_risks": true
    }
)
result = response.json()
print("=== SUMMARY ===")
print(result['summary'])
print("\n=== SENTIMENT ===")
print(result['sentiment'])
print("\n=== ACTION ITEMS ===")
print(result['action_items'])
print(f"\nAnalysis completed in {result['analysis_time_seconds']:.2f}s")


# ============================================================================
# 10. VECTOR STORE MANAGEMENT
# ============================================================================

"""
A) Get Statistics
"""

# Curl:
curl http://localhost:8000/vector-store/stats

# Python:
response = requests.get("http://localhost:8000/vector-store/stats")
stats = response.json()
print(f"Total entries: {stats['total_entries']}")


"""
B) Clear Index (use with caution!)
"""

# Curl:
curl -X POST "http://localhost:8000/vector-store/clear"

# Python:
response = requests.post("http://localhost:8000/vector-store/clear")
print(response.json())


# ============================================================================
# COMPLETE WORKFLOW EXAMPLE
# ============================================================================

"""
End-to-end workflow in Python
"""

import requests
import json

BASE_URL = "http://localhost:8000"

# 1. Check health
print("1. Checking health...")
resp = requests.get(f"{BASE_URL}/health")
print(f"Status: {resp.json()['status']}\n")

# 2. Process audio file
print("2. Processing conversation...")
resp = requests.post(
    f"{BASE_URL}/process-conversation",
    json={"audio_path": "data/meeting.wav"}
)
process_result = resp.json()
print(f"Chunks created: {process_result['chunks_created']}\n")

# 3. Ask questions
print("3. Asking questions...")
questions = [
    "What are the main topics?",
    "What are the action items?",
    "What was the sentiment?",
]

for question in questions:
    resp = requests.post(
        f"{BASE_URL}/qa",
        json={"question": question}
    )
    answer = resp.json()
    print(f"Q: {question}")
    print(f"A: {answer['answer']}\n")

# 4. Comprehensive analysis
print("4. Running comprehensive analysis...")
resp = requests.post(
    f"{BASE_URL}/analyze",
    json={
        "text": "Meeting transcript...",
        "include_summary": True,
        "include_sentiment": True,
        "include_action_items": True
    }
)
analysis = resp.json()
print(f"Analysis completed in {analysis['analysis_time_seconds']:.2f}s\n")

# 5. Vector store stats
print("5. Checking vector store...")
resp = requests.get(f"{BASE_URL}/vector-store/stats")
stats = resp.json()
print(f"Total indexed entries: {stats['total_entries']}")


# ============================================================================
# ERROR HANDLING EXAMPLE
# ============================================================================

"""
Proper error handling in API calls
"""

import requests
from requests.exceptions import RequestException

def api_call_with_error_handling(endpoint, data):
    try:
        response = requests.post(
            f"http://localhost:8000{endpoint}",
            json=data,
            timeout=30
        )
        response.raise_for_status()  # Raise exception for bad status
        return response.json()
    
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Is it running?")
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e.response.status_code}")
        print(f"Details: {e.response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")

# Usage:
result = api_call_with_error_handling(
    "/qa",
    {"question": "What happened?"}
)
if result:
    print(result)
