import csv
from typing import List, Tuple
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, messagebox


Point = Tuple[float, float]

def leer_puntos_csv(ruta_csv: str) -> List[Point]:
    """Lee un CSV con encabezados x,y y regresa una lista de tuplas (x,y)."""
    puntos: List[Point] = []
    with open(ruta_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            x = float(row["x"])
            y = float(row["y"])
            puntos.append((x, y))
    return puntos


def punto_mas_izquierdo(puntos: List[Point]) -> int:
    """
    Regresa el índice del punto más a la izquierda.
    En empate de x, escoger el de menor y (para hacerlo determinista).
    """
    idx = 0
    for i in range(1, len(puntos)):
        if (puntos[i][0] < puntos[idx][0] or
           (puntos[i][0] == puntos[idx][0] and puntos[i][1] < puntos[idx][1])):
            idx = i
    return idx


def orientacion(a: Point, b: Point, c: Point) -> float:
    """
    Regresa el valor del producto cruz (cross product).

    - > 0  : giro antihorario (CCW)
    - < 0  : giro horario (CW)
    - == 0 : colineales
    """
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def distancia2(a: Point, b: Point) -> float:
    """Distancia al cuadrado (evita usar sqrt)."""
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy


def convex_hull(puntos: List[Point]) -> List[Point]:
    """
    Implementación del algoritmo Jarvis March (Gift Wrapping).
    """
    if len(puntos) < 3:
        return puntos[:]  # no hay polígono

    hull: List[Point] = []
    start_idx = punto_mas_izquierdo(puntos)
    p_idx = start_idx

    while True:
        hull.append(puntos[p_idx])
        q_idx = (p_idx + 1) % len(puntos)

        for r_idx in range(len(puntos)):
            if r_idx == p_idx:
                continue

            o = orientacion(puntos[p_idx], puntos[q_idx], puntos[r_idx])

            # Si r es más antihorario que q
            if o > 0:
                q_idx = r_idx

            # Si son colineales, elegir el más lejano
            elif o == 0:
                if distancia2(puntos[p_idx], puntos[r_idx]) > distancia2(puntos[p_idx], puntos[q_idx]):
                    q_idx = r_idx

        p_idx = q_idx

        if p_idx == start_idx:
            break

    return hull


def dibujar(puntos: List[Point], hull: List[Point], titulo: str = "Convex Hull"):
    """Dibuja puntos y el polígono del hull."""
    xs = [p[0] for p in puntos]
    ys = [p[1] for p in puntos]

    plt.figure()
    plt.scatter(xs, ys)

    if len(hull) >= 2:
        hx = [p[0] for p in hull] + [hull[0][0]]
        hy = [p[1] for p in hull] + [hull[0][1]]
        plt.plot(hx, hy)

    plt.title(titulo)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.tight_layout()
    plt.show()

def seleccionar_archivo():
    ruta = filedialog.askopenfilename(
        title="Seleccionar archivo CSV",
        filetypes=[("Archivos CSV", "*.csv")]
    )

    if ruta:
        try:
            main(ruta)
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo procesar el archivo:\n{e}"
            )


def main(ruta):
    # Cambia la ruta si es necesario
    ruta = "puntos.csv"

    puntos = leer_puntos_csv(ruta)
    hull = convex_hull(puntos)

    print(f"Puntos: {len(puntos)}")
    print(f"Vértices del hull: {len(hull)}")

    dibujar(puntos, hull, titulo="Convex Hull")



    
# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Entrada de Datos")
ventana.geometry("800x500")

# 2. Campo de entrada (Entry)


# 3. Botón para confirmar la acción
boton = tk.Button(ventana, text="Seleccionar archivo CSV", command=seleccionar_archivo)
boton.pack(pady=20)

# Etiqueta para mostrar el resultado
#etiqueta_resultado = tk.Label(ventana, text="")
#etiqueta_resultado.pack()

ventana.mainloop()

