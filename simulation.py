import random 
#переносим нашего агента из файла agent
from agent import Agent 

class EvolutionSimulation:
    def __init__ (self, population_size, start_x, start_y):
        self.population_size = population_size
        self.start_x = start_x
        self.start_y = start_y

        #счетчик поколений
        self.generation = 1

        #пустой список для группы ботов
        self.agents = []

        #заполним его новыми агентами
        for i in range(population_size):
            new_bot = Agent(start_x, start_y)
            self.agents.append(new_bot)

    def update (self, step_index, max_width, max_height):
        #продвижение каждого агента в толпе на один шаг 
        for bot in self.agents:
            bot.move(step_index, max_width, max_height)

    def make_new_generation(self, target_x, target_y, mutation_rate = 0.05):
        #оценка старого покаления и создание нового, более продвинутого
        
        #пусть каждый агент сам считает свой успех
        for bot in self.agents:
            bot.calculate_success(target_x, target_y)

        #сортировка агентов. Нужно, чтобы самые успешные были в начале 
        #сортировка для переборки списка и замена местами 
        self.agents.sort (key = lambda x: x.success, reverse = True)

        #отбираем 5 лучших агентов (родители следующего поколения)
        parents = self.agents [:5]
        #новый список для следующего поколения
        new_agents = []

        #Заполение сипска потомством до 50 
        while len(new_agents) < self.population_size:
            #выбираем двух случайных из лучших 
            p_agent = random.choice(parents)
            m_agent = random.choice(parents)

            #создаем приемника 
            child = Agnet (self.start_x, self.start_y)

            #скрещиваем гены (половина от p_agent, половина от m_agent)
            seprator = len(child.genome) // 2
            child.genome = p_agent.genome[:seprator] + m_agent.genome[seprator:]

            #смешение разных геномов *мутация
            #пройдемся по всему геному и меняем команду на случайную
            for i in range (len(child.genome)):
                random_percent = random.random()
                if random_percent < mutation_rate:
                    child.genome[i] = random = random.randint(0, 3)

                #добавляем потомка в новое поколение
            new_agents.append(child)

        #замена предыдущего поколения на новое 
        self.agents = new_agents

        #увеличиваем номер поколения +1
        self.generation = self.generation + 1

        
