import psycopg2
import sys
import time
from psycopg2.extras import RealDictCursor

# Veritabanı değişkenleri
DB_NAME = "dbname"
DB_USER = "postgres"
DB_PASS = ""
DB_HOST = "127.0.0.1"

def cikis():
    print("\nÇıkış yapılıyor...")
    time.sleep(1)
    sys.exit(1)

def getAllUsers():
    # Tüm kullanıcıları listelemeye yarar
    query_builder.execute("SELECT * FROM users")
    users = query_builder.fetchall()
    if(query_builder.rowcount > 0):
        print(f"Toplam {query_builder.rowcount} kayıt bulundu!\n")
        for user in users:
            # user_groups tablosunda dongüdeki üyenin grup id'si ni aratıyoruz
            query_builder.execute("SELECT group_name FROM user_groups WHERE group_id = %s", str(user['user_group']))
            user_group = query_builder.fetchone()['group_name']
            print(f"Üye id: {user['user_id']}")
            print(f"Üye adı: {user['user_name']}")
            print(f"Üye grubu: {user_group}")
            if user != users[-1]:
                print("--------------")
            else:
                print("\n")
    else:
        print("Hiç kullanıcı bulunamadı!\n")

def getAllGroups():
    try:
        query_builder.execute("SELECT * FROM user_groups")
        user_groups = query_builder.fetchall()
        if(query_builder.rowcount > 0):
            print(f"Toplam {query_builder.rowcount} kayıt bulundu!\n")
            for group in user_groups:
                print(f"Grup id: {group['group_id']}")
                print(f"Grup adı: {group['group_name']}\n")
        else:
            print("Hiç kullanıcı grubu bulunamadı!\n")
    except psycopg2.DatabaseError as e:
        print('Bir hata oluştu! %s' % e)    

def getUser():
    try:
        kullanici_id = int(input("Bilgilerini getirmek istediğin kullanıcının idsini gir: "))
        query_builder.execute("SELECT * FROM users WHERE user_id = %s" % kullanici_id)
        if(query_builder.rowcount > 0):
            user = query_builder.fetchone()
            print("--- ÜYE BİLGİLERİ ---")
            print(f"Kullanıcı id: {user['user_id']}")
            print(f"Kullanıcı adı: {user['user_name']}\n")
        else:
            print("Kullanıcı bulunamadı!\n")
    except psycopg2.DatabaseError as e:
        print('Bir hata oluştu! %s' % e)    

def deleteUser():
    user_id = int(input("Silinmesini istediğiniz kullanıcının id'si: "))
    try:
        query_builder.execute("SELECT * FROM users WHERE user_id = %s", [user_id])
        if(query_builder.rowcount > 0):
            user = query_builder.fetchone()
            query_builder.execute("DELETE FROM users WHERE user_id = %s", [user['user_id']])
            print("Kullanıcı başarıyla silindi!\n")
        else:
            print("Silinecek kullanıcı bulunamadı!\n")
    except psycopg2.DatabaseError as e:
        print('Bir hata oluştu! %s' % e)    

def createUser():
    user_name = str(input("Kullanıcı adı: "))
    user_group = str(input("Kullanıcı grubu id: "))
    try:
        query_builder.execute("SELECT * FROM user_groups WHERE group_id = %s" % user_group)
        if(query_builder.rowcount > 0):
            query_builder.execute("INSERT INTO users (user_name, user_group) VALUES(%s, %s)", [user_name, user_group])
            print(f"{user_name} adında yeni bir kullanıcı oluşturuldu.\n")
        else:
            print("Belirilen grup id'e göre kullanıcı grubu bulunamadığından dolayı kullanıcı oluşturulamadı!")
    except psycopg2.DatabaseError as e:
        print('Bir hata oluştu! %s' % e)    

def updateUser():
    kullanici_id = int(input("Düzenlemek istediğin kullanıcının idsini gir: "))
    query_builder.execute("SELECT * FROM users WHERE user_id = %s", [kullanici_id])
    if(query_builder.rowcount > 0):
        kullanici_adi = input("Yeni kullanıcı adı girin: ")
        kullanici_grup = input("Yeni kullanıcı grubu girin: ")
        query_builder.execute("SELECT * FROM user_groups WHERE group_id = %s", [kullanici_grup])
        if(query_builder.rowcount > 0):
            query_builder.execute("""
            UPDATE users
            SET user_name = %s,
            user_group = %s
            """
            , [kullanici_adi, kullanici_grup])
            print("Kullanıcı güncellendi!\n")
        else:
            print("Belirilen grup id'e göre kullanıcı grubu bulunamadığından dolayı kullanıcı düzenlenemedi!\n")
    else:
        print("Kullanıcı bulunamadı!\n")    

