def test_retrieval_pipeline(
    retrieval_pipeline
):

    results = retrieval_pipeline.search(
        "How does UserManager create a user?"
    )

    assert len(results) > 0

    names = [
        result["name"]
        for result in results
    ]

    assert "create_user" in names