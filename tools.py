from db import conn

def create_user(name: str, email: str, created_at: str):
    with conn.cursor() as cur:
        cur.execute(
    """
    INSERT INTO users (name, email, created_at)
    VALUES (%(name)s, %(email)s, NOW())
    RETURNING id, name, email, created_at
    """,
    {
        "name": name,
        "email": email
    }
)

        row = cur.fetchone()
        conn.commit()

    return {
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "created_at": str(row[3])
    }

def get_user_by_id(user_id: int):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, name, email, created_at
            FROM users
            WHERE id = %(id)s
            """,
            {"id": user_id}
        )

        row = cur.fetchone()

    if not row:
        return {"error": "User not found"}

    return {
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "created_at": str(row[3])
    }

def get_users_by_date_range(start_date: str, end_date: str):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, name, email, created_at
            FROM users
            WHERE created_at BETWEEN %(start)s AND %(end)s
            ORDER BY created_at
            """,
            {
                "start": start_date,
                "end": end_date
            }
        )

        rows = cur.fetchall()

    return [
        {
            "id": r[0],
            "name": r[1],
            "email": r[2],
            "created_at": str(r[3])
        }
        for r in rows
    ]

def update_user(user_id: int, name: str = None, email: str = None):
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE users
            SET
                name = COALESCE(%(name)s, name),
                email = COALESCE(%(email)s, email)
            WHERE id = %(user_id)s
            RETURNING id, name, email, created_at
            """,
            {
                "name": name,
                "email": email,
                "user_id": user_id
            }
        )

        row = cur.fetchone()
        conn.commit()

    if not row:
        return {"error": "User not found"}

    return {
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "created_at": row[3]
    }