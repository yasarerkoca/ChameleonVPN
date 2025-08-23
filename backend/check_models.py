#cd ~/ChameleonVPN/backend
#python3 check_models.py
# check_models.py

from app.config.database import Base

def check_duplicate_tables():
    tables = {}
    duplicates = []

    for table_name, table in Base.metadata.tables.items():
        if table_name in tables:
            duplicates.append(table_name)
        else:
            tables[table_name] = table

    if duplicates:
        print("🚨 Çift tanımlı tablolar bulundu:")
        for d in duplicates:
            print(f" - {d}")
    else:
        print("✅ Hiçbir tablo çakışması yok.")

if __name__ == "__main__":
    check_duplicate_tables()