def createGroup():
    grup_adi = str(input("Oluşturulacak kullanıcı grubu adı girin: "))
    try:
        query_builder.execute("SELECT * FROM user_groups WHERE group_name = %s", [grup_adi])
        if(query_builder.rowcount > 0):
            print("Bu grup adına sahip bir grup mevcut!\n")
        else:
            query_builder.execute("INSERT INTO user_groups (group_name) VALUES(%s)", [grup_adi])
        print(f"{grup_adi} adında yeni bir kullanıcı grubu oluşturuldu.\n")
    except psycopg2.DatabaseError as e:
        print('Bir hata oluştu! %s' % e)    
        sys.exit(1)

def createUserGroup(group_name):
    try:
        query_builder.execute('INSERT INTO user_groups(group_name) VALUES ("%s");', [str(group_name)])
        print(f"{group_name} adında yeni bir kullanıcı grubu oluşturuldu.")
    except psycopg2.DatabaseError as e:
        print('Bir hata oluştu! %s' % e)    
        sys.exit(1)

while True:
    try:
        # Database bağlantısı
        con = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        query_builder = con.cursor(cursor_factory=RealDictCursor)
        komutlar = {
            "komut_1": {
                "komut_adi": "users",
                "komut_aciklama": "Tüm kullanıcıları listele",
                "fonksiyon": "getAllUsers"
            },
            "komut_2": {
                "komut_adi": "getuser",
                "komut_aciklama": "Girilen ID değerine göre kullanıcı bilgisi getir",
                "fonksiyon": "getUser"
            },
            "komut_3": {
                "komut_adi": "adduser",
                "komut_aciklama": "Yeni bir kullanıcı oluştur",
                "fonksiyon": "createUser"
            },
            "komut_5": {
                "komut_adi": "edituser",
                "komut_aciklama": "Belirtilen id'e göre bulunan kullanıcının bilgilerini düzenle",
                "fonksiyon": "updateUser"
            },
            "komut_6": {
                "komut_adi": "deluser",
                "komut_aciklama": "Belirtilen id'e göre bulunan kullanıcıyı sil",
                "fonksiyon": "deleteUser"
            },
            "komut_7": {
                "komut_adi": "groups",
                "komut_aciklama": "Kullanıcı gruplarını listele",
                "fonksiyon": "getAllGroups"
            },
            "komut_8": {
                "komut_adi": "add_group",
                "komut_aciklama": "Kullanıcı grubu oluştur",
                "fonksiyon": "createGroup"
            },
            "komut_9": {
                "komut_adi": "exit",
                "komut_aciklama": "Programdan çıkış yap",
                "fonksiyon": "cikis"
            },
        }
        print("Kullanılabilecek komutlar: \n")
        for komut in komutlar:
            komut_adi = komutlar[komut].get('komut_adi')
            komut_aciklama = komutlar[komut].get('komut_aciklama')
            komut_fonksiyonu = komutlar[komut].get('fonksiyon')
            komut_fonksiyonu_stripped = komut_fonksiyonu.strip('"') 
            print(f"Komut adı: {komut_adi}\nKomut açıklaması: {komut_aciklama}\n")
        islem = str(input("Çalıştırmak istediğiniz komut: "))

        for komut in komutlar:
            if(islem in komutlar[komut].values()):
                if komutlar[komut].get('fonksiyon') in dir():
                    locals()[komutlar[komut].get('fonksiyon')]()
                else:
                    print(f"{komutlar[komut].get('fonksiyon')} adında bir fonksiyon bulunamadı!\n")
            else:
                continue
            
    # Hata olması durumunda konsola hata mesajı basıyoruz        
    except psycopg2.DatabaseError as e:
        print('Bir hata oluştu! %s' % e)    
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nÇıkış yapılıyor...")
        time.sleep(1)
        sys.exit(1)
    finally:
        if con is not None:
            # Veritabanına kaydet
            con.commit()
            # Sorgu oluşturucuyu kapat
            query_builder.close()
            # Bağlantıyı kapat
            con.close()
