"""
End-to-end demo of AI Conversation Intelligence System
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.transcriber import get_transcriber
from src.core.chunker import get_chunker
from src.core.embedder import get_embeddings_generator
from src.rag.vector_store import get_vector_store
from src.rag.retriever import get_retriever
from src.analysis.summarizer import get_summarizer
from src.analysis.sentiment import get_sentiment_analyzer
from src.analysis.action_items import get_action_item_extractor
from src.analysis.qa import get_qa_engine


def demo_1_transcription():
    """Demo 1: Transcribe audio"""
    print("\n" + "="*80)
    print("DEMO 1: Audio Transcription")
    print("="*80)

    try:
        # NOTE: Replace with your actual audio file path
        audio_path = Path("data/sample_conversation.wav")

        if not audio_path.exists():
            print(f"⚠️ Audio file not found at {audio_path}")
            print("To use this demo, place an audio file at: data/sample_conversation.wav")
            return None

        transcriber = get_transcriber()
        result = transcriber.transcribe(audio_path)

        print(f"\n📝 Transcription Result:")
        print(f"Text: {result['text'][:500]}...")
        print(f"Language: {result['language']}")
        print(f"Duration: {result['duration']:.2f}s")

        return result["text"]

    except Exception as e:
        print(f"❌ Transcription failed: {e}")
        return None


def demo_2_chunking(text: str = None):
    """Demo 2: Text chunking"""
    print("\n" + "="*80)
    print("DEMO 2: Text Chunking")
    print("="*80)

    if not text:
        # Use sample text
        text = """
        Customer: Hi, I want to discuss our Q4 marketing budget. We need to allocate 
        resources better.
        
        Manager: Sure, let's break it down by channel. Social media is performing well.
        We should increase investment there.
        
        Customer: That makes sense. What about email marketing?
        
        Manager: Email has good ROI. I propose increasing it by 30%. We should hire 
        a specialist for this.
        
        Customer: Good idea. What's the timeline?
        
        Manager: We can start recruitment next week. The role should be filled by 
        end of month.
        
        Customer: Excellent. So action items are: increase social budget, increase 
        email budget 30%, and start hiring. Due end of month?
        
        Manager: Correct. I'll prepare the detailed budget doc by Friday.
        """

    chunker = get_chunker()
    chunks = chunker.chunk(text, method="paragraphs")

    print(f"\n📚 Chunking Results:")
    print(f"Total chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks[:3]):
        print(f"\nChunk {chunk['id']}:")
        print(f"Text: {chunk['text'][:150]}...")
        print(f"Size: {chunk['end'] - chunk['start']} chars")

    return text, chunks


def demo_3_embeddings(chunks: list):
    """Demo 3: Generate embeddings"""
    print("\n" + "="*80)
    print("DEMO 3: Embeddings Generation")
    print("="*80)

    try:
        embeddings_gen = get_embeddings_generator()
        chunks_with_embeddings = embeddings_gen.embed_chunks(chunks)

        print(f"\n🔢 Embeddings Generated:")
        print(f"Dimension: {embeddings_gen.get_dimension()}")
        print(f"Chunks embedded: {len(chunks_with_embeddings)}")

        return chunks_with_embeddings

    except Exception as e:
        print(f"❌ Embedding generation failed: {e}")
        return None


def demo_4_vector_store(chunks: list):
    """Demo 4: Vector store operations"""
    print("\n" + "="*80)
    print("DEMO 4: Vector Store Management")
    print("="*80)

    try:
        vector_store = get_vector_store()

        # Add embeddings
        embeddings_array = [
            chunk.pop("embedding") for chunk in chunks
        ]
        vector_store.add_embeddings(embeddings_array, chunks)

        stats = vector_store.get_stats()
        print(f"\n📊 Vector Store Stats:")
        print(f"Total entries: {stats['total_entries']}")
        print(f"Dimension: {stats['dimension']}")

        return vector_store

    except Exception as e:
        print(f"❌ Vector store operation failed: {e}")
        return None


def demo_5_retrieval(text: str):
    """Demo 5: RAG retrieval"""
    print("\n" + "="*80)
    print("DEMO 5: RAG Retrieval")
    print("="*80)

    try:
        query = "What are the action items discussed?"
        retriever = get_retriever()
        results = retriever.retrieve(query, top_k=3)

        print(f"\n🔍 Retrieval Results for: '{query}'")
        print(f"Found: {len(results)} relevant chunks")
        for i, result in enumerate(results):
            print(f"\nResult {i+1}:")
            print(f"Text: {result['text'][:150]}...")
            print(f"Similarity: {result['similarity_score']:.3f}")

        return results

    except Exception as e:
        print(f"❌ Retrieval failed: {e}")
        return None


def demo_6_summarization(text: str):
    """Demo 6: Conversation summarization"""
    print("\n" + "="*80)
    print("DEMO 6: Conversation Summarization")
    print("="*80)

    try:
        summarizer = get_summarizer()

        # Full summary
        print("\n📄 Full Summary:")
        result = summarizer.summarize_full(text)
        print(result["summary"][:500])

        # Bullet points
        print("\n📌 Bullet Points:")
        result = summarizer.summarize_bullet_points(text)
        print(result["bullet_points"][:300])

    except Exception as e:
        print(f"❌ Summarization failed: {e}")


def demo_7_sentiment(text: str):
    """Demo 7: Sentiment analysis"""
    print("\n" + "="*80)
    print("DEMO 7: Sentiment Analysis")
    print("="*80)

    try:
        analyzer = get_sentiment_analyzer()

        # Overall sentiment
        print("\n😊 Overall Sentiment:")
        result = analyzer.analyze_overall(text)
        print(result["analysis"][:400])

        # Issue detection
        print("\n⚠️ Issues Detected:")
        result = analyzer.detect_issues(text)
        print(result["issues_detected"][:300])

    except Exception as e:
        print(f"❌ Sentiment analysis failed: {e}")


def demo_8_action_items(text: str):
    """Demo 8: Action item extraction"""
    print("\n" + "="*80)
    print("DEMO 8: Action Item Extraction")
    print("="*80)

    try:
        extractor = get_action_item_extractor()

        # Extract action items
        print("\n✅ Action Items:")
        result = extractor.extract_action_items(text)
        print(result["action_items"][:500])

        # Extract decisions
        print("\n🎯 Decisions:")
        result = extractor.extract_decisions(text)
        print(result["decisions"][:300])

    except Exception as e:
        print(f"❌ Action item extraction failed: {e}")


def demo_9_qa(text: str):
    """Demo 9: Q&A"""
    print("\n" + "="*80)
    print("DEMO 9: Question Answering")
    print("="*80)

    try:
        qa_engine = get_qa_engine()

        questions = [
            "What budget changes were discussed?",
            "Who should be hired?",
            "When is the deadline?",
        ]

        for question in questions:
            print(f"\n❓ Q: {question}")
            result = qa_engine.answer_question(question)
            print(f"✅ A: {result['answer'][:300]}...")

    except Exception as e:
        print(f"❌ Q&A failed: {e}")


def main():
    """Run all demos"""
    print("\n" + "="*80)
    print("AI CONVERSATION INTELLIGENCE SYSTEM - DEMO")
    print("="*80)

    # Demo 1: Transcription (skip if no audio file)
    transcribed_text = demo_1_transcription()

    # Use sample text if transcription not available
    if not transcribed_text:
        _, chunks = demo_2_chunking()
    else:
        _, chunks = demo_2_chunking(transcribed_text)

    # Demo 3: Embeddings
    chunks_with_embeddings = demo_3_embeddings(chunks)

    # Demo 4: Vector store
    if chunks_with_embeddings:
        demo_4_vector_store(chunks_with_embeddings)

    # Use text for demos
    sample_text = """Customer: Hi, I want to discuss our Q4 marketing budget. We need to allocate 
resources better. Manager: Sure, let's break it down by channel. Social media is performing well.
We should increase investment there. Customer: That makes sense. What about email marketing?
Manager: Email has good ROI. I propose increasing it by 30%. We should hire a specialist for this.
Customer: Good idea. What's the timeline? Manager: We can start recruitment next week."""

    # Demo 5: Retrieval
    # demo_5_retrieval(sample_text)

    # Demo 6-9: Analysis (requires API keys)
    print("\n" + "="*80)
    print("NOTE: Analysis demos require OPENAI_API_KEY environment variable")
    print("="*80)
    print("\nTo run analysis demos, set: export OPENAI_API_KEY='your-key'")
    print("Then uncomment the analysis demos in this script.")

    print("\n" + "="*80)
    print("DEMO COMPLETED!")
    print("="*80)


if __name__ == "__main__":
    main()
