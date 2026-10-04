from llm.llm_client import LLMClient


class RAGAnswerGenerator:

    def __init__(self):
        self.llm = LLMClient()

    def generate(self, question, retrieved_documents):

        context_parts = []

        for doc in retrieved_documents:
            context_parts.append(
                f"""
File: {doc['file_path']}
Lines: {doc['start_line']}-{doc['end_line']}
Element: {doc['element_type']}
Name: {doc['name']}

Code:
{doc['content']}
"""
            )

        context = "\n".join(context_parts)

        prompt = f"""
You are GitContext-AI, an intelligent codebase assistant.

Answer the user's question using ONLY the provided code context.

USER QUESTION:
{question}

CODE CONTEXT:
{context}

INSTRUCTIONS:
1. Explain the answer clearly.
2. Use only information present in the code context.
3. Do not invent code or functionality.
4. Mention the relevant file and line numbers.
5. If the context is insufficient, clearly say that the available code context is insufficient.
6. Keep the answer concise but useful.

ANSWER:
"""

        return self.llm.generate_answer(prompt)


if __name__ == "__main__":

    generator = RAGAnswerGenerator()

    sample_documents = [
        {
            "file_path": "data/sample_test.py",
            "start_line": 3,
            "end_line": 4,
            "element_type": "function",
            "name": "create_user",
            "content": "def create_user(name):\n    return {'name': name}"
        }
    ]

    answer = generator.generate(
        "How does create_user work?",
        sample_documents
    )

    print("\nRAG Answer:")
    print(answer)