import customtkinter as ctk
import tkinter as tk  
import simulation as EvSim

#размеры экрана и позиции агента
WIDTH = 800
HEIGHT = 600

START_X = 400 #снизу по центру
START_Y = 550

TARGET_X = 400 # финиш вверху по центру 
TARGET_Y = 50

#создаем 50 ботов, стратующих снизу экрана
sim = EvSim(population_size = 50, start_x = START_X, start_y = START_Y)

#переменная, записывающая какой шаг делает поколение в данный момент 
current_step = 0

#флаг запуска симуляции в данный момент 
is_running = False

#обновление экрана по таймеру 
def update_simulation_loop():
    global current_step, is_running

    #при паузе или симуляция не проводится - ничего не делаем
    if is_running == False:
        return

    #с помощью логики передвигаем агентов на один шаг 
    sim.update(current_step, WIDTH, HEIGHT)

    #очистка экрана, перерисовка в новых координатах
    canvas.delete("all")

    #финиш как зеленый круг 
    canvas.create_oval(TARGET_X - 15, TARGET_Y - 15, TARGET_X + 15, TARGET_Y + 15, fill = "green", outline = "")
    #для старта пока возьмем синий круг. В будущем могут быть правки
    canvas.create_oval(START_X - 10, START_Y - 10, START_X + 10, START_Y + 10, fill = "blue", outline = "")

    #отрисовка агентов 
    for agent in sim.agent:
        #агент жив - фиолетовый, в противном случае серый 
        if agent.is_alive:
            colot = "violet"
        else:
            color = "grey"

    #теперь точка агента
    canvas.create_oval (agent.x - 4, agent.y - 4, agent.x + 4, agent.y + 4, fill = color, outline = "")

    #следующий шаг генома 
    current_step = current_step + 1

    #флаг для всех 300 шагов. после этого поколение заканичвает путь 
    if current_step >= 300:
        #отбор лучших, создание нового поколения 
        sim.make_new_generation(TARGET_X, START_Y, mutation_rate = 0.05)

        #сброс счетчика шагов 
        current_step = 0

        #обновления вывода экрана. указание нового поколения 
        label_gen.configure (text = "Generation: " + str(sim.generation))

    #цикл таймера через каждые 20 сек пока что 
    window.after(20, update_simulation_loop)

