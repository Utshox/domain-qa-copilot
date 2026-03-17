from typing import List, Dict, Any
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from datasets import Dataset
from langchain_google_vertexai import ChatVertexAI, VertexAIEmbeddings
from app.core.config import settings

class EvaluationService:
    def __init__(self):
        self.llm = ChatVertexAI(
            model_name="gemini-1.5-flash",
            project=settings.GOOGLE_CLOUD_PROJECT
        )
        self.embeddings = VertexAIEmbeddings(
            model_name="text-multilingual-embedding-002",
            project=settings.GOOGLE_CLOUD_PROJECT
        )

    def run_evaluation(self, test_dataset: List[Dict[str, Any]]) -> Dict[Any, Any]:
        """
        test_dataset should be a list of dicts with:
        question: list, answer: list, contexts: list of lists, ground_truth: list
        """
        dataset = Dataset.from_list(test_dataset)
        
        result = evaluate(
            dataset=dataset,
            metrics=[
                faithfulness,
                answer_relevancy,
                context_precision,
            ],
            llm=self.llm,
            embeddings=self.embeddings,
        )
        
        return result
evaluator = EvaluationService()
