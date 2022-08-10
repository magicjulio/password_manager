from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self):
        self.key = None
        self.password_file = None
        self.dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        print(self.key)

        with open(path, "wb") as f:
            f.write(self.key)


    def load_key(self, path):
        with open(path, "rb") as f:
            self.key = f.read()


    def create_password_file(self, path, init_values=None):
        self.password_file = path
        if init_values is not None:
            for key,val in init_values.items():
                self.add_psw(key, val)


    def load_password_file(self, path):
        self.password_file = path
        with open(path, "r") as f:
            for line in f:
                site, encrypted = line.split(":")
                self.dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()


    def add_psw(self, site, psw):
        self.dict[site] = psw
        if self.password_file is not None:
            with open(self.password_file, "a+") as f:
                encry = Fernet(self.key).encrypt(psw.encode())
                f.write(site + ":" + encry.decode() + "\n")

    def get_password(self, site):
        return self.dict[site]


def main():
    password = {
        "example": "password",
        "username": "abc123",
    }
    pm = PasswordManager()
    print("""
    What do you want to do?
    (1) Creat key
    (2) Load key
    (3) create new password file
    (4) Load exsisting passwordfile
    (5) Add password
    (6) Get a password
    (q) Quit
    """)

    done = False
    while not done:
        choice = input("Enter a choice: ")
        if choice == "1":
            path = input("Enter path: ")
            pm.create_key(path)
        elif choice == "2":
            path = input("Enter path: ")
            pm.load_key(path)


        elif choice == "3":
            path = input("Enter path: ")
            pm.create_password_file(path, password)

        elif choice == "4":
            path = input("Enter path: ")
            pm.load_password_file(path)

        elif choice == "5":
            site = input("Enter site")
            psw = input("Enter password: ")
            pm.add_psw(site, psw)
        elif choice == "6":
            site = input("Enter site: ")
            print(f"Password for {site} is {pm.get_password(site)}")
        elif choice == "q":
            print("Bye")
            done = True

        else:
            print("invalid choice!")

if __name__ == "__main__":
    main()

