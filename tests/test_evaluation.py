from evaluation.retrieval_evaluation import (
    calculate_metrics
)


def test_retrieval_evaluation(
    retrieval_pipeline
):

    metrics = calculate_metrics(
        retrieval_pipeline
    )

    assert metrics["total_test_queries"] == 4

    assert 0 <= metrics["precision_at_3"] <= 1

    assert 0 <= metrics["recall_at_3"] <= 1

    assert 0 <= metrics["mrr"] <= 1

    assert 0 <= metrics["retrieval_accuracy"] <= 1

    assert metrics["recall_at_3"] == 1.0

    assert metrics["retrieval_accuracy"] == 1.0