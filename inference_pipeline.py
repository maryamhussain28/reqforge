# core/inference_pipeline.py

from .preprocessing import RequirementPreprocessor
from .embedding_engine import HashEmbeddingEngine
from .structuring_engine import RequirementStructurer
from .scoring_engine import HybridScoringEngine


class ReqForgeInferencePipeline:
    """
    End-to-end AI inference workflow.
    Designed for interactive real-time execution.
    """

    def __init__(self):
        self.preprocessor = RequirementPreprocessor()
        self.embedding_engine = HashEmbeddingEngine()
        self.structurer = RequirementStructurer()
        self.scorer = HybridScoringEngine()

    def process(self, requirement_text: str):
        # Step 1: Preprocessing
        processed = self.preprocessor.preprocess(requirement_text)

        # Step 2: Embedding Generation
        embedding = self.embedding_engine.generate(
            processed["normalized_text"]
        )

        # Step 3: Structuring Transformation
        structured = self.structurer.structure(processed["clauses"])

        # Step 4: Hybrid Evaluation
        score = self.scorer.evaluate(
            requirement_text,
            structured,
            embedding
        )

        return {
            "structured_output": structured,
            "evaluation": score
        }