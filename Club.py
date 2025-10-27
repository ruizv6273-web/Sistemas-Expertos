import random
import os

# --- 1. DEFINICIÓN DE COMPONENTES ---

PERSONAJES = {
    "1": "Profesor Mora",
    "2": "Señorita Escarlata",
    "3": "Coronel Rubio",
    "4": "Doctora Orquídea",
    "5": "Reverendo Verde"
}

ARMAS = {
    "1": "Candelabro",
    "2": "Cuerda",
    "3": "Llave Inglesa",
    "4": "Pistola",
    "5": "Puñal"
}

LOCACIONES = {
    "1": "La Biblioteca",
    "2": "El Salón de Baile",
    "3": "La Cocina",
    "4": "El Conservatorio",
    "5": "El Estudio"
}

# --- 2. DEFINICIÓN DE LAS 5 HISTORIAS ---

HISTORIAS = [
    {
        "titulo": "El crimen de la sabiduría",
        "narrativa": "El Profesor Mora, en un ataque de celos intelectuales, ha acabado con la vida del Sr. Black en la Biblioteca usando un pesado Candelabro.",
        "solucion": ("Profesor Mora", "Candelabro", "La Biblioteca")
    },
    {
        "titulo": "El último baile",
        "narrativa": "Buscando una exclusiva que fue negada, la Señorita Escarlata silenció al Sr. Black con un Puñal durante el baile de gala.",
        "solucion": ("Señorita Escarlata", "Puñal", "El Salón de Baile")
    },
    {
        "titulo": "Un asunto de honor",
        "narrativa": "Un viejo rencor militar llevó al Coronel Rubio a usar su Pistola de servicio en el Estudio del anfitrión.",
        "solucion": ("Coronel Rubio", "Pistola", "El Estudio")
    },
    {
        "titulo": "La trampa natural",
        "narrativa": "La Doctora Orquídea, temiendo ser expuesta, usó una Cuerda para simular un accidente en el frondoso Conservatorio.",
        "solucion": ("Doctora Orquídea", "Cuerda", "El Conservatorio")
    },
    {
        "titulo": "Pecado en la despensa",
        "narrativa": "El Reverendo Verde, descubierto malversando fondos, silenció al Sr. Black con una Llave Inglesa encontrada en la Cocina.",
        "solucion": ("Reverendo Verde", "Llave Inglesa", "La Cocina")
    }
]

