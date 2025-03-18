def user_schema(user) -> dict:

    return {"id": str(user["_id"]),"nombre": user["nombre"],"codigo": user["codigo"], "estado": user["estado"]}

def users_all_schemas(users) -> list:
    return [user_schema(user) for user in users]