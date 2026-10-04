from retrieval.retrieval_pipeline import RetrievalPipeline


# ============================================================
# TEST DATASET
# ============================================================

TEST_QUERIES = [

    {
        "question": "How does UserManager create a user?",
        "expected_name": "create_user"
    },

    {
        "question": "How does UserManager delete a user?",
        "expected_name": "delete_user"
    },

    {
        "question": "What does calculate_total do?",
        "expected_name": "calculate_total"
    },

    {
        "question": "Which async function fetches data?",
        "expected_name": "fetch_data"
    }

]


# ============================================================
# RETRIEVAL EVALUATION
# ============================================================

def calculate_metrics(pipeline=None):

    # Reuse existing pipeline when called
    # from the FastAPI backend.
    #
    # This prevents opening the same Qdrant
    # storage with multiple clients.

    if pipeline is None:

        pipeline = RetrievalPipeline(
            candidate_limit=5,
            final_limit=3
        )


    precision_scores = []

    recall_scores = []

    reciprocal_ranks = []


    for test in TEST_QUERIES:

        question = test["question"]

        expected_name = test["expected_name"]


        results = pipeline.search(
            question
        )


        top_k = len(results)

        relevant_count = 0

        first_relevant_rank = None


        for rank, document in enumerate(
            results,
            start=1
        ):

            name = document.get(
                "name",
                ""
            )


            if name == expected_name:

                relevant_count += 1


                if first_relevant_rank is None:

                    first_relevant_rank = rank


        # ====================================================
        # PRECISION@K
        # ====================================================

        if top_k > 0:

            precision_at_k = (
                relevant_count /
                top_k
            )

        else:

            precision_at_k = 0.0


        # ====================================================
        # RECALL@K
        # ====================================================

        if relevant_count > 0:

            recall_at_k = 1.0

        else:

            recall_at_k = 0.0


        # ====================================================
        # RECIPROCAL RANK
        # ====================================================

        if first_relevant_rank is not None:

            reciprocal_rank = (
                1 /
                first_relevant_rank
            )

        else:

            reciprocal_rank = 0.0


        precision_scores.append(
            precision_at_k
        )

        recall_scores.append(
            recall_at_k
        )

        reciprocal_ranks.append(
            reciprocal_rank
        )


    # ========================================================
    # FINAL METRICS
    # ========================================================

    total_tests = len(
        TEST_QUERIES
    )


    average_precision = (
        sum(precision_scores) /
        total_tests
    )


    average_recall = (
        sum(recall_scores) /
        total_tests
    )


    mean_reciprocal_rank = (
        sum(reciprocal_ranks) /
        total_tests
    )


    retrieval_accuracy = (
        sum(
            1
            for score in recall_scores
            if score > 0
        ) /
        total_tests
    )


    return {

        "total_test_queries":
            total_tests,

        "precision_at_3":
            round(
                average_precision,
                2
            ),

        "recall_at_3":
            round(
                average_recall,
                2
            ),

        "mrr":
            round(
                mean_reciprocal_rank,
                2
            ),

        "retrieval_accuracy":
            round(
                retrieval_accuracy,
                2
            )
    }


# ============================================================
# TERMINAL REPORT
# ============================================================

def evaluate_retrieval():

    metrics = calculate_metrics()


    print()

    print("=" * 70)

    print(
        "GitContext-AI Retrieval Evaluation"
    )

    print("=" * 70)


    print(
        f"Total Test Queries : "
        f"{metrics['total_test_queries']}"
    )


    print(
        f"Precision@3       : "
        f"{metrics['precision_at_3']:.2f}"
    )


    print(
        f"Recall@3          : "
        f"{metrics['recall_at_3']:.2f}"
    )


    print(
        f"MRR               : "
        f"{metrics['mrr']:.2f}"
    )


    print(
        f"Retrieval Accuracy: "
        f"{metrics['retrieval_accuracy']:.2f}"
    )


    print("=" * 70)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    evaluate_retrieval()