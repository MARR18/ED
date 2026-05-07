import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, scrolledtext
import time
import re
import json
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import pandas as pd
from docx import Document
import openpyxl

# Configuración del tema oscuro moderno
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SortingApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Sorting Suite - Intercalación | Mezcla Directa | Mezcla Equilibrada")
        self.root.geometry("1400x800")
        self.root.minsize(1200, 700)
        
        # Variables de estado
        self.original_data = []          # Datos originales (inmutables)
        self.current_data = []           # Datos en proceso de ordenamiento
        self.sorting_generator = None
        self.comparisons = 0
        self.moves = 0
        self.start_time = 0
        self.is_sorting = False
        self.selected_method = "Intercalación"
        self.max_display = 200
        
        self.setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_ui(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Panel izquierdo: Controles, log, estadísticas
        self.left_panel = ctk.CTkFrame(self.main_frame, width=400)
        self.left_panel.pack(side="left", fill="both", expand=False, padx=(0, 10))
        self.left_panel.pack_propagate(False)
        
        # Panel derecho: Visualización y datos
        self.right_panel = ctk.CTkFrame(self.main_frame)
        self.right_panel.pack(side="right", fill="both", expand=True)
        
        # ========== Panel izquierdo ==========
        # Sección de carga de archivo
        self.file_frame = ctk.CTkFrame(self.left_panel)
        self.file_frame.pack(fill="x", padx=10, pady=10)
        
        self.load_btn = ctk.CTkButton(self.file_frame, text="📂 Cargar Archivo", command=self.load_file, font=("Segoe UI", 14))
        self.load_btn.pack(side="left", padx=5, pady=5)
        
        self.file_label = ctk.CTkLabel(self.file_frame, text="Ningún archivo cargado", font=("Segoe UI", 12))
        self.file_label.pack(side="left", padx=10)
        
        # Selector del método de ordenamiento
        self.method_frame = ctk.CTkFrame(self.left_panel)
        self.method_frame.pack(fill="x", padx=10, pady=10)
        
        self.method_label = ctk.CTkLabel(self.method_frame, text="Algoritmo:", font=("Segoe UI", 14, "bold"))
        self.method_label.pack(side="left", padx=5)
        
        self.method_var = ctk.StringVar(value="Intercalación")
        self.method_menu = ctk.CTkOptionMenu(self.method_frame, values=["Intercalación", "Mezcla Directa", "Mezcla Equilibrada"],
                                              variable=self.method_var, command=self.on_method_change)
        self.method_menu.pack(side="left", padx=10)
        
        # Botón iniciar ordenamiento
        self.sort_btn = ctk.CTkButton(self.left_panel, text="🚀 Iniciar Ordenamiento", command=self.start_sorting,
                                      font=("Segoe UI", 14, "bold"), height=40)
        self.sort_btn.pack(fill="x", padx=10, pady=10)
        
        # Estadísticas
        self.stats_frame = ctk.CTkFrame(self.left_panel)
        self.stats_frame.pack(fill="x", padx=10, pady=10)
        
        self.time_label = ctk.CTkLabel(self.stats_frame, text="⏱️ Tiempo: -- ms", font=("Segoe UI", 13))
        self.time_label.pack(anchor="w", padx=5, pady=2)
        
        self.comp_label = ctk.CTkLabel(self.stats_frame, text="🔢 Comparaciones: 0", font=("Segoe UI", 13))
        self.comp_label.pack(anchor="w", padx=5, pady=2)
        
        self.moves_label = ctk.CTkLabel(self.stats_frame, text="🔄 Movimientos: 0", font=("Segoe UI", 13))
        self.moves_label.pack(anchor="w", padx=5, pady=2)
        
        self.elements_label = ctk.CTkLabel(self.stats_frame, text="📊 Elementos: 0", font=("Segoe UI", 13))
        self.elements_label.pack(anchor="w", padx=5, pady=2)
        
        # Consola visual / Log
        self.log_frame = ctk.CTkFrame(self.left_panel)
        self.log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.log_title = ctk.CTkLabel(self.log_frame, text="📝 Registro de Proceso", font=("Segoe UI", 14, "bold"))
        self.log_title.pack(anchor="w", padx=5, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(self.log_frame, wrap=tk.WORD, height=12, bg="#2b2b2b", fg="#ffffff",
                                                  font=("Consolas", 11))
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Barra de estado
        self.status_bar = ctk.CTkLabel(self.left_panel, text="✅ Listo", font=("Segoe UI", 12), anchor="w")
        self.status_bar.pack(fill="x", padx=10, pady=(0, 10))
        
        # ========== Panel derecho ==========
        # Visualización gráfica (barras)
        self.canvas_frame = ctk.CTkFrame(self.right_panel)
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Datos originales y ordenados (texto)
        self.text_frame = ctk.CTkFrame(self.right_panel)
        self.text_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.original_label = ctk.CTkLabel(self.text_frame, text="📄 Datos Originales:", font=("Segoe UI", 13, "bold"))
        self.original_label.pack(anchor="w")
        
        self.original_text = scrolledtext.ScrolledText(self.text_frame, height=4, bg="#2b2b2b", fg="#ffffff",
                                                       font=("Consolas", 11))
        self.original_text.pack(fill="x", pady=(0, 5))
        
        self.sorted_label = ctk.CTkLabel(self.text_frame, text="✅ Datos Ordenados:", font=("Segoe UI", 13, "bold"))
        self.sorted_label.pack(anchor="w")
        
        self.sorted_text = scrolledtext.ScrolledText(self.text_frame, height=4, bg="#2b2b2b", fg="#ffffff",
                                                     font=("Consolas", 11))
        self.sorted_text.pack(fill="x")
        
    def on_method_change(self, choice):
        self.selected_method = choice
        self.log(f"Método cambiado a: {choice}")
        
    def log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
    def update_status(self, message, is_error=False):
        self.status_bar.configure(text=message, text_color="red" if is_error else "#ffffff")
        self.root.update_idletasks()
        
    def load_file(self):
        filetypes = [
            ("Todos los soportados", "*.json *.txt *.csv *.xlsx *.docx *.html *.xml"),
            ("JSON", "*.json"), ("TXT", "*.txt"), ("CSV", "*.csv"),
            ("Excel", "*.xlsx"), ("Word", "*.docx"), ("HTML", "*.html"), ("XML", "*.xml")
        ]
        filepath = ctk.filedialog.askopenfilename(filetypes=filetypes)
        if not filepath:
            return
        
        self.update_status("Cargando archivo...")
        numbers = []
        try:
            if filepath.endswith('.json'):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                numbers = self._extract_numbers(str(data))
            
            elif filepath.endswith('.txt'):
                with open(filepath, 'r', encoding='utf-8') as f:
                    text = f.read()
                numbers = self._extract_numbers(text)
            
            elif filepath.endswith('.csv'):
                df = pd.read_csv(filepath)
                numbers = self._extract_numbers(df.to_string())
            
            elif filepath.endswith('.xlsx'):
                df = pd.read_excel(filepath)
                numbers = self._extract_numbers(df.to_string())
            
            elif filepath.endswith('.docx'):
                doc = Document(filepath)
                full_text = "\n".join([para.text for para in doc.paragraphs])
                numbers = self._extract_numbers(full_text)
            
            elif filepath.endswith('.html'):
                with open(filepath, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')
                    numbers = self._extract_numbers(soup.get_text())
            
            elif filepath.endswith('.xml'):
                tree = ET.parse(filepath)
                root = tree.getroot()
                text = ET.tostring(root, encoding='unicode')
                numbers = self._extract_numbers(text)
            
            else:
                raise ValueError("Formato no soportado")
            
            if not numbers:
                raise ValueError("No se encontraron números en el archivo")
            
            # Conservar el tipo original (int o float)
            self.original_data = numbers[:]
            self.current_data = numbers[:]
            self.elements_label.configure(text=f"📊 Elementos: {len(self.original_data)}")
            
            # Mostrar datos originales (hasta 100)
            display_orig = self.original_data[:100]
            self.original_text.delete(1.0, tk.END)
            self.original_text.insert(tk.END, ", ".join(str(x) for x in display_orig))
            if len(self.original_data) > 100:
                self.original_text.insert(tk.END, "...")
            
            self.sorted_text.delete(1.0, tk.END)
            self.sorted_text.insert(tk.END, "Aún no ordenado")
            
            self.draw_bars(self.original_data)
            self.file_label.configure(text=filepath.split("/")[-1])
            self.log(f"Archivo cargado: {filepath}. Se encontraron {len(self.original_data)} números.")
            self.update_status("Archivo cargado correctamente")
            
            # Resetear estadísticas
            self.comparisons = 0
            self.moves = 0
            self.comp_label.configure(text="🔢 Comparaciones: 0")
            self.moves_label.configure(text="🔄 Movimientos: 0")
            self.time_label.configure(text="⏱️ Tiempo: -- ms")
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}", is_error=True)
            self.log(f"ERROR al cargar archivo: {str(e)}")
            messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")
    
    def _extract_numbers(self, text):
        """Extrae números enteros y decimales de un texto."""
        pattern = r"-?\d+\.?\d*"
        matches = re.findall(pattern, text)
        numbers = []
        for m in matches:
            try:
                if '.' in m:
                    numbers.append(float(m))
                else:
                    numbers.append(int(m))
            except:
                continue
        return numbers
    
    def draw_bars(self, data):
        """Dibuja barras representando los datos en el canvas."""
        self.canvas.delete("all")
        if not data:
            return
        
        display_data = data[:self.max_display]
        if len(data) > self.max_display:
            self.canvas.create_text(10, 20, anchor="nw", fill="orange",
                                    text=f"Mostrando solo {self.max_display} de {len(data)} valores", font=("Segoe UI", 10))
        
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10 or h < 10:
            w, h = 800, 400
        
        n = len(display_data)
        if n == 0:
            return
        
        bar_width = max(2, w / n - 2)
        max_val = max(display_data) if display_data else 1
        min_val = min(display_data) if display_data else 0
        if max_val == min_val:
            max_val = min_val + 1
        
        for i, val in enumerate(display_data):
            norm = (val - min_val) / (max_val - min_val)
            bar_height = 20 + norm * (h - 60)
            x0 = i * (bar_width + 2)
            y0 = h - bar_height
            x1 = x0 + bar_width
            y1 = h - 10
            color = "#3a86ff" if not self.is_sorting else "#ff9e3a"
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
        
        self.canvas.update_idletasks()
    
    def start_sorting(self):
        if self.is_sorting:
            self.log("Ya hay un proceso de ordenamiento en curso")
            return
        
        if not self.original_data:
            self.update_status("Primero carga un archivo con datos", is_error=True)
            return
        
        # Reiniciar estado
        self.comparisons = 0
        self.moves = 0
        self.current_data = self.original_data[:]  # Copia fresca
        self.start_time = time.perf_counter()
        self.is_sorting = True
        self.sort_btn.configure(state="disabled", text="⏳ Ordenando...")
        self.load_btn.configure(state="disabled")
        self.method_menu.configure(state="disabled")
        
        self.log(f"Iniciando ordenamiento con método: {self.selected_method}")
        self.update_status(f"Ordenando con {self.selected_method}...")
        
        # Seleccionar el generador correspondiente
        if self.selected_method == "Intercalación":
            self.sorting_generator = self._merge_sort_generator(self.current_data, 0, len(self.current_data)-1)
        elif self.selected_method == "Mezcla Directa":
            self.sorting_generator = self._bottom_up_merge_sort_generator(self.current_data)
        elif self.selected_method == "Mezcla Equilibrada":
            self.sorting_generator = self._balanced_merge_sort_generator(self.current_data)
        else:
            self.is_sorting = False
            return
        
        self._next_step()
    
    def _next_step(self):
        try:
            state = next(self.sorting_generator)
            # Actualizar datos actuales
            self.current_data = state['data'][:]   # Asegurar copia
            self.comparisons = state['comparisons']
            self.moves = state['moves']
            
            # Actualizar interfaz
            self.draw_bars(self.current_data)
            self.comp_label.configure(text=f"🔢 Comparaciones: {self.comparisons}")
            self.moves_label.configure(text=f"🔄 Movimientos: {self.moves}")
            elapsed = (time.perf_counter() - self.start_time) * 1000
            self.time_label.configure(text=f"⏱️ Tiempo: {elapsed:.1f} ms")
            
            if state.get('log_msg'):
                self.log(state['log_msg'])
            
            # Programar siguiente paso (pequeño delay para visualización)
            self.root.after(5, self._next_step)
            
        except StopIteration:
            elapsed = (time.perf_counter() - self.start_time) * 1000
            self.log(f"Ordenamiento completado en {elapsed:.2f} ms")
            self.log(f"Comparaciones totales: {self.comparisons}, Movimientos totales: {self.moves}")
            self.update_status(f"Ordenamiento finalizado - {elapsed:.1f} ms")
            
            # Mostrar datos ordenados (hasta 100)
            display_sorted = self.current_data[:100]
            self.sorted_text.delete(1.0, tk.END)
            self.sorted_text.insert(tk.END, ", ".join(str(x) for x in display_sorted))
            if len(self.current_data) > 100:
                self.sorted_text.insert(tk.END, "...")
            
            # Verificar orden
            sorted_ok = all(self.current_data[i] <= self.current_data[i+1] 
                           for i in range(len(self.current_data)-1))
            if sorted_ok:
                self.log("✅ La lista está correctamente ordenada.")
            else:
                self.log("⚠️ Advertencia: La lista no está completamente ordenada.")
            
            self.is_sorting = False
            self.sort_btn.configure(state="normal", text="🚀 Iniciar Ordenamiento")
            self.load_btn.configure(state="normal")
            self.method_menu.configure(state="normal")
            self.sorting_generator = None
    
    # ------------------------------------------------------------
    # 1. INTERCALACIÓN (Merge Sort recursivo)
    # ------------------------------------------------------------
    def _merge_sort_generator(self, arr, left, right):
        """Merge Sort que devuelve paso a paso el estado actual del arreglo."""
        comparisons = 0
        moves = 0
        # Copia auxiliar (se usa para evitar múltiples asignaciones)
        temp = arr[:]
        
        def merge(l, m, r):
            nonlocal comparisons, moves, temp
            i, j, k = l, m+1, l
            while i <= m and j <= r:
                comparisons += 1
                if arr[i] <= arr[j]:
                    temp[k] = arr[i]
                    i += 1
                else:
                    temp[k] = arr[j]
                    j += 1
                moves += 1
                k += 1
                # Actualizar arr con el estado parcial de temp
                arr[:] = temp[:]
                yield {'data': arr[:], 'comparisons': comparisons, 'moves': moves, 'log_msg': None}
            while i <= m:
                temp[k] = arr[i]
                i += 1
                k += 1
                moves += 1
                arr[:] = temp[:]
                yield {'data': arr[:], 'comparisons': comparisons, 'moves': moves, 'log_msg': None}
            while j <= r:
                temp[k] = arr[j]
                j += 1
                k += 1
                moves += 1
                arr[:] = temp[:]
                yield {'data': arr[:], 'comparisons': comparisons, 'moves': moves, 'log_msg': None}
            # Copiar la sección mezclada de vuelta a arr y a temp (ya está en arr)
            yield {'data': arr[:], 'comparisons': comparisons, 'moves': moves, 'log_msg': f"Mezcla [{l}:{r}] completada"}
        
        def msort(l, r):
            if l < r:
                m = (l + r) // 2
                yield from msort(l, m)
                yield from msort(m+1, r)
                yield from merge(l, m, r)
        
        yield from msort(left, right)
        yield {'data': arr[:], 'comparisons': comparisons, 'moves': moves, 'log_msg': "Intercalación finalizada"}
    
    # ------------------------------------------------------------
    # 2. MEZCLA DIRECTA (Bottom-up Merge Sort)
    # ------------------------------------------------------------
    def _bottom_up_merge_sort_generator(self, arr):
        n = len(arr)
        comparisons = 0
        moves = 0
        width = 1
        temp = arr[:]
        
        def merge(l, m, r):
            nonlocal comparisons, moves, temp
            # Usamos una copia local de temp para no interferir
            local_temp = temp[:]
            i, j, k = l, m+1, l
            while i <= m and j <= r:
                comparisons += 1
                if arr[i] <= arr[j]:
                    local_temp[k] = arr[i]
                    i += 1
                else:
                    local_temp[k] = arr[j]
                    j += 1
                moves += 1
                k += 1
                arr[:] = local_temp[:]
                yield {'data': arr[:], 'comparisons': comparisons, 'moves': moves, 'log_msg': None}
            while i <= m:
                local_temp[k] = arr[i]
                i += 1
                k += 1
                moves += 1
                arr[:] = local_temp[:]
                yield {'data': arr[:], 'comparisons': comparisons, 'moves': moves, 'log_msg': None}
            while j <= r:
                local_temp[k] = arr[j]
                j += 1
                k += 1
                moves += 1
                arr[:] = local_temp[:]
                yield {'data': arr[:], 'comparisons': comparisons, 'moves': moves, 'log_msg': None}
            arr[l:r+1] = local_temp[l:r+1]
            temp[:] = arr[:]
        
        while width < n:
            for left in range(0, n, 2*width):
                mid = min(left + width - 1, n-1)
                right = min(left + 2*width - 1, n-1)
                if mid < right:
                    yield from merge(left, mid, right)
                    yield {'data': arr[:], 'comparisons': comparisons, 'moves': moves,
                           'log_msg': f"Mezcla directa: segmento [{left}:{right}] ancho={width}"}
            width *= 2
        yield {'data': arr[:], 'comparisons': comparisons, 'moves': moves, 'log_msg': "Mezcla Directa completada"}
    
    # ------------------------------------------------------------
    # 3. MEZCLA EQUILIBRADA (Implementación similar a Merge Sort iterativo)
    # ------------------------------------------------------------
    def _balanced_merge_sort_generator(self, arr):
        n = len(arr)
        comparisons = 0
        moves = 0
        width = 1
        temp = arr[:]
        
        def merge_pass(current_width):
            nonlocal comparisons, moves, temp
            i = 0
            while i < n:
                left = i
                mid = min(i + current_width - 1, n - 1)
                right = min(i + 2 * current_width - 1, n - 1)
                if mid < right:
                    # Mezclar [left..mid] y [mid+1..right]
                    l, r, k = left, mid+1, left
                    while l <= mid and r <= right:
                        comparisons += 1
                        if arr[l] <= arr[r]:
                            temp[k] = arr[l]
                            l += 1
                        else:
                            temp[k] = arr[r]
                            r += 1
                        moves += 1
                        k += 1
                        arr[:] = temp[:]
                        yield {'data': arr[:], 'comparisons': comparisons, 'moves': moves, 'log_msg': None}
                    while l <= mid:
                        temp[k] = arr[l]
                        l += 1
                        k += 1
                        moves += 1
                        arr[:] = temp[:]
                        yield {'data': arr[:], 'comparisons': comparisons, 'moves': moves, 'log_msg': None}
                    while r <= right:
                        temp[k] = arr[r]
                        r += 1
                        k += 1
                        moves += 1
                        arr[:] = temp[:]
                        yield {'data': arr[:], 'comparisons': comparisons, 'moves': moves, 'log_msg': None}
                    arr[left:right+1] = temp[left:right+1]
                i += 2 * current_width
                yield {'data': arr[:], 'comparisons': comparisons, 'moves': moves,
                       'log_msg': f"Mezcla equilibrada: ancho={current_width}"}
        
        while width < n:
            gen = merge_pass(width)
            for step in gen:
                yield step
            width *= 2
        yield {'data': arr[:], 'comparisons': comparisons, 'moves': moves, 'log_msg': "Mezcla Equilibrada finalizada"}
    
    def on_closing(self):
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SortingApp()
    app.run()