# Parte 1: Trabajar con estructuras de datos

# Problema 1: Listas
# Crear una lista de libros favoritos y funciones para gestionarla
favorite_books = ["Cien años de soledad", "1984", "El principito", "Don Quijote de la Mancha", "Harry Potter"]

def print_books():
    """Imprime la lista de libros favoritos."""
    print("Lista de libros favoritos:")
    for book in favorite_books:
        print(f"- {book}")

def add_new_book():
    """Permite al usuario agregar un nuevo libro a la lista."""
    book = input("Ingrese el título de un nuevo libro: ").strip()
    if book:
        favorite_books.append(book)
        print(f"'{book}' ha sido añadido a la lista.")
    else:
        print("No ingresó un título válido.")

# Problema 2: Diccionarios
# Crear un diccionario con información de amigos
friends_info = {
    "Carlos": 25,
    "María": 30,
    "Luis": 27
}

def print_friends():
    """Imprime la información de los amigos almacenados en el diccionario."""
    print("Información de amigos:")
    for name, age in friends_info.items():
        print(f"{name} tiene {age} años.")

def update_age():
    """Permite actualizar la edad de un amigo si su nombre está en la lista."""
    name = input("Ingrese el nombre del amigo para actualizar su edad: ").strip()
    if name in friends_info:
        try:
            new_age = int(input(f"Ingrese la nueva edad de {name}: "))
            friends_info[name] = new_age
            print(f"La edad de {name} ha sido actualizada a {new_age} años.")
        except ValueError:
            print("Por favor, ingrese un número válido.")
    else:
        print("Ese amigo no está en la lista.")

# Problema 3: Tuplas
# Crear una tupla con países para visitar
countries_to_visit = ("Japón", "Italia", "Canadá")

def print_countries():
    """Imprime la lista de países que se desean visitar."""
    print("Países que me gustaría visitar:")
    for country in countries_to_visit:
        print(f"- {country}")

def check_country():
    """Permite al usuario verificar si un país específico está en la lista."""
    country = input("Ingrese el nombre de un país para verificar si está en la lista: ").strip()
    if country in countries_to_visit:
        print(f"Sí, {country} está en la lista.")
    else:
        print(f"No, {country} no está en la lista.")

# Parte 2: Implementación de la Programación Orientada a Objetos

# Clase para una cuenta bancaria
class BankAccount:
    """Representa una cuenta bancaria simple con métodos para depositar, retirar y consultar saldo."""
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        """Añade una cantidad al saldo de la cuenta."""
        if amount > 0:
            self.balance += amount
            print(f"Depósito de ${amount} realizado. Nuevo saldo: ${self.balance}")
        else:
            print("Ingrese una cantidad válida para depositar.")

    def withdraw(self, amount):
        """Retira una cantidad del saldo si hay fondos suficientes."""
        if amount > self.balance:
            print("Fondos insuficientes.")
        elif amount > 0:
            self.balance -= amount
            print(f"Retiro de ${amount} realizado. Nuevo saldo: ${self.balance}")
        else:
            print("Ingrese una cantidad válida para retirar.")

    def get_balance(self):
        """Devuelve el saldo actual de la cuenta."""
        return self.balance

# Demostración de la clase BankAccount
if __name__ == "__main__":
    account = BankAccount("Juan", 1000)
    account.deposit(500)
    account.withdraw(300)
    account.withdraw(1500)  # Intento de retiro con fondos insuficientes
    print(f"Saldo final: ${account.get_balance()}")
