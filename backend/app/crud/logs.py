from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.logs.anomaly_fraud_record import AnomalyFraudRecord

class LogCRUD:
    def create(self, db: Session, data: Dict[str, Any]) -> AnomalyFraudRecord:
        obj = AnomalyFraudRecord(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def list(self, db: Session, limit: int = 100, offset: int = 0) -> List[AnomalyFraudRecord]:
        stmt = select(AnomalyFraudRecord).offset(offset).limit(limit)
        return list(db.execute(stmt).scalars())

    def get(self, db: Session, _id: int) -> Optional[AnomalyFraudRecord]:
        return db.get(AnomalyFraudRecord, _id)

log_crud = LogCRUD()
