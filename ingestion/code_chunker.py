import ast
from pathlib import Path


def extract_code_chunks(file_path: str) -> list[dict]:
    """
    Convert a Python source file into structure-aware chunks.
    Each chunk contains source code and useful metadata.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    source_code = path.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    lines = source_code.splitlines()
    tree = ast.parse(source_code)

    chunks = []

    for node in tree.body:

        # -------------------------
        # Class
        # -------------------------
        if isinstance(node, ast.ClassDef):

            class_start = node.lineno
            class_end = getattr(
                node,
                "end_lineno",
                node.lineno
            )

            class_code = "\n".join(
                lines[class_start - 1:class_end]
            )

            chunks.append({
                "type": "class",
                "name": node.name,
                "parent": None,
                "file_path": str(path),
                "start_line": class_start,
                "end_line": class_end,
                "code": class_code,
            })

            # Extract methods inside the class
            for child in node.body:

                if isinstance(
                    child,
                    (ast.FunctionDef, ast.AsyncFunctionDef)
                ):

                    method_start = child.lineno
                    method_end = getattr(
                        child,
                        "end_lineno",
                        child.lineno
                    )

                    method_code = "\n".join(
                        lines[method_start - 1:method_end]
                    )

                    method_type = (
                        "async_method"
                        if isinstance(
                            child,
                            ast.AsyncFunctionDef
                        )
                        else "method"
                    )

                    chunks.append({
                        "type": method_type,
                        "name": child.name,
                        "parent": node.name,
                        "file_path": str(path),
                        "start_line": method_start,
                        "end_line": method_end,
                        "code": method_code,
                    })

        # -------------------------
        # Function
        # -------------------------
        elif isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef)
        ):

            function_start = node.lineno
            function_end = getattr(
                node,
                "end_lineno",
                node.lineno
            )

            function_code = "\n".join(
                lines[function_start - 1:function_end]
            )

            function_type = (
                "async_function"
                if isinstance(
                    node,
                    ast.AsyncFunctionDef
                )
                else "function"
            )

            chunks.append({
                "type": function_type,
                "name": node.name,
                "parent": None,
                "file_path": str(path),
                "start_line": function_start,
                "end_line": function_end,
                "code": function_code,
            })

    return chunks


if __name__ == "__main__":

    test_file = "data/sample_test.py"

    chunks = extract_code_chunks(test_file)

    print("\nStructure-Aware Code Chunks")
    print("=" * 70)

    for index, chunk in enumerate(chunks, start=1):

        print(f"\nCHUNK {index}")
        print("-" * 70)

        print(f"Type       : {chunk['type']}")
        print(f"Name       : {chunk['name']}")
        print(f"Parent     : {chunk['parent']}")
        print(f"File       : {chunk['file_path']}")
        print(
            f"Lines      : "
            f"{chunk['start_line']}-{chunk['end_line']}"
        )

        print("\nCode:")
        print(chunk["code"])

    print("\n" + "=" * 70)
    print(f"Total chunks: {len(chunks)}")