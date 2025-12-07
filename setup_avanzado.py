import sqlite3
import os

def crear_base_avanzada():
    db_name = 'taller_pro.db'
    
    if os.path.exists(db_name):
        os.remove(db_name)

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fallas (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            sistema TEXT,
            solucion TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reglas (
            falla_id INTEGER,
            sintoma TEXT,
            peso INTEGER,
            FOREIGN KEY(falla_id) REFERENCES fallas(id)
        )
    ''')

    fallas = [
        (1, "Batería Muerta", "Electrico", "Reemplazar batería o intentar cargarla con pinzas."),
        (2, "Alternador Dañado", "Electrico", "El alternador no carga. Se requiere reemplazo inmediato."),
        (3, "Fusible Quemado", "Electrico", "Localizar fusible fundido en la caja y reemplazar."),
        (4, "Balatas Cristalizadas", "Frenos", "Lijar balatas o cambiarlas si están muy delgadas."),
        (5, "Fuga de Líquido de Frenos", "Frenos", "PELIGRO: Reparar fuga en mangueras y purgar sistema."),
        (6, "Discos Deformados", "Frenos", "Rectificar discos o cambiarlos (causa vibración)."),
        (7, "Junta de Culata Dañada", "Motor", "Reparación mayor requerida. No usar el auto."),
        (8, "Falta de Aceite", "Motor", "Rellenar nivel de aceite y monitorear fugas."),
        (9, "Bujías en mal estado", "Motor", "Realizar afinación y cambio de bujías.")
    ]
    cursor.executemany("INSERT INTO fallas VALUES (?,?,?,?)", fallas)

    reglas = [
        (1, "No enciende nada (tablero apagado)", 5), 
        (1, "Sonido 'clic' repetitivo al girar llave", 4),
        (2, "Auto se apaga en movimiento", 5), 
        (2, "Luces suben y bajan intensidad al acelerar", 4), 
        (2, "Testigo de batería encendido en tablero", 5),
        (3, "Un solo componente eléctrico no funciona (ej. radio)", 5),
        (4, "Chirrido agudo al frenar", 5), 
        (4, "Distancia de frenado aumenta", 3),
        (5, "Pedal de freno se va al fondo suavemente", 5), 
        (5, "Mancha de líquido aceitoso cerca de las ruedas", 5),
        (5, "Testigo de frenos encendido", 4),
        (6, "Vibración en el volante al frenar", 5),
        (7, "Humo blanco denso constante por escape", 5), 
        (7, "Aceite color 'café con leche'", 5), 
        (7, "Consumo excesivo de agua/refrigerante", 4),
        (7, "Motor se sobrecalienta rápido", 4),
        (8, "Testigo de aceite encendido", 5), 
        (8, "Ruido de golpeteo metálico (taca-taca)", 4),
        (9, "Motor tiembla en semáforos", 4),
        (9, "Dificultad para acelerar (jaloneos)", 4)
    ]
    cursor.executemany("INSERT INTO reglas VALUES (?,?,?)", reglas)

    conn.commit()
    conn.close()
    print(f"Base de datos {db_name} generada correctamente.")

if __name__ == "__main__":
    crear_base_avanzada()
