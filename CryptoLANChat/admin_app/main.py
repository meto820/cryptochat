from admin_app.server import start_server
from admin_app.auth import check_or_create_admin

def main():
    pw = input("🔐 Admin parolası: ")
    if check_or_create_admin(pw):
        print("🟢 Admin doğrulandı")
        start_server()
    else:
        print("❌ Yanlış admin parolası")

if __name__ == "__main__":
    main()
