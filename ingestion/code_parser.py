import ast
from pathlib import Path


def parse_python_file(file_path: str) -> list[dict]:
    """
    Parse a Python file and extract its structural elements:
    classes, functions, and methods.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.suffix.lower() != ".py":
        raise ValueError("Only Python files are supported.")

    source_code = path.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    tree = ast.parse(source_code)

    elements = []

    # Module-level information
    elements.append({
        "type": "module",
        "name": path.name,
        "file_path": str(path),
        "start_line": 1,
        "end_line": len(source_code.splitlines()),
    })

    for node in ast.walk(tree):

        # Function
        if isinstance(node, ast.FunctionDef):

            elements.append({
                "type": "function",
                "name": node.name,
                "file_path": str(path),
                "start_line": node.lineno,
                "end_line": getattr(
                    node,
                    "end_lineno",
                    node.lineno
                ),
            })

        # Async Function
        elif isinstance(node, ast.AsyncFunctionDef):

            elements.append({
                "type": "async_function",
                "name": node.name,
                "file_path": str(path),
                "start_line": node.lineno,
                "end_line": getattr(
                    node,
                    "end_lineno",
                    node.lineno
                ),
            })

        # Class
        elif isinstance(node, ast.ClassDef):

            elements.append({
                "type": "class",
                "name": node.name,
                "file_path": str(path),
                "start_line": node.lineno,
                "end_line": getattr(
                    node,
                    "end_lineno",
                    node.lineno
                ),
            })

    return elements


if __name__ == "__main__":

    print("Python Code Parser")
    print("=" * 50)

    # Test file
    test_file = "data/sample_test.py"

    elements = parse_python_file(test_file)

    for element in elements:
        print(
            f"{element['type']:15} "
            f"{element['name']:20} "
            f"lines {element['start_line']}-{element['end_line']}"
        )

    print("=" * 50)
    print(f"Total elements found: {len(elements)}")