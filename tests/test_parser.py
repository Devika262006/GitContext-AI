from ingestion.code_parser import parse_python_file


def test_python_parser(tmp_path):

    test_file = tmp_path / "test_sample.py"

    test_file.write_text(
        """
class UserManager:

    def create_user(self, name):
        return {"name": name}

    def delete_user(self, user_id):
        return f"Deleted {user_id}"


def calculate_total(a, b):
    return a + b
""",
        encoding="utf-8"
    )


    elements = parse_python_file(
        str(test_file)
    )


    assert len(elements) > 0


    names = [
        element["name"]
        for element in elements
    ]


    assert "UserManager" in names
    assert "create_user" in names
    assert "delete_user" in names
    assert "calculate_total" in names