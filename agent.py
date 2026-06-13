import random

class Agent:
    def __init__(self, start_x, start_y, genome_size = 300):
        #флаг стартовой позиции
        self.start_x = start_x
        self.start_y = start_y

        #текущие координты, меняющиеся при передвижении
        self.x = start_x
        self.y = start_y

        #оценка бота и статус жизни

        self.success = 0.0
        self.is_alive = True

        #создаем пустой список для генома 
        self.genome = []

        # по очередно 300 раз кидаем случайное число и переносим в список 
        for i in range(genome_size):
            random_step = random.randint(0,3) # 0 - вверх, 1 - вправо, 2 - вниз, 3 - влево
            self.genome.append(random_step)

def reset(self):
    #возращаем агента на старт перед новым поколением 
    self.x = self.start_x
    self.y = self.start_y
    self.is_alive = True

def move(self, step_index, max_width, max_height):
    #делаем один шаг по команде из генома 
    if self.is_alive == False:
        return

    #защита при условии кончившихся шагов
    if step_index >= len(self.genome):
        return
    #берем команду под нужным номером 
    command = self.genome[step_index]
    step_size = 5 #сколько пикселей за шаг проходится

    #двигаем точку в зависимости от команды
    if command == 0:
        self.y = self.y - step_size
    elif command == 1:
        self.x = self.x + step_size
    elif command == 2:
        self.y = self.y + step_size
    elif command == 3:
        self.x = self.x - step_size

    #флаг если выход за границы экрана - смерть
    if self.x < 0 or self.x > max_width or self.y < 0 or self.y > max_height:
        self.is_alive = False

def count_success (self, target_x, targe_y):
    #расстояние до финиша
    distance = ((target_x - self.x) ** 2 + (targe_y - self.y) ** 2) ** 0.5

    #проверка для идеального прохода агента
    if distance == 0:
        self.success == 10000.0
    else:
        #чем меньше расстояние, тем больше число успеха
        self.success = 1.0 / distance