import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import copy

class SimulationGUI:
    def __init__(self, controller, university_classes):
        self.controller = controller
        self.university_classes = university_classes

        self.root = tk.Tk()
        self.root.title("Simulación de Reservas de Laboratorio")
        self.root.geometry("900x600")

        # Frame principal
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        # Selección de clases de simulación (múltiple)
        tk.Label(main_frame, text="Clases de Simulación:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
        self.class_listbox = tk.Listbox(main_frame, selectmode=tk.MULTIPLE, height=6, width=35, font=("Arial", 11))
        for cls in university_classes:
            self.class_listbox.insert(tk.END, cls.__name__)
        self.class_listbox.grid(row=1, column=0, sticky="w")
        self.class_listbox.bind("<<ListboxSelect>>", self.show_class_description)

        # Descripción
        self.desc_label = tk.Label(main_frame, text="", wraplength=400, justify="left", font=("Arial", 10))
        self.desc_label.grid(row=2, column=0, sticky="w", pady=5)

        # Número de alumnos
        tk.Label(main_frame, text="Número de alumnos:", font=("Arial", 12, "bold")).grid(row=0, column=1, sticky="w")
        self.students_var = tk.IntVar(value=1)
        tk.Entry(main_frame, textvariable=self.students_var, font=("Arial", 11), width=8).grid(row=1, column=1, sticky="w")

        # Número de iteraciones
        tk.Label(main_frame, text="N° de iteraciones:", font=("Arial", 12, "bold")).grid(row=0, column=2, sticky="w")
        self.iter_var = tk.IntVar(value=1)
        tk.Entry(main_frame, textvariable=self.iter_var, font=("Arial", 11), width=8).grid(row=1, column=2, sticky="w")

        # Botón de simulación
        tk.Button(main_frame, text="Comparar", font=("Arial", 12, "bold"), command=self.run_comparison).grid(row=1, column=3, padx=20)

        # Botones para ver grafo y estadísticas (deshabilitados por defecto)
        self.btn_graph = tk.Button(main_frame, text="Ver Grafo", font=("Arial", 11), state=tk.DISABLED, command=self.show_graph)
        self.btn_graph.grid(row=2, column=1, pady=5)
        self.btn_stats = tk.Button(main_frame, text="Ver Estadísticas", font=("Arial", 11), state=tk.DISABLED, command=self.show_stats)
        self.btn_stats.grid(row=2, column=2, pady=5)

        # Tabla de métricas comparativas
        self.metrics_tree = ttk.Treeview(main_frame, columns=("Clase", "Métrica", "Promedio"), show="headings", height=18)
        self.metrics_tree.heading("Clase", text="Clase")
        self.metrics_tree.heading("Métrica", text="Métrica")
        self.metrics_tree.heading("Promedio", text="Promedio")
        self.metrics_tree.column("Clase", width=180)
        self.metrics_tree.column("Métrica", width=250)
        self.metrics_tree.column("Promedio", width=120)
        self.metrics_tree.grid(row=3, column=0, columnspan=4, pady=20, sticky="nsew")

        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_columnconfigure(3, weight=1)

    def show_class_description(self, event=None):
        selected = self.class_listbox.curselection()
        if not selected:
            self.desc_label.config(text="")
            return
        descs = {
            cls.__name__: cls.__doc__ or "Sin descripción."
            for cls in self.university_classes
        }
        desc_text = ""
        for idx in selected:
            class_name = self.class_listbox.get(idx)
            desc_text += f"{class_name}: {descs.get(class_name, '')}\n\n"
        self.desc_label.config(text=desc_text.strip())

    def show_loading(self):
        self.loading_win = tk.Toplevel(self.root)
        self.loading_win.title("Procesando...")
        self.loading_win.geometry("350x120")
        self.loading_win.transient(self.root)
        self.loading_win.grab_set()
        tk.Label(self.loading_win, text="Esto podría tardar un poco...\nPor favor espera.", font=("Arial", 12)).pack(pady=10)
        self.progress = ttk.Progressbar(self.loading_win, mode="indeterminate", length=250)
        self.progress.pack(pady=10)
        self.progress.start(10)

    def hide_loading(self):
        if hasattr(self, "progress"):
            self.progress.stop()
        if hasattr(self, "loading_win"):
            self.loading_win.destroy()

    def show_graph(self):
        if hasattr(self, "last_university") and self.last_university:
            self.controller.change_university(self.last_university)
            self.controller.show_pending_bookings_graph()

    def show_stats(self):
        if hasattr(self, "last_university") and self.last_university:
            self.controller.change_university(self.last_university)
            self.controller.show_booking_stats()

    def run_comparison(self):
        selected_indices = self.class_listbox.curselection()
        n_students = self.students_var.get()
        n_iter = self.iter_var.get()
        if not selected_indices or n_students < 1 or n_iter < 1:
            messagebox.showerror("Error", "Selecciona al menos una clase, un número válido de alumnos y de iteraciones.")
            return

        # Deshabilita los botones antes de simular
        self.btn_graph.config(state=tk.DISABLED)
        self.btn_stats.config(state=tk.DISABLED)
        self.last_university = None

        def task():
            selected_classes = [self.university_classes[i] for i in selected_indices]
            results = {cls.__name__: [] for cls in selected_classes}
            last_university = None

            for cls in selected_classes:
                for _ in range(n_iter):
                    students = [self.controller.university.students[0].__class__(f"Student_{i+1}", i+1) for i in range(n_students)]
                    labs_copy = copy.deepcopy(self.controller.university.laboratories)
                    tools_copy = copy.deepcopy(self.controller.university.laboratory_tools)
                    university = cls(labs_copy, tools_copy, students)
                    controller = self.controller.__class__(university)
                    controller.concurrent_ramdom_bookings([i+1 for i in range(n_students)])
                    stats = controller.get_statistics()
                    results[cls.__name__].append(stats)
                    last_university = university

            def update_table():
                for row in self.metrics_tree.get_children():
                    self.metrics_tree.delete(row)
                metric_keys = set()
                for stats in results.values():
                    for stat in stats:
                        metric_keys.update(stat.keys())
                metric_keys = [k for k in metric_keys if "time" in k.lower() or "total" in k.lower() or "pending" in k.lower() or "approved" in k.lower() or "rejected" in k.lower() or "finished" in k.lower()]
                for cls_name, stats_list in results.items():
                    for stat in stats_list:
                        for key in metric_keys:
                            value = stat.get(key, "-")
                            self.metrics_tree.insert("", "end", values=(cls_name, key, f"{value:.4f}" if isinstance(value, float) else value))
                self.hide_loading()
                # Si solo hay una clase, guarda la universidad y habilita los botones
                if len(selected_indices) == 1 and last_university is not None:
                    self.last_university = last_university
                    self.btn_graph.config(state=tk.NORMAL)
                    self.btn_stats.config(state=tk.NORMAL)
                else:
                    self.last_university = None

            self.root.after(0, update_table)

        self.show_loading()
        threading.Thread(target=task, daemon=True).start()

    def run(self):
        self.root.mainloop()