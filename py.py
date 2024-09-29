import tkinter as tk
from tkinter import ttk

class ScrollingTreeview(ttk.Treeview):
    def __init__(self, master=None, scroll_columns=None, **kw):
        super().__init__(master, **kw)
        self.scroll_columns = scroll_columns if scroll_columns else []
        self.full_texts = {}       # {item_id: {column: full_text}}
        self.scroll_positions = {} # {item_id: {column: current_pos}}
        self.update_counters = {}  # {item_id: {column: counter}}

    def insert_row(self, parent, index, values, **kw):
        item_id = super().insert(parent, index, values=values, **kw)
        self.full_texts[item_id] = {}
        self.scroll_positions[item_id] = {}
        self.update_counters[item_id] = {}
        for col in self.scroll_columns:
            try:
                col_index = self["columns"].index(col)
                full_text = str(values[col_index]) + "   "
                self.full_texts[item_id][col] = full_text
                self.scroll_positions[item_id][col] = 0
                self.update_counters[item_id][col] = 0
            except ValueError:
                continue
        return item_id

    def animate_text(self):
        for item_id in self.get_children():
            for col in self.scroll_columns:
                full_text = self.full_texts.get(item_id, {}).get(col, "")
                if not full_text:
                    continue
                col_width = self.column(col, option='width')
                display_length = max(1, col_width // 7)
                if len(full_text) <= display_length:
                    continue

                counter = self.update_counters[item_id][col]
                if counter >= 1:
                    pos = self.scroll_positions[item_id][col]
                    display_text = full_text[pos: pos + display_length]
                    if len(display_text) < display_length:
                        pos = 0
                        display_text = full_text[pos: pos + display_length]
                    else:
                        pos += 1

                    self.scroll_positions[item_id][col] = pos
                    self.update_counters[item_id][col] = 0

                    current_values = list(self.item(item_id, "values"))
                    col_index = self["columns"].index(col)
                    current_values[col_index] = display_text
                    self.item(item_id, values=current_values)
                else:
                    self.update_counters[item_id][col] += 1

        self.after(100, self.animate_text)

def main():
    root = tk.Tk()
    root.title("Inventario de Productos")
    root.geometry("1400x600")

    productos_data = [
        ("CLAMP-001", "Abrazadera Clamp Reforzada T-304 DLaT SST304 1/2\" - 3/4\"", "Abrazadera Clamp Reforzada", "Clamp", "SST304", "1/2\" - 3/4\"", 100, 51.84, 10, "A1", "S1", "DLaT", "2024-01-10"),
        ("CLAMP-001", "Abrazadera Clamp Reforzada T-304 DLaT SST304 1\" - 1-1/2\"", "Abrazadera Clamp Reforzada", "Clamp", "SST304", "1\" - 1-1/2\"", 100, 51.84, 10, "A1", "S1", "DLaT", "2024-01-10"),
        ("CLAMP-001", "Abrazadera Clamp Reforzada T-304 DLaT SST304 2\" - 2-1/2\"", "Abrazadera Clamp Reforzada", "Clamp", "SST304", "2\" - 2-1/2\"", 100, 51.84, 10, "A1", "S1", "DLaT", "2024-01-10"),
        ("CLAMP-001", "Abrazadera Clamp Reforzada T-304 DLaT SST304 3\" - 4\"", "Abrazadera Clamp Reforzada", "Clamp", "SST304", "3\" - 4\"", 100, 51.84, 10, "A1", "S1", "DLaT", "2024-01-10"),
        ("CLAMP-001", "Abrazadera Clamp Reforzada T-304 DLaT SST304 6\" - 8\"", "Abrazadera Clamp Reforzada", "Clamp", "SST304", "6\" - 8\"", 100, 51.84, 10, "A1", "S1", "DLaT", "2024-01-10"),
        ("CLAMP-001", "Abrazadera Clamp Reforzada T-304 DLaT SST304 10\"", "Abrazadera Clamp Reforzada", "Clamp", "SST304", "10\"", 100, 51.84, 10, "A1", "S1", "DLaT", "2024-01-10"),
        
        ("ADP-002", "Adaptador Hembra Clamp T-304 DLaT SST304 1\" x 1\"", "Adaptador Hembra Clamp", "Clamp", "SST304", "1\" x 1\"", 200, 464.40, 20, "A1", "S1", "DLaT", "2024-02-15"),
        ("ADP-002", "Adaptador Hembra Clamp T-304 DLaT SST304 1-1/2\" x 1-1/2\"", "Adaptador Hembra Clamp", "Clamp", "SST304", "1-1/2\" x 1-1/2\"", 200, 464.40, 20, "A1", "S1", "DLaT", "2024-02-15"),
        ("ADP-002", "Adaptador Hembra Clamp T-304 DLaT SST304 2\" x 2\"", "Adaptador Hembra Clamp", "Clamp", "SST304", "2\" x 2\"", 200, 464.40, 20, "A1", "S1", "DLaT", "2024-02-15"),
        
        ("ADP-003", "Adaptador Macho Clamp T-304 DLaT SST304 1\" x 1\"", "Adaptador Macho Clamp", "Clamp", "SST304", "1\" x 1\"", 150, 475.20, 15, "A1", "S1", "DLaT", "2024-02-15"),
        ("ADP-003", "Adaptador Macho Clamp T-304 DLaT SST304 1-1/2\" x 1-1/2\"", "Adaptador Macho Clamp", "Clamp", "SST304", "1-1/2\" x 1-1/2\"", 150, 475.20, 15, "A1", "S1", "DLaT", "2024-02-15"),
        ("ADP-003", "Adaptador Macho Clamp T-304 DLaT SST304 2\" x 2\"", "Adaptador Macho Clamp", "Clamp", "SST304", "2\" x 2\"", 150, 475.20, 15, "A1", "S1", "DLaT", "2024-02-15"),
        
        ("CODO-45-001", "Codo 45° Clamp T-304 DLaT SST304 1\" - 1-1/2\"", "Codo 45° Clamp", "Codo", "SST304", "1\" - 1-1/2\"", 120, 101.52, 12, "B1", "S1", "DLaT", "2024-03-01"),
        ("CODO-45-001", "Codo 45° Clamp T-304 DLaT SST304 2\" - 2-1/2\"", "Codo 45° Clamp", "Codo", "SST304", "2\" - 2-1/2\"", 120, 101.52, 12, "B1", "S1", "DLaT", "2024-03-01"),
        ("CODO-45-001", "Codo 45° Clamp T-304 DLaT SST304 3\" - 4\"", "Codo 45° Clamp", "Codo", "SST304", "3\" - 4\"", 120, 101.52, 12, "B1", "S1", "DLaT", "2024-03-01"),
        
        ("CODO-90-002", "Codo 90° Clamp T-304 DLaT SST304 1\" - 1-1/2\"", "Codo 90° Clamp", "Codo", "SST304", "1\" - 1-1/2\"", 80, 232.20, 8, "B1", "S1", "DLaT", "2024-03-10"),
        ("CODO-90-002", "Codo 90° Clamp T-304 DLaT SST304 2\" - 2-1/2\"", "Codo 90° Clamp", "Codo", "SST304", "2\" - 2-1/2\"", 80, 232.20, 8, "B1", "S1", "DLaT", "2024-03-10"),
        ("CODO-90-002", "Codo 90° Clamp T-304 DLaT SST304 3\" - 4\"", "Codo 90° Clamp", "Codo", "SST304", "3\" - 4\"", 80, 232.20, 8, "B1", "S1", "DLaT", "2024-03-10"),
        ("CODO-90-002", "Codo 90° Clamp T-304 DLaT SST304 6\"", "Codo 90° Clamp", "Codo", "SST304", "6\"", 80, 232.20, 8, "B1", "S1", "DLaT", "2024-03-10"),
        
        # Otros productos y medidas se agregarían aquí de forma similar...
    ]

    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    columns = ("Código", "Nombre Completo", "Nombre", "Tipo", "Material", "Medida", "Cantidad", "Precio", "Mínimo", "Rack", "Sección", "Marca", "Fecha de Compra")
    table = ScrollingTreeview(frame, columns=columns, show="headings", scroll_columns=columns)

    for col in columns:
        table.heading(col, text=col)
        table.column(col, anchor=tk.CENTER, width=150, minwidth=50, stretch=False)

    for producto in productos_data:
        table.insert_row("", tk.END, values=producto)

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=table.yview)
    table.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    table.pack(fill=tk.BOTH, expand=True)

    table.animate_text()

    root.mainloop()

if __name__ == "__main__":
    main()
