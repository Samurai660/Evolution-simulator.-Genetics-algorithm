import customtkinter as ctk
import tkinter as tk 

class UiStaff:
    def __init__(self, window, width, height, on_star_click):
        #левая панель для управления 
        self.panel = ctk.CTkFrame (window, width = 200, height = 580)
        self.panel.pack (side = "left", padx = 10, fill = "y")

        #текстовый номер поколения 
        self.label_gen = ctk.CTkLabel (self.panel, text = "Generation: 1", font = ("Times New Roman", 20, "bold"))
        self.label_gen.pack (pady = 20)

        #кнопка старт/пауза
        self.btn_start = ctk.CTkButton (self.panel, text = "Start", 
                                        font = ("Arial", 16), fg_color = "green",
                                        command = on_star_click)

        self.btn_start.pack (pady = 10, padx = 20, fill = "x")

        #создаем canvas для отрисовки точек

        self.canvas = tk.Canvas(window, width = width, height = heigth, bg = "1e1e1e", highlightthickness = 0)
        self.canvas.pack (side = "right", padx = 10, pady = 10)
