import customtkinter as ctk
import tkinter as tk 

class UiStaff:
    def __init__(self, window, width, height, start_callback, settings_callback, restart_callback, exit_callback, show_path_callback):
        self.window = window
        self.width = width
        self.height = height
        #сохраняем колбэки для доступа внутри класса
        self.start_callback = start_callback
        self.settings_callback = settings_callback
        self.restart_callback = restart_callback
        self.exit = exit_callback
        self.show_path_callback = show_path_callback
       

        #левая паенль для управления
        self.panel = ctk.CTkFrame(window, width=200, height=580)
        self.panel.pack(side="left", padx=10, fill="y")

        #текстовый номер поколения 
        self.label_gen = ctk.CTkLabel (self.panel, text = "Generation: 1", font = ("Times New Roman", 20, "bold"))
        self.label_gen.pack (pady = 20)

        #кнопка старт/пауза
        self.btn_start = ctk.CTkButton (self.panel, text = "Start [Space]", font = ("Arial", 16), fg_color = "green", command = self.start_callback)
        self.btn_start.pack (pady = 10, padx = 20, fill = "x")

        # кнопка рестарта
        self.btn_restart = ctk.CTkButton (self.panel, text = "Restart [R]", font = ("Arial", 14), fg_color = "#795038", command = self.restart_callback)
        self.btn_restart.pack (pady = 10, padx = 20, fill = "x")

        #кнопка показать путь волновым алгоритмом 
        self.btn_show_path = ctk.CTkButton (self.panel, text = "Show path", font = ("Arial", 14), fg_color = "#1a6fa3", command = self.show_path_callback)
        self.btn_show_path.pack (pady = 10, padx = 20, fill = "x")

        #информационная панель снизу
        self.info_frame = ctk.CTkFrame(self.panel, fg_color="#2a2a2a", corner_radius=8)
        self.info_frame.pack(pady=20, padx=10, fill="x", side="bottom")

        self.label_best = ctk.CTkLabel(self.info_frame, text="Best fitness: 0", font=("Arial", 12), anchor="w")
        self.label_best.pack(padx=10, pady=2, fill="x")

        self.label_record = ctk.CTkLabel(self.info_frame, text="Record fitness: 0", font=("Arial", 12), anchor="w")
        self.label_record.pack(padx=10, pady=2, fill="x")

        self.label_alive = ctk.CTkLabel(self.info_frame, text="Alive agents: 0/0", font=("Arial", 12), anchor="w")
        self.label_alive.pack(padx=10, pady=2, fill="x")

        self.label_status = ctk.CTkLabel(self.info_frame, text="Status: Stopped", font=("Arial", 12), anchor="w")
        self.label_status.pack(padx=10, pady=(2, 8), fill="x")

        #создаем canvas для отрисовки точек
        self.canvas = tk.Canvas(window, width = width, height = height, bg = "#1e1e1e", highlightthickness = 0)
        self.canvas.pack (side = "right", padx = 10, pady = 10)
        
        #привязка клавиш 
        self.window.bind ("<space>", lambda e: self.start_callback())
        self.window.bind ("<r>", lambda e: self.restart_callback())
        self.window.bind ("<R>", lambda e: self.restart_callback())
        self.window.bind ("<Escape>", lambda e: self.window.destroy())

        #обновление информационной панели, вызов из the genetic
    def update_info (self, generation, best_fitness, record_fitness, alive, total, running):

         self.label_gen.configure(text =f"Generation: {generation}")
         self.label_best.configure(text=f"Closeness: {round(best_fitness, 1)}")
         self.label_record.configure(text = f"Record fitness: {round(record_fitness, 1)}")
         self.label_alive.configure(text = f"Alive agents: {alive}/{total}")
         if record_fitness == -999999:
            self.label_record.configure(text="Record fitness: —")
         else:
            self.label_record.configure(text=f"Record fitness: {round(record_fitness, 1)}")

         if running:
             status = "Running"
         else:
             status = "Stopped"

         self.label_status.configure(text = f"Status: {status}")

        #смена текста кнопки старт/стоп 
    def set_btn_start_text(self, text, color):
         self.btn_start.configure(text = text, fg_color = color)