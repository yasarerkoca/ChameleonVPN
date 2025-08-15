import pytest
import time
from app.config.database import SessionLocal
from app.models.user.user import User
from app.models.corporate.corporate_user_group import CorporateUserGroup
from sqlalchemy.exc import IntegrityError

@pytest.mark.asyncio
async def test_crud_user():
    db = SessionLocal()
    unique_email = f"testuser_{int(time.time())}@example.com"
    try:
        # Önce test için grup ekle
        group = CorporateUserGroup(name=f"TestGroup_{int(time.time())}")
        db.add(group)
        db.commit()
        db.refresh(group)

        # Önce sil (varsa)
        user = db.query(User).filter_by(email=unique_email).first()
        if user:
            db.delete(user)
            db.commit()

        # CREATE
        new_user = User(
            email=unique_email,
            password_hash="Aa1!aa1!bb2@BB2@",
            is_active=True,
            full_name="Test User",
            corporate_group_id=group.id,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        assert new_user.id is not None

        # READ
        user = db.query(User).filter_by(email=unique_email).first()
        assert user is not None

        # UPDATE
        user.is_active = False
        db.commit()
        db.refresh(user)
        assert user.is_active is False

        # DELETE
        db.delete(user)
        db.commit()
        user = db.query(User).filter_by(email=unique_email).first()
        assert user is None

        # Grubu da sil
        db.delete(group)
        db.commit()

    except IntegrityError as e:
        db.rollback()
        assert False, f"IntegrityError: {e}"
    finally:
        db.close()
