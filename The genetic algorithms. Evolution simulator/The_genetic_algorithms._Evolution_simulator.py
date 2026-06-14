import customtkinter as ctk
from simulation import EvolutionSimulation
from ui_stuff import UiStaff
from wavemethod import find_wave_way

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
        self.pop_size = 100
        self.mutation_rate = 0.15
        self.record_fitness = -999999
        #показывать ли путь волны
        self.show_path = True

        # Инициализируем логику толпы ботов
        self.sim = EvolutionSimulation (population_size=self.pop_size, start_x=self.start_x, start_y=self.start_y, target_x = self.target_x, target_y = self.target_y)
        self.current_step = 0
        self.is_running = False

        # Создаем окно базы
        self.window = ctk.CTk()
        self.window.title("Simulator evolution AI")
        self.window.geometry("1050x650")
        self.window.resizable(False, False)

        #инициализируем графику
        self.ui = UiStaff (self.window, self.width, self.height, start_callback = self.start_button_clicked,
                           settings_callback = self.apply_settings_clicked, restart_callback = self.restart_clicked,
                           exit_callback = self.window.destroy, show_path_callback = self.toggle_path_clicked)
        
        #вызов волного метода один раз при старте приложения
        self.ideal_path = find_wave_way ((self.start_x, self.start_y), (self.target_x, self.target_y), self.width, self.height, self.obstacle)
        # Отрисовываем первый стартовый кадр
        self.redraw_screen()

    def redraw_screen(self):
        #отрсовка объектов на экране
        self.ui.canvas.delete("all")
        
        #если путь найдем, то рисуем его 
        if self.ideal_path and self.show_path:
            for point in self.ideal_path:
                px, py = point
                #рисуем маленькую точку
                self.ui.canvas.create_oval (px - 2, py - 2, px + 2, py + 2, fill = "#009e8e", outline = "")

        # Старт и Финиш
        self.ui.canvas.create_oval (self.target_x - 15, self.target_y - 15, self.target_x + 15, self.target_y + 15, fill = "green", outline = "")
        self.ui.canvas.create_oval (self.start_x - 10, self.start_y - 10, self.start_x + 10, self.start_y + 10, fill = "blue", outline = "")
        
        # Стена
        self.ui.canvas.create_rectangle (self.obstacle[0], self.obstacle[1], self.obstacle[2], self.obstacle[3], fill = "#e74c3c", outline = "")
        
        #точки агенты: фиолетовые - живые, серые - нет
        for agent in self.sim.agents:
            if agent.is_alive:
                color = "violet"
            else:
                color = "grey"
            self.ui.canvas.create_oval(agent.x - 4, agent.y - 4, agent.x + 4, agent.y + 4, fill = color, outline = "")

        #обновление инфо панели 
        alive_count = sum( 1 for a in self.sim.agents if a.is_alive)
        best = max(agent.success for agent in self.sim.agents)

        self.ui.update_info(self.sim.generation, best, self.record_fitness, 
                            alive_count, self.pop_size, self.is_running)

    def update_simulation_loop(self):
        #логика шагов, обновление таймера 
        if not self.is_running:
            return

        #движение агентов 
        self.sim.update(self.current_step, self.width, self.height)

        #считаем каждый успех кадр для инф панели
        for agent in self.sim.agents:
            agent.count_success(self.target_x, self.target_y)
        
        #проверка на столкновение 
        for agent in self.sim.agents:
            if agent.is_alive:
                if self.obstacle[0] <= agent.x <= self.obstacle[2] and self.obstacle[1] <= agent.y <= self.obstacle[3]:
                    agent.is_alive = False
                    agent.collided = True

        #обновление графики
        self.redraw_screen()
        self.current_step += 1
        
        if self.current_step >= 1500:
            self.is_running = False
        
        #как достигаем 600 шагов, то естественный отбор
            if hasattr (self, "after_id"):
                self.window.after_cancel(self.after_id)

                self.current_step = 0
                self.sim.make_new_generation (self.target_x, self.target_y, mutation_rate = self.mutation_rate)

                #обновление рекорда 
                best = max(agent.success for agent in self.sim.agents)
                if best > self.record_fitness:
                    self.record_fitness = best

                self.ui.set_btn_start_text("Start", "green")
                self.is_running = True

        if self.is_running:
            self.after_id = self.window.after (20, self.update_simulation_loop)

    def start_button_clicked(self):
        #клик на start/stop
        if not self.is_running:
            self.is_running = True
            self.ui.set_btn_start_text("Stop", "red")
            self.update_simulation_loop()
        else:
            self.is_running = False
            self.ui.set_btn_start_text("Start", "green")

            if hasattr (self, 'after_if'):
                self.window.after_cancel (self.after_id)
            self.redraw_screen()
    
    #реализация перезапуска
    def restart_clicked(self):
        #полный сброс симуляции
        self.is_running = False
        self.current_step = 0
        self.record_fitness = 0

        if hasattr (self, "after_id"):
            self.window.after_cancel (self.after_id)

        self.sim = EvolutionSimulation (population_size = self.pop_size, start_x = self.start_x,
                                       start_y = self.start_y, target_x = self.target_x , target_y = self.target_y)
        self.ui.set_btn_start_text ("Start", "green")
        self.redraw_screen()
    
    #включение/выключение волнового метода 
    def toggle_path_clicked(self):
        self.show_path = not self.show_path

        if self.show_path:
            self.ui.btn_show_path.configure (text = "Hide path")
        else:
            self.ui.btn_show_path.configure (text = "Show path")
        self.redraw_screen()
    
    #применение настроек и запуск
    def apply_settings_clicked(self):
        
        self.ui.label_error.configure(text = "")
        
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
            
            self.restart_clicked()
            
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