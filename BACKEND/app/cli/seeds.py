from app.core.database import SessionLocal
from app.core.seed import run_all_seeds


def main():
    db = SessionLocal()

    try:
        run_all_seeds(db)
        print("Seeds ejecutados correctamente!")

    finally:
        db.close()


if __name__ == "__main__":
    main()