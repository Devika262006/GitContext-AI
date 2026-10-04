import os
import time

from dotenv import load_dotenv
from google import genai


load_dotenv()


class LLMClient:

    def __init__(self):

        self.api_key = os.getenv("GEMINI_API_KEY")

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.5-flash-lite"
        )

        self.max_retries = 3

        self.retry_delay = 2


        if not self.api_key:

            raise ValueError(
                "GEMINI_API_KEY is not set. "
                "Please add it to the .env file."
            )


        self.client = genai.Client(
            api_key=self.api_key
        )


    def generate_answer(
        self,
        prompt: str
    ) -> str:

        if not prompt.strip():

            raise ValueError(
                "Prompt cannot be empty."
            )


        last_error = None


        for attempt in range(
            1,
            self.max_retries + 1
        ):

            try:

                print(
                    f"\nGemini request "
                    f"attempt {attempt}/"
                    f"{self.max_retries}"
                )


                response = (
                    self.client.models.generate_content(
                        model=self.model,
                        contents=prompt
                    )
                )


                if not response.text:

                    raise ValueError(
                        "Gemini returned an empty response."
                    )


                print(
                    "Gemini response generated successfully!"
                )


                return response.text


            except Exception as error:

                last_error = error


                print(
                    f"Gemini request failed "
                    f"on attempt {attempt}:"
                )

                print(error)


                if attempt < self.max_retries:

                    wait_time = (
                        self.retry_delay * attempt
                    )


                    print(
                        f"Retrying in "
                        f"{wait_time} seconds..."
                    )


                    time.sleep(wait_time)


                else:

                    print(
                        "Maximum Gemini retries reached."
                    )


        raise RuntimeError(
            "Gemini service is temporarily "
            "unavailable after multiple retries."
        ) from last_error


# =========================================================
# DIRECT TEST
# =========================================================

if __name__ == "__main__":

    llm = LLMClient()


    answer = llm.generate_answer(
        "Explain what a Python function is "
        "in one simple sentence."
    )


    print("\n")
    print("=" * 70)
    print("LLM RESPONSE")
    print("=" * 70)

    print(answer)

    print("=" * 70)