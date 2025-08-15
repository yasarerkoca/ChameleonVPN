from app.config.database import engine, Base

# Tüm modeller otomatik olarak import edilmeli. (User, Plan, ProxyIP, ...)

def main():
    print("Tüm tablolar oluşturuluyor...")
    Base.metadata.create_all(bind=engine)
    print("Tablo oluşturma işlemi tamamlandı.")

if __name__ == "__main__":
    main()
