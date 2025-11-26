from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

def main(argv=None):
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE users (x int, y int)"))
        conn.execute(
            text("INSERT INTO users (x, y) VALUES (:x, :y)"),
            [{"x": 1, "y": 1}, {"x": 2, "y": 4}]
        )
        conn.commit()

    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO users (x, y) VALUES (:x, :y)"),
            [{"x": 6, "y": 8}, {"x": 9, "y": 10}]
        )

    with engine.connect() as conn:
        result = conn.execute(text("SELECT x, y FROM users"))
        for row in result:
            print(f"x: {row.x}, y: {row.y}")

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT x, y FROM users WHERE y > :y AND x > :x"), 
            {"y": 2, "x": 4}
        )
        for row in result:
            print(f"x: {row.x}  y: {row.y}")

    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO users (x, y) VALUES (:x, :y)"),
            [{"x": 11, "y": 12}, {"x": 13, "y": 14}],
        )
        conn.commit()

    stmt = text("SELECT x, y FROM users WHERE y > :y AND x > :x ORDER BY x, y")
    with Session(engine) as session:
        result = session.execute(stmt, {"y": 6, "x": 1})
        for row in result:
            print(f"x: {row.x}  y: {row.y}")

    with Session(engine) as session:
        result = session.execute(
            text("UPDATE users SET y=:y WHERE x=:x"),
            [{"x": 9, "y": 11}, {"x": 13, "y": 15}],
        )
        session.commit()


if __name__ == "__main__":
    main()