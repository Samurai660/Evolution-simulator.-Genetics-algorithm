import customtkinter as ctk
from simulation import EvolutionSimulation
from ui_stuff import UiStaff
import ui_stuff

class EvolutionApp:
    def __init__(self):
        #размер экрана и положение агентов
        self.width = 800
        self.height = 600
        self.start_x = 400
        self.start_y = 550
        self.target_x = 400
        self.target_y = 50

        # стена
        self.obstacle = (200, 280, 600, 320)

        # Переменные настроек
        self.pop_size = 50
        self.mutation_rate = 0.05

        # Инициализируем логику толпы ботов
        self.sim = EvolutionSimulation (population_size=self.pop_size, start_x=self.start_x, start_y=self.start_y)
        self.current_step = 0
        self.is_running = False

        # Создаем окно базы
        self.window = ctk.CTk()
        self.window.title("Simulator evolution AI")
        self.window.geometry("1050x650")
        self.window.resizable(False, False)

        #инициализируем графику
        self.ui = UiStaff (self.window, self.width, self.height, self.start_button_clicked, self.apply_settings_clicked)
        
        # Отрисовываем первый стартовый кадр
        self.redraw_screen()

    def redraw_screen(self):
        #отрсовка объектов на экране
        self.ui.canvas.delete("all")
        
        # Старт и Финиш
        self.ui.canvas.create_oval (self.target_x - 15, self.target_y - 15, self.target_x + 15, self.target_y + 15, fill = "green", outline = "")
        self.ui.canvas.create_oval (self.start_x - 10, self.start_y - 10, self.start_x + 10, self.start_y + 10, fill = "blue", outline = "")
        
        # Стена
        self.ui.canvas.create_rectangle (self.obstacle[0], self.obstacle[1], self.obstacle[2], self.obstacle[3], fill = "#e74c3c", outline = "")
        
        #точки агенты: фиолетовые - живые, серые - нет
        for agent in self.sim.agents:
            if agent.is_alive:
                colot = "violet"
            else:
                color = "grey"
            self.ui.canvas.create_oval(agent.x - 4, agent.y - 4, agent.x + 4, agent.y + 4, fill = color, outline = "")

    def update_simulation_loop(self):
        #логика шаков, обновление таймера 
        if not self.is_running:
            return

        #движение агентов 
        self.sim.update(self.current_step, self.width, self.height)
        
        #проверка на столкновение 
        for agent in self.sim.agents:
            if agent.is_alive:
                if self.obstacle[0] <= agent.x <= self.obstacle[2] and self.obstacle[1] <= agent.y <= self.obstacle[3]:
                    agent.is_alive = False

        #обновление графики
        self.redraw_screen()
        self.current_step += 1
        
        #как достигаем 300 шагов, то естественный отбор
        if self.current_step >= 300:
            self.sim.make_new_generation(self.target_x, self.target_y, mutation_rate=self.mutation_rate)
            self.current_step = 0
            self.ui.label_gen.configure (text = "Generation: " + str(self.sim.generation))
        
        #обновление таймера каждые 20 сек
        self.window.after(20, self.update_simulation_loop)

    def start_button_clicked(self):
        #клик на start/stop
        if not self.is_running:
            self.is_running = True
            self.ui.btn_start.configure(text = "Stop", fg_color = "red")
            self.update_simulation_loop()
        else:
            self.is_running = False
            self.ui.btn_start.configure(text = "Start", fg_color = "green")

    def apply_settings_clicked(self):
        
        self.ui.label_error.configure(text="")
        
        try:
            # Парсим популяцию
            raw_pop = self.ui.entry_pop.get()
            new_pop = int(raw_pop)
            if new_pop < 2 or new_pop > 200:
                raise ValueError("The population should be from 2 to 200")

            # переводим в другой формат и проверяем
            raw_mut = self.ui.entry_mut.get()
            new_mut = float(raw_mut)
            if new_mut < 0.0 or new_mut > 1.0:
                raise ValueError("The mutation should be from 0.0 to 1.0")

            # Если проверки прошли — перезапускается симуляция с 1 поколения
            self.pop_size = new_pop
            self.mutation_rate = new_mut
            
            self.is_running = False
            self.ui.btn_start.configure (text= "Start", fg_color = "green")
            self.current_step = 0
            self.sim = EvolutionSimulation (population_size=self.pop_size, start_x=self.start_x, start_y=self.start_y)
            self.ui.label_gen.configure(text = "Generation: 1")
            self.redraw_screen()
            
            self.ui.label_error.configure(text= "Settings apply", text_color = "#2ecc71")

        except ValueError as e:
            error_message = str(e)
            if "invalid literal" in error_message:
                error_message = "Enter only numbers"
            self.ui.label_error.configure(text = error_message, text_color = "#e74c3c")

    def run(self):
        self.window.mainloop()

# Запуск программы
if __name__ == "__main__":
    app = EvolutionApp()
    app.run()