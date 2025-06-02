import matplotlib.pyplot as plt
import pandas as pd

class BookingStatsTable:
    def __init__(self, booking_details):
        self.booking_details = booking_details
        self.df = pd.DataFrame(self._to_dict_list())

    def _to_dict_list(self):
        # Convierte los objetos a un diccionario simple para pandas
        dicts = []
        for b in self.booking_details:
            dicts.append({
                "booking_id": b.get("booking_id"),
                "student": str(b.get("student")),
                "laboratory": str(b.get("laboratory")) if b.get("laboratory") else None,
                "tools": ", ".join([str(t) for t in b.get("tools")]) if b.get("tools") else "",
                "status": b.get("status"),
            })
        return dicts

    def show_stats(self):
        total = len(self.df)
        by_status = self.df['status'].value_counts()
        no_lab = self.df['laboratory'].isna().sum()
        no_tools = (self.df['tools'] == "").sum()

        # Gráfico de barras para estados
        plt.figure(figsize=(8, 4))
        by_status.plot(kind='bar', color='skyblue')
        plt.title('Bookings by Status')
        plt.xlabel('Status')
        plt.ylabel('Count')
        plt.tight_layout()
        plt.show()

        # Gráfico de pastel para laboratorios asignados vs no asignados
        plt.figure(figsize=(5, 5))
        plt.pie([total - no_lab, no_lab], labels=['With Lab', 'Without Lab'], autopct='%1.1f%%', colors=['#66b3ff', '#ff9999'])
        plt.title('Bookings With/Without Laboratory')
        plt.show()

        # Gráfico de pastel para herramientas asignadas vs no asignadas
        plt.figure(figsize=(5, 5))
        plt.pie([total - no_tools, no_tools], labels=['With Tools', 'Without Tools'], autopct='%1.1f%%', colors=['#99ff99', '#ffcc99'])
        plt.title('Bookings With/Without Tools')
        plt.show()

        # Mostrar primeras 10 filas como tabla
        #print("\n=== First 10 bookings ===")
        #print(self.df.head(10).to_string(index=False))

    def show_table(self):
        print(self.df.to_string(index=False))