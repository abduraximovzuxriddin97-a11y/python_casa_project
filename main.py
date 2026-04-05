"""////////////////////////////  KASSA DASTURI  ////////////////////////////"""



import sqlite3



# Databasega yaratish
connect = sqlite3.connect("kassa.db")
cursor = connect.cursor()


ism = input("ismingizni kiriting: ").capitalize()

def register(name: str):
    print( f"""---Salom {name}---
---Kassa dasturiga xush kelibsiz!---
""")


    while True:
        register_input = input("---tizimga kirish---\n\n1. Login\n2. Exit\nTanlang: ")
        if register_input == "1":
            cursor.execute("""
SELECT * FROM login_and_password WHERE id = ?
""", (1,))
            data_col = cursor.fetchall()

            cursor.execute("""
SELECT * FROM login_and_password WHERE id = ?
""", (2,))
            data_row = cursor.fetchall()

            login = ""
            parol = ""

            for i in data_col:
                login = i[1]
            
            for i in data_row:
                parol = i[1]
            
            login_input = input("login kirit: ")
            parol_input = input("parol kirit: ")

            if login_input == login and parol_input == parol:
                main_menu()
            else:
                print("Qayta urining")


        elif register_input == "2":
            print("Dasturdan to'xtadi...")
            break
        else:
            print("Qayta urining")
    

text = """
1. Savdo
2. Mahsulot o'chirish
3. Mahsulotlar
4. Mahsulot qo'shish
5. Mahsulotni yangilash
6. Parolni yangilash
0. Chiqish(Hamma bo'limda 0 ni tanlab menuga qaytish mumkin)
"""

def main_menu():
    while True:
        print(text)
        try:
            main_input = int(input("Tanlang (1/2/3): "))

            if main_input == 1:
                savdo()
                break
            elif main_input == 2:
                delete()
                break
            elif main_input == 3:
                mahsulotlar_func()
                break
            elif main_input == 4:
                mahsulot_qoshish()
                break
            elif main_input == 5:
                mahsulot_yangilash()
                break
            elif main_input == 6:
                login_password_change()
                break
            elif main_input == 0:
                break
            else:
                print("Noto'g'ri menu tanlandi, qayta urining")
        except:
            print("Iltimos bo'limlarni raqamda tanlang")


# ------------------------------  Savdo bo'limi  ------------------------------
def savdo():
    print("\n---Savdo bo'limi---\n")

    ortga()


# ------------------------------  Mahsulotlar o'chirish  ------------------------------
def delete():
    print("\n---Mahsulot o'chirish bo'limi---\n")

    while True:
        try:
            kod = int(input("O'chirmoqchi bo'lgan mahsulotingizning kodini kiriting: "))


            cursor.execute("""
    SELECT * FROM mahsulotlar WHERE mahsulot_kodi = ?
    """, (kod,))

            mahsulot = cursor.fetchall()

            if mahsulot:
                cursor.execute("""
    SELECT * FROM mahsulotlar WHERE mahsulot_kodi = ?
    """, (kod,))
                remove = cursor.fetchall()
                print(remove)
                while True:
                    ha_yoq = input("Haqiqatdan ham shu mahsulotni o'chirmoqchimisiz(ha/yo'q): ").lower()

                    if ha_yoq == "ha":
                        cursor.execute("""
        DELETE FROM mahsulotlar WHERE mahsulot_kodi = ?
        """, (kod,))

                        connect.commit()
                        print("Mahsulot o'chirildi")
                        ortga()
                    elif ha_yoq == "yo'q" or ha_yoq == "yoq":
                        print("Mahsulot o'chirilmadi")
                        ortga()
                    else:
                        print("Kechirasiz faqat ha yoki yo'q deb javob bering")
                    
            elif kod == 0:
                main_menu()
                break
            else:
                print("Bunday kodli mahsulot mavjud emas.\nQayta urining.")
        except:
            print("Iltimos kodni raqamlarda kiriting")


# ------------------------------  Mahsulotlar bo'limi  ------------------------------
def mahsulotlar_func():
    print("\n---Mahsulotlar bo'limi---\n")

    cursor.execute("""
SELECT * FROM mahsulotlar
""")
    
    data = cursor.fetchall()
    connect.commit()

    product = ""
    product_price = ""

    for i in data:
        product = i[1]
        product_price = i[2]

    
        print(f"{product} | {product_price}")

    ortga()