class SimuladorClue:

    def __init__(self):
        self.solucion_secreta = {}
        self.narrativa_historia = ""
        self.cartas_computadora = set()
        self.cuaderno = {}
        self.locacion_actual = ""

    def iniciar_juego(self):
        """
        Configura el juego seleccionando una historia y preparando las cartas.
        """
        # 1. Seleccionar la historia
        historia_elegida = random.choice(HISTORIAS)
        solucion_tuple = historia_elegida["solucion"]
        self.solucion_secreta = {
            "personaje": solucion_tuple[0],
            "arma": solucion_tuple[1],
            "locacion": solucion_tuple[2]
        }
        self.narrativa_historia = historia_elegida["narrativa"]

        # 2. Crear todas las cartas y el cuaderno
        todas_las_cartas = set(PERSONAJES.values()) | set(ARMAS.values()) | set(LOCACIONES.values())
        
        # Inicializar cuaderno (todo desconocido)
        for carta in sorted(list(todas_las_cartas)):
            self.cuaderno[carta] = "[ ]" # [ ] = Desconocido, [X] = Descartado

        # 3. Crear la "mano" de la computadora (todas las cartas menos la solución)
        self.cartas_computadora = todas_las_cartas - set(self.solucion_secreta.values())

        # 4. Saludo inicial
        print("=" * 70)
        print("     BIENVENIDO AL SIMULADOR DE MISTERIO 'CLUE'")
        print("=" * 70)
        print("Ha ocurrido un terrible asesinato en la mansión.")
        print("\nLA HISTORIA DE HOY:")
        print(f"-> {self.narrativa_historia}\n")
        print("¡Tu trabajo es descubrir al culpable, el arma y la locación!")
        input("\nPresiona Enter para comenzar tu investigación...")

    def limpiar_consola(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_cuaderno(self):
        """
        Muestra la hoja de deducción del jugador.
        """
        print("\n--- TU CUADERNO DE DEDUCCIÓN ---")
        print("Personajes:")
        for p in PERSONAJES.values():
            print(f"  {self.cuaderno[p]} {p}")
        
        print("\nArmas:")
        for a in ARMAS.values():
            print(f"  {self.cuaderno[a]} {a}")

        print("\nLocaciones:")
        for l in LOCACIONES.values():
            print(f"  {self.cuaderno[l]} {l}")
        print("----------------------------------\n")

    def mostrar_tablero(self):
        """
        Muestra el "tablero" de la consola con las locaciones.
        """
        print("--- TABLERO DE LA MANSIÓN ---")
        print("+-------------------+-------------------+-------------------+")
        print("| (1) La Biblioteca | (2) Salón de Baile| (3) La Cocina     |")
        print("+-------------------+-------------------+-------------------+")
        print("| (4) Conservatorio |      PASILLO      | (5) El Estudio    |")
        print("+-------------------+-------------------+-------------------+")

    def elegir_opcion(self, opciones_dict, prompt):
        """
        Función de ayuda para obtener una entrada válida del usuario.
        """
        print(prompt)
        for key, value in opciones_dict.items():
            print(f"  {key}. {value}")
        
        while True:
            eleccion = input("Tu elección (1-5): ")
            if eleccion in opciones_dict:
                return opciones_dict[eleccion]
            else:
                print("Esa no es una opción válida. Intenta de nuevo.")

    def turno_jugador(self):
        """
        Ejecuta un solo turno del jugador: Mover y Sugerir.
        """
        # 1. Mover (Elegir locación para la sugerencia)
        self.mostrar_tablero()
        self.locacion_actual = self.elegir_opcion(LOCACIONES, "\n¿A qué locación te mueves para investigar?")
        print(f"\nTe has movido a: {self.locacion_actual}")

        # 2. Hacer Sugerencia
        print(f"Estás en {self.locacion_actual}. Debes hacer una sugerencia.")
        sug_personaje = self.elegir_opcion(PERSONAJES, "\n¿Quién sospechas que fue?")
        sug_arma = self.elegir_opcion(ARMAS, "\n¿Con qué arma?")

        print(f"\nTu sugerencia: Fue {sug_personaje} con el {sug_arma} en {self.locacion_actual}.")

        # 3. Computadora procesa la sugerencia
        sugerencia_set = {sug_personaje, sug_arma, self.locacion_actual}
        
        # Encontrar las cartas que la computadora SÍ tiene
        cartas_para_mostrar = self.cartas_computadora.intersection(sugerencia_set)

        if not cartas_para_mostrar:
            print("\n¡ALERTA! Nadie (la computadora) pudo desmentir tu sugerencia...")
            print("(Esto significa que ninguna de esas 3 cartas está en la mano de la computadora)")
        else:
            # La computadora elige aleatoriamente UNA de las cartas que tiene
            carta_mostrada = random.choice(list(cartas_para_mostrar))
            print(f"\nLa computadora te muestra la carta: [{carta_mostrada}]")
            
            # Actualizar el cuaderno del jugador
            self.cuaderno[carta_mostrada] = "[X]"
            print(f"(Has marcado '{carta_mostrada}' como descartada en tu cuaderno)")
        
        input("\nPresiona Enter para continuar...")

    def hacer_acusacion_final(self):
        """
        Permite al jugador hacer una acusación final para ganar o perder.
        """
        print("\n--- ¡ACUSACIÓN FINAL! ---")
        print("Elige con cuidado. Si fallas, el caso se cierra.")
        
        ac_personaje = self.elegir_opcion(PERSONAJES, "\n¿Quién es el CULPABLE?")
        ac_arma = self.elegir_opcion(ARMAS, "\n¿Cuál fue el ARMA?")
        ac_locacion = self.elegir_opcion(LOCACIONES, "\n¿Dónde fue el CRIMEN?")

        print(f"\nTu acusación final es: {ac_personaje} con el {ac_arma} en {ac_locacion}.")

        # Comprobar la solución
        if (ac_personaje == self.solucion_secreta["personaje"] and
            ac_arma == self.solucion_secreta["arma"] and
            ac_locacion == self.solucion_secreta["locacion"]):
            
            print("\n¡FELICIDADES! ¡HAS RESUELTO EL MISTERIO!")
            print(f"Efectivamente, la solución era: {self.solucion_secreta['personaje']}, {self.solucion_secreta['arma']}, {self.solucion_secreta['locacion']}")
            return True # Ganó
        else:
            print("\n¡INCORRECTO! Has acusado a la persona equivocada.")
            print("La verdadera solución era:")
            print(f"  Culpable: {self.solucion_secreta['personaje']}")
            print(f"  Arma:     {self.solucion_secreta['arma']}")
            print(f"  Locación: {self.solucion_secreta['locacion']}")
            return True # Perdió (termina el juego)

    def jugar(self):
        """
        Bucle principal del juego.
        """
        self.limpiar_consola()
        self.iniciar_juego()
        
        juego_terminado = False
        while not juego_terminado:
            self.limpiar_consola()
            self.mostrar_cuaderno()
            self.turno_jugador()
            
            while True:
                accion = input("\n¿Qué deseas hacer ahora?\n  1. Continuar investigando (siguiente turno)\n  2. Hacer una ACUSACIÓN FINAL\nTu elección: ")
                if accion == "1":
                    break # Continúa al siguiente turno
                elif accion == "2":
                    juego_terminado = self.hacer_acusacion_final()
                    break # Termina el juego
                else:
                    print("Opción no válida.")
        
        print("\n--- Fin del Juego ---")

# --- Ejecutar el simulador ---
if __name__ == "__main__":
    juego = SimuladorClue()
    juego.jugar()