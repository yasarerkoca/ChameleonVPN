# -*- coding: utf-8 -*-
"""
Pydantic uyum katmanı:
- V2: model_config = ConfigDict(from_attributes=True)
- V1: class Config: from_attributes = True

Kullanım:
    from app.schemas._base import ORMSchema
    class MySchema(ORMSchema):
        id: int
        name: str
"""
from pydantic import BaseModel

try:
    # Pydantic v2
    from pydantic import ConfigDict  # type: ignore

    class ORMSchema(BaseModel):
        # SQLAlchemy objelerinden alan okumayı açar (v2 karşılığı)
        model_config = ConfigDict(from_attributes=True)

except ImportError:
    # Pydantic v1 geriye uyumluluk
    class ORMSchema(BaseModel):
        class Config:
            # v1 karşılığı
            from_attributes = True


__all__ = ["ORMSchema"]
