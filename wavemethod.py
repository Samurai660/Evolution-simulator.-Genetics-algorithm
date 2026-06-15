from tkinter import CURRENT


def find_wave_way (start, target, grid_width, grid_height, obstacles):
    #Поиск кратчайшего пути методом волны
    #start: кортеж (x, y) - координаты старта 
    #target: кортеж (x, y) - координаты финиша 
    #grid_width, grid_height: размеры сетки
    #obstacles: список кортежей с стенами
    
    #очередь для клеток, которые нужно проверить. Начинаем со старта 
    queue = [start]

    #словарь, где для каждой клетки мы запомним откда мы в нее пришли 
    parent_map = {start: None}

    #множество посещенных клеток, чтобы не повторяться 
    visited = set()
    visited.add(start)

    #запуск волны
    while len(queue) > 0:
        #берем первую клетку из очереди (FIFO)
        current = queue.pop(0)
        curr_x, curr_y = current

        #если мы дошли до цели - конец
        if current == target:
            break

        #смотрим на 4 соседних направления (влево, вправо, вверх, вниз)
        neighbors = [(curr_x + 10, curr_y), #вправо
                     (curr_x - 10, curr_y), #влево
                     (curr_x, curr_y + 10), #вверх
                     (curr_x, curr_y - 10)] # вниз 
        for next_node in neighbors:
            nx, ny = next_node

            #проверка на выход за границы экрана
            if 0 <= nx < grid_width and 0 <= ny < grid_height:
                #проверка стены 
                is_wall = (obstacles[0] <= nx <= obstacles[2] and obstacles[1] <= ny <= obstacles[3])

                if not is_wall and next_node not in visited:
                    visited.add(next_node)
                    parent_map[next_node] = current
                    queue.append(next_node)


    if target not in parent_map:
        return [] #возврат пустого пути 

    #восстановление пути с конца 
    path = []
    current_step = target
    while current_step is not None:
        path.append(current_step)
        current_step = parent_map[current_step]

    #разворачиваем путь, от старта к финишу 
    path.reverse()
    return path