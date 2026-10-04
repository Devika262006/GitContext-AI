class UserManager:

    def create_user(self, name):
        return {"name": name}

    def delete_user(self, user_id):
        return f"Deleted {user_id}"


def calculate_total(price, quantity):
    return price * quantity


async def fetch_data():
    return "data"