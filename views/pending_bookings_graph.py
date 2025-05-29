import networkx as nx
import matplotlib.pyplot as plt

class PendingBookingsGraph:
    def __init__(self, pending_bookings, laboratories, laboratory_tools):
        self.pending_bookings = pending_bookings
        self.laboratories = laboratories
        self.laboratory_tools = laboratory_tools
        self.G = nx.Graph()

    def build_graph(self):
        for booking in self.pending_bookings:
            booking_node = f"Booking {booking.booking_id}\n{booking.status.name}"
            self.G.add_node(booking_node, type='booking')

            # --- Laboratorio solicitado ---
            lab_solicited = next((l for l in self.laboratories if l.id == booking.room_id_solicited), None)
            if lab_solicited:
                lab_node = f"Lab {lab_solicited.id}: \n{lab_solicited.name}"
                self.G.add_node(lab_node, type='lab')
                self.G.add_edge(booking_node, lab_node, label='requests')

            # --- Laboratorio asignado (si hay) ---
            if booking.room_id:
                lab_assigned = next((l for l in self.laboratories if l.id == booking.room_id), None)
                if lab_assigned:
                    lab_node = f"Lab {lab_assigned.id}: \n{lab_assigned.name}"
                    self.G.add_node(lab_node, type='lab')
                    self.G.add_edge(booking_node, lab_node, label='assigned')

            # --- Herramientas solicitadas ---
            for tool_id in booking.tool_ids_solicited:
                tool = next((t for t in self.laboratory_tools if t.id == tool_id), None)
                if tool:
                    tool_node = f"{tool.id} tool: \n{tool.name}"
                    self.G.add_node(tool_node, type='tool')
                    self.G.add_edge(booking_node, tool_node, label='requests')

            # --- Herramientas asignadas (si hay) ---
            for tool_id in booking.tool_ids:
                tool = next((t for t in self.laboratory_tools if t.id == tool_id), None)
                if tool:
                    tool_node = f"{tool.id} tool: \n{tool.name}"
                    self.G.add_node(tool_node, type='tool')
                    self.G.add_edge(booking_node, tool_node, label='assigned')

    def draw(self):
        plt.figure(figsize=(14, 8))
        pos = nx.spring_layout(self.G, k=1.2, iterations=2000)
        labels = nx.get_edge_attributes(self.G, 'label')
        node_colors = []
        for n, d in self.G.nodes(data=True):
            if d.get('type') == 'tool':
                node_colors.append('orange')
            elif d.get('type') == 'lab':
                node_colors.append('lightblue')
            else:
                node_colors.append('lightgreen')
        nx.draw(self.G, pos, with_labels=True, node_color=node_colors, node_size=1200, font_size=9, arrows=False)
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=labels, font_size=8)
        plt.title("Pending Bookings Graph (Solicited & Assigned)")
        plt.tight_layout()
        plt.show()