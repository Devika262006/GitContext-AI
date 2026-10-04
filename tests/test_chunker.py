from ingestion.code_chunker import extract_code_chunks


def test_code_chunker(tmp_path):

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


async def fetch_data():
    return "data"
""",
        encoding="utf-8"
    )


    chunks = extract_code_chunks(
        str(test_file)
    )


    assert len(chunks) > 0


    names = [
        chunk["name"]
        for chunk in chunks
    ]


    assert "UserManager" in names
    assert "create_user" in names
    assert "delete_user" in names
    assert "calculate_total" in names
    assert "fetch_data" in names