# Simulación de Reservas de Laboratorio

Este proyecto permite comparar diferentes estrategias de gestión de reservas de laboratorios universitarios usando concurrencia y simulación. Incluye una interfaz gráfica desarrollada en Tkinter para seleccionar clases de simulación, definir parámetros y visualizar resultados.

## Requisitos

- Python 3.8+
- [networkx](https://networkx.org/)
- [matplotlib](https://matplotlib.org/)
- [scipy](https://scipy.org/)
- [pandas](https://pandas.pydata.org/)

Puedes instalar las dependencias ejecutando:

```sh
pip install networkx matplotlib scipy pandas
```
o

```sh
pip install -r requirements.txt
```

## Uso

1. Ejecuta el archivo principal de la aplicación 
```sh 
python main.py 
```
2. Selecciona una o varias clases de simulación.
3. Define el número de alumnos y de iteraciones.
4. Haz clic en **Comparar** para ejecutar la simulación.
5. Si seleccionas solo una clase, podrás usar los botones **Ver Grafo** y **Ver Estadísticas** para visualizar los resultados detallados de esa simulación.

## Estructura del Proyecto

- `views/`: Contiene la interfaz gráfica (`simulation_gui.py`).
- `controllers/`: Lógica de control y coordinación.
- `models/`: Lógica de negocio y entidades principales.
- Otros módulos para visualización de gráficos y estadísticas.

## Visualizaciones

- **Ver Grafo**: Muestra el grafo de reservas pendientes usando NetworkX y Matplotlib.
- **Ver Estadísticas**: Muestra estadísticas de reservas en formato tabla usando Pandas.
