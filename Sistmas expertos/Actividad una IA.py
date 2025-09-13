#Victor Alberto Ruiz Ruiz

# Parte 1: Trabajar con estructuras de datos

# Problema 1: Listas
favorite_books = []

# Agregamos libros a la lista
favorite_books.append("Cien años de soledad")
favorite_books.append("1984")
favorite_books.append("El principito")
favorite_books.append("Don Quijote de la Mancha")
favorite_books.append("Moby Dick")

def print_books(books):
    """Imprime los libros en la lista."""
    for book in books:
        print(book)

def add_book(books):
    """Permite al usuario agregar un libro a la lista."""
    new_book = input("Ingrese un nuevo libro: ")
    books.append(new_book)

# Problema 2: Diccionarios
friends_info = {
    "Carlos": 25,
    "María": 22,
    "José": 30
}

def print_friends(friends):
    """Imprime la información de los amigos."""
    for name, age in friends.items():
        print(f"{name} tiene {age} años.")

def update_age(friends):
    """Permite actualizar la edad de un amigo."""
    name = input("Ingrese el nombre del amigo: ")
    if name in friends:
        new_age = int(input(f"Ingrese la nueva edad de {name}: "))
        friends[name] = new_age
    else:
        print("Ese amigo no está en la lista.")

# Problema 3: Tuplas
countries_to_visit = ("Japón", "Italia", "Canadá")

def print_countries(countries):
    """Imprime los países en la tupla."""
    for country in countries:
        print(country)

def check_country(countries):
    """Permite al usuario verificar si un país está en la tupla."""
    country = input("Ingrese el país que desea buscar: ")
    if country in countries:
        print(f"{country} está en la lista de países a visitar.")
    else:
        print(f"{country} no está en la lista.")

# Parte 2: Programación Orientada a Objetos
class BankAccount:
    """Clase que representa una cuenta bancaria."""
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        """Agrega dinero a la cuenta."""
        self.balance += amount
        print(f"Depósito de {amount} realizado. Saldo actual: {self.balance}")

    def withdraw(self, amount):
        """Retira dinero de la cuenta, asegurando que el saldo no sea negativo."""
        if amount > self.balance:
            print("Fondos insuficientes.")
        else:
            self.balance -= amount
            print(f"Retiro de {amount} realizado. Saldo actual: {self.balance}")

    def get_balance(self):
        """Devuelve el saldo actual."""
        return self.balance

# Demostración de la clase BankAccount
cuenta = BankAccount("Juan", 1000)
cuenta.deposit(500)
cuenta.withdraw(300)
cuenta.withdraw(1500)  # Intento de retiro mayor al saldo
print(f"Saldo final: {cuenta.get_balance()}")
