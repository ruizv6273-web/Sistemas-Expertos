import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

class SistemaExpertoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Experto Mecánico v2.0")
        self.root.geometry("650x550")
        self.root.configure(bg="#f0f2f5")
        
        try:
            self.conn = sqlite3.connect('taller_pro.db')
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se encontró la base de datos.\nEjecute primero 'setup_avanzado.py'.\nError: {e}")
            root.destroy()
            return
        
        self.crear_pantalla_inicio()

    def crear_pantalla_inicio(self):
        self.limpiar_ventana()
        
        tk.Label(self.root, text="Diagnóstico Automotriz Inteligente", 
                 font=("Helvetica", 20, "bold"), bg="#f0f2f5", fg="#2c3e50").pack(pady=30)
        
        tk.Label(self.root, text="¿En qué sistema del vehículo percibe la falla?", 
                 font=("Helvetica", 12), bg="#f0f2f5").pack(pady=10)

        frame_botones = tk.Frame(self.root, bg="#f0f2f5")
        frame_botones.pack(pady=20)

        estilos_botones = [
            ("MOTOR", "#e74c3c"),
            ("FRENOS", "#e67e22"),
            ("ELECTRICO", "#f1c40f")
        ]

        for texto, color in estilos_botones:
            btn = tk.Button(frame_botones, text=texto, font=("Helvetica", 12, "bold"),
                            width=15, height=3, bg=color, fg="white", bd=0, cursor="hand2",
                            command=lambda s=texto.capitalize(): self.cargar_sintomas(s))
            btn.pack(side=tk.LEFT, padx=15)

        tk.Label(self.root, text="Sistema Experto - Proyecto Escolar", 
                 font=("Arial", 9, "italic"), bg="#f0f2f5", fg="gray").pack(side=tk.BOTTOM, pady=10)

    def cargar_sintomas(self, sistema_seleccionado):
        self.limpiar_ventana()
        self.sistema_actual = sistema_seleccionado
        
        tk.Label(self.root, text=f"Evaluando: Sistema {sistema_seleccionado}", 
                 font=("Helvetica", 16, "bold"), bg="#f0f2f5", fg="#34495e").pack(pady=15)
        
        tk.Label(self.root, text="Marque las casillas de los síntomas presentes:", 
                 font=("Arial", 11), bg="#f0f2f5").pack()

        query = """
            SELECT DISTINCT r.sintoma 
            FROM reglas r
            JOIN fallas f ON r.falla_id = f.id
            WHERE f.sistema = ?
        """
        self.cursor.execute(query, (sistema_seleccionado,))
        sintomas_db = self.cursor.fetchall()

        frame_container = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        frame_container.pack(pady=10, padx=50, fill="both", expand=True)

        canvas = tk.Canvas(frame_container, bg="white")
        scrollbar = ttk.Scrollbar(frame_container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="white")

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.check_vars = []
        self.sintomas_texto = []

        for sintoma in sintomas_db:
            var = tk.IntVar()
            texto = sintoma[0]
            chk = tk.Checkbutton(self.scrollable_frame, text=texto, variable=var, 
                                 font=("Arial", 11), bg="white", activebackground="white", anchor="w")
            chk.pack(fill="x", padx=10, pady=5)
            self.check_vars.append(var)
            self.sintomas_texto.append(texto)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        frame_acciones = tk.Frame(self.root, bg="#f0f2f5")
        frame_acciones.pack(pady=15)

        tk.Button(frame_acciones, text="Cancelar / Volver", command=self.crear_pantalla_inicio, 
                  bg="#95a5a6", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        
        tk.Button(frame_acciones, text="DIAGNOSTICAR", command=self.motor_inferencia, 
                  bg="#2ecc71", fg="white", font=("Arial", 12, "bold"), width=20).pack(side=tk.LEFT, padx=10)

    def motor_inferencia(self):
        sintomas_detectados = []
        for i, var in enumerate(self.check_vars):
            if var.get() == 1:
                sintomas_detectados.append(self.sintomas_texto[i])
        
        if not sintomas_detectados:
            messagebox.showwarning("Falta información", "Por favor seleccione al menos un síntoma.")
            return

        placeholders = ','.join(['?'] * len(sintomas_detectados))
        query = f"""
            SELECT f.nombre, f.solucion, SUM(r.peso) as certeza
            FROM fallas f
            JOIN reglas r ON f.id = r.falla_id
            WHERE r.sintoma IN ({placeholders}) AND f.sistema = ?
            GROUP BY f.nombre
            ORDER BY certeza DESC
        """
        
        params = sintomas_detectados + [self.sistema_actual]
        self.cursor.execute(query, params)
        resultados = self.cursor.fetchall()

        self.mostrar_resultados(resultados)

    def mostrar_resultados(self, resultados):
        self.limpiar_ventana()
        
        tk.Label(self.root, text="Resultados del Análisis", 
                 font=("Helvetica", 18, "bold"), bg="#f0f2f5", fg="#2c3e50").pack(pady=15)

        if resultados:
            mejor_diagnostico = resultados[0]
            
            card = tk.Frame(self.root, bg="white", bd=1, relief="solid")
            card.pack(padx=30, pady=10, fill="x")
            
            tk.Label(card, text="Falla Detectada:", font=("Arial", 10), bg="white", fg="gray").pack(pady=(10,0))
            tk.Label(card, text=mejor_diagnostico[0], font=("Helvetica", 16, "bold"), bg="white", fg="#c0392b").pack(pady=5)
            
            tk.Label(card, text="Recomendación:", font=("Arial", 10, "bold"), bg="white").pack(pady=(10,0))
            tk.Label(card, text=mejor_diagnostico[1], font=("Arial", 11), bg="white", wraplength=500, justify="center").pack(pady=5)
            
            tk.Label(card, text=f"Certeza: {mejor_diagnostico[2]} puntos", font=("Arial", 9, "bold"), bg="#ecf0f1", width=50).pack(pady=(10,0), fill="x")

            if len(resultados) > 1:
                tk.Label(self.root, text="Otras posibilidades menores:", bg="#f0f2f5", font=("Arial", 10, "bold")).pack(pady=(15,5))
                for res in resultados[1:3]:
                    tk.Label(self.root, text=f"• {res[0]} (Certeza: {res[2]})", bg="#f0f2f5").pack()

        else:
            tk.Label(self.root, text="No se encontró una coincidencia exacta.", font=("Arial", 14), bg="#f0f2f5", fg="red").pack(pady=20)
            tk.Label(self.root, text="Intente seleccionar más síntomas o consulte a un mecánico.", bg="#f0f2f5").pack()

        tk.Button(self.root, text="Volver al Inicio", command=self.crear_pantalla_inicio, 
                  bg="#3498db", fg="white", font=("Arial", 11)).pack(pady=30)

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaExpertoGUI(root)
    root.mainloop()