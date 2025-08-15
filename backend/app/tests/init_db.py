from app.config.database import SessionLocal
from app.models.user.user import User  # Doğru import yolu
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_test_user():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "yasarerkoca@gmail.com").first()
        if not user:
            password_hash = pwd_context.hash("Aa1!aa1!bb2@BB2@")
            new_user = User(
                email="testuser@example.com",
                password_hash=password_hash,  # DİKKAT: doğru alan!
                full_name="Test User",
                is_active=True
            )
            db.add(new_user)
            db.commit()
            print("Test kullanıcı oluşturuldu.")
        else:
            print("Test kullanıcı zaten var.")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()
