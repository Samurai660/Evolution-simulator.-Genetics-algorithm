import random 
#переносим нашего агента из файла agent
from agent import Agent 

class EvolutionSimulation:
    def __init__ (self, population_size, start_x, start_y, target_x, target_y):
        self.target_x = target_x
        self.target_y = target_y
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
        #добавление счетчика ходов
        if not hasattr(self, "step_index"):
            self.step_index = 0
        #продвижение каждого агента в толпе на один шаг 
        for bot in self.agents:
            bot.move(step_index, max_width, max_height)
        self.step_index += 1
        #ключевой момент. Смерть агента
        all_dead = all (not agent.is_alive for agent in self.agents)
        #кроме смерти у них еще могут закончится ходы 
        if all_dead or self.step_index >= 300:
            self.make_new_generation(self.target_x, self.target_y)
            self.step_index = 0

    def make_new_generation(self, target_x, target_y, mutation_rate = 0.05):
        #оценка старого покаления и создание нового, более продвинутого
        
        #пусть каждый агент сам считает свой успех
        for bot in self.agents:
            bot.count_success(target_x, target_y)

        #сортировка агентов. Нужно, чтобы самые успешные были в начале 
        #сортировка для переборки списка и замена местами 
        self.agents.sort (key = lambda x: x.success, reverse = True)

        #отбираем 5 лучших агентов (родители следующего поколения)
        parents = self.agents [:3]
        #новый список для следующего поколения
        new_agents = []

        self.generation += 1
        #нужно обязательно, чтобы новое поколение начинало ходить с 0 шага
        self.step_index = 0
        #reset для нового агента
        for agent in self.agents:
            agent.reset()

        #Заполение сипска потомством до 50 
        while len(new_agents) < self.population_size:
            #выбираем двух случайных из лучших 
            p_agent = random.choice(parents)
            m_agent = random.choice(parents)

            #создаем приемника 
            child = Agent (self.start_x, self.start_y)

            #скрещиваем гены (половина от p_agent, половина от m_agent)
            seprator = len(child.genome) // 2
            child.genome = p_agent.genome[:seprator] + m_agent.genome[seprator:]

            #смешение разных геномов *мутация
            #пройдемся по всему геному и меняем команду на случайную
            for i in range (len(child.genome)):
                random_percent = random.random()
                if random_percent < mutation_rate:
                    child.genome[i] = random.randint(0, 3)

                #добавляем потомка в новое поколение
            new_agents.append(child)

        #замена предыдущего поколения на новое 
        self.agents = new_agents


    

        