# ------------------------------  Mahsulot qo'shish bo'limi  ------------------------------
def mahsulot_qoshish():
    print("\n---Mahsulot qo'shish bo'limi---\n")

    while True:
        try:
            kod = int(input("Ushbu mahsulot uchun kod kiriting: "))

            cursor.execute("""
    SELECT * FROM mahsulotlar WHERE mahsulot_kodi = ?
    """, (kod,))

            mahsulot = cursor.fetchall()

            if not mahsulot:
                yangi_mahsulot_nomi = input("Mahsulot nomini kiriting: ").capitalize()
                yangi_mahsulot_narxi = int(input("Mahsulot narxini kiriting: "))

                cursor.execute("""
        INSERT INTO mahsulotlar (mahsulot_kodi, mahsulot_nomi, mahsulot_narxi)
                        VALUES (?, ?, ?)
        """, (kod, yangi_mahsulot_nomi, yangi_mahsulot_narxi))

                connect.commit()
                print("Mahsulot qo'shildi")
                ortga()
            elif kod == 0:
                main_menu()
                break
            elif mahsulot:
                print("Kechirasiz ushbu kodda ichida mahsulot mavjud\nQayta urining")
            else:
                print("Ushbu raqam mahsulot uchun kod bo'la olmaydi")
        except:
            print("Iltimos kodni raqamlarda kiriting")


# ------------------------------  Mahsulot yangilash bo'limi  ------------------------------
def mahsulot_yangilash():
    print("\n---Mahsulot qo'shish bo'limi---\n")

    while True:
        try:
            product_refresh = int(input("Yangilamoqchi bo'lgan mahsulotingizning kodini kiriting: "))

            cursor.execute("""
SELECT * FROM mahsulotlar WHERE mahsulot_kodi = ?
""", (product_refresh,))
            
            products = cursor.fetchall()

            if products:
                cursor.execute("""
SELECT * FROM mahsulotlar WHERE mahsulot_kodi = ?
""", (product_refresh,))
                
                product = cursor.fetchall()

                product_text = """
1. Mahsulot narxini o'zgartirish
"""
                print(product[0])

                while True:
                    try:
                        choose_price = int(input(f"{product_text}\nTanlang: "))

                        if choose_price == 1:
                            new_price = int(input("Yangi narxni kiriting: "))

                            cursor.execute("""
        UPDATE mahsulotlar SET mahsulot_narxi = ? WHERE mahsulot_kodi = ?
        """, (new_price, product_refresh))
                        
                            connect.commit()

                            print("Mahsulot yangilandi")

                            ortga()
                        else:
                            print("Qayta urining")
                    except:
                        print("Iltimos raqamlarda kiriting")
                    
            elif product_refresh == 0:
                main_menu()
                break
            else:
                print("Bunday kodli mahsulot mavjud emas")
        except:
            print("Iltimos kodni raqamlarda kiriting")


# ------------------------------  Parolni o'zgartirish  ------------------------------
def login_password_change():
    print("\n---Parolni o'zgartirish bo'limi---\n")

    while True:
        parol_input = input("Joriy parolni kirit: ")

        cursor.execute("""
SELECT * FROM login_and_password WHERE id = ?
""", (2,))
        data = cursor.fetchall()
        parol = ""
            
        for i in data:
            parol = i[1]
        

        if parol_input == parol:
            new_password = input("Yangi parolni kiriting: ")

            cursor.execute("""
DELETE FROM login_and_password WHERE id = ?
""", (2,))
            cursor.execute("""
INSERT INTO login_and_password (id, log_pass)
                           VALUES (?, ?)
""", (2, new_password))
            
            connect.commit()
            print("Yangi parol muvaffaqiyatli o'rnatildi")
            ortga()
        elif parol_input == "0":
            main_menu()
            break
        else:
            print("Parol noto'g'ri")


# ------------------------------  Ortga  ------------------------------
def ortga():
    while True:
        mahsulot = input("\n1. Ortga qaytish\n\nTanlang: ")
        if mahsulot == "1":
            main_menu()
            break
        else:
            print("Qayta urining")



connect.commit()

if __name__ == "__main__":
    register(ism)

connect.close()
