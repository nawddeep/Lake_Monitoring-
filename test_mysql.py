import pymysql

passwords = ['', 'root', 'admin', 'password', '1234', '123456', 'manman', '13022006']
connected = False

for pwd in passwords:
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password=pwd, connect_timeout=2)
        print(f"[SUCCESS] Connected to MySQL as root with password: '{pwd}'")
        with conn.cursor() as cur:
            cur.execute("SHOW DATABASES;")
            dbs = [row[0] for row in cur.fetchall()]
            print("Existing databases:", dbs)
        conn.close()
        connected = True
        break
    except pymysql.MySQLError as e:
        print(f"Trying root / '{pwd}' -> {e}")

if not connected:
    print("[FAIL] Could not connect with common passwords.")
