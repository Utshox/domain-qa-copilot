import asyncio
import os
from dotenv import load_dotenv
from app.services.evaluator import evaluator
from app.services.generator import generator
from app.db.vector import vector_db

load_dotenv()

async def main():
    # 0. Seed the vector database with context
    print("Seeding in-memory vector database...")
    from langchain_core.documents import Document
    seed_docs = [
        Document(
            page_content="The copilot features ingestion, chunking, embedding, indexing, retrieval, answer generation, citations, and a feedback loop.",
            metadata={"source": "manual.pdf"}
        )
    ]
    vector_db.add_documents(seed_docs)

    # 1. Prepare a small test dataset
    # In a real scenario, you'd load this from a JSON file
    test_data = [
        {
            "question": "What are the main features of this copilot?",
            "ground_truth": "The copilot features ingestion, chunking, embedding, indexing, retrieval, answer generation, citations, and a feedback loop."
        }
    ]

    # 2. Generate answers and retrieve contexts for evaluation
    eval_dataset = []
    for item in test_data:
        print(f"Evaluating: {item['question']}")
        result = await generator.generate_answer(item['question'])
        
        # Ragas expects: question, answer, contexts, ground_truth
        eval_dataset.append({
            "question": item['question'],
            "answer": result['answer'],
            "contexts": [s.get('content', '') for s in result['sources']],
            "ground_truth": item['ground_truth']
        })

    # 3. Run Ragas evaluation
    if eval_dataset:
        print("Running Ragas metrics...")
        results = evaluator.run_evaluation(eval_dataset)
        print("\nEvaluation Results:")
        print(results)
    else:
        print("No data to evaluate.")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set OPENAI_API_KEY environment variable.")
    else:
        asyncio.run(main())
