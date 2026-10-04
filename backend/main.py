from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import time
import os

from retrieval.retrieval_pipeline import RetrievalPipeline
from evaluation.retrieval_evaluation import calculate_metrics


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="GitContext-AI",
    description="AI-powered codebase intelligence and RAG API",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# RETRIEVAL PIPELINE
# ============================================================

pipeline = None


def get_pipeline():

    global pipeline

    if pipeline is None:

        pipeline = RetrievalPipeline(
            candidate_limit=5,
            final_limit=3
        )

    return pipeline


# ============================================================
# REQUEST MODEL
# ============================================================

class QuestionRequest(BaseModel):

    question: str


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "GitContext-AI API is running",
        "status": "healthy"
    }


# ============================================================
# ASK ENDPOINT
# ============================================================

@app.post("/ask")
def ask_question(
    request: QuestionRequest
):

    question = request.question.strip()

    start_time = time.perf_counter()


    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )


    try:

        result = get_pipeline().answer_with_sources(
            question
        )


        elapsed_time = (
            time.perf_counter()
            - start_time
        )


        return {

            "question":
                question,

            "answer":
                result["answer"],

            "sources":
                result["sources"],

            "status":
                "success",

            "metrics": {

                "response_time_seconds":
                    round(
                        elapsed_time,
                        2
                    ),

                "sources_retrieved":
                    len(
                        result["sources"]
                    ),

                "final_results":
                    len(
                        result["sources"]
                    ),

                "model":
                    os.getenv(
                        "GEMINI_MODEL",
                        "gemini-3.5-flash-lite"
                    )
            }
        }


    except RuntimeError as error:

        print(
            f"LLM service error: {error}"
        )


        raise HTTPException(

            status_code=503,

            detail={

                "message":
                    "AI service is temporarily unavailable.",

                "suggestion":
                    "Please try again in a few moments."
            }
        )


    except Exception as error:

        print(
            f"Unexpected error: {error}"
        )


        raise HTTPException(

            status_code=500,

            detail={

                "message":
                    "An unexpected error occurred.",

                "suggestion":
                    "Please try again later."
            }
        )


# ============================================================
# EVALUATION ENDPOINT
# ============================================================

@app.get("/evaluation")
def evaluation():

    try:

        metrics = calculate_metrics(
            get_pipeline()
        )


        return {

            "status":
                "success",

            "evaluation":
                metrics
        }


    except Exception as error:

        print(
            f"Evaluation error: {error}"
        )


        raise HTTPException(

            status_code=500,

            detail={

                "message":
                    "Unable to calculate retrieval evaluation.",

                "error":
                    str(error)
            }
        )