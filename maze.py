from random import choice

# поле
field = []

# клетки,которые надо посетить
need_to_visit = []

# начальные х и у
new_X_and_Y = []
# координата по оси х
now_x = 0
# и у
now_y = 0
# проденный в лабиринте путь
way = []


def create(width, height):
    global now_x, now_y, new_X_and_Y, field, need_to_visit, way
    # делаем заготовку из -1
    field = [[-1 for x in range(width)]for y in range(height)]

    # меняем, где надо, -1 на стену 0 и место, которое надо посетить на 1
    for y in range(1, len(field) - 1):
        for x in range(1, len(field[y]) - 1):
            if x % 2 != 0 and y % 2 != 0:
                field[y][x] = 1
            else:
                field[y][x] = 0

    # чистим список на всякий случай (точнее, на случай повторной генерации лабиринта)
    need_to_visit = []

    # заполняем его координатами единиц из поля
    for x in range(len(field)):
        for y in range(len(field[x])):
            if field[x][y] == 1:
                need_to_visit.append([x, y])
    del x, y

    # выбираем начальную клетку
    new_X_and_Y = choice(need_to_visit)

    # определяем х
    now_x = new_X_and_Y[0]

    # и у
    now_y = new_X_and_Y[1]

    # чистим путь
    way = []

    # удаляем начальные координаты
    need_to_visit.remove([now_x, now_y])


# получаем координаты соседей
def getNeighbors(now_x, now_y, now_field):
    # список координат соседей
    neighbors = []

    # если подходит по условию клетка, то добавляем ее в список
    # проверка работает так - рассматриваем клетки, где х или у координата больше или меньше на два
    # то есть клетка выше нынешней на одну, ниже на одну, слева  и справа через одну
    # если такая координата есть в списке тех, которые надо посетить, добавляем ее туда.
    if [now_x, now_y - 2] in need_to_visit and now_field[now_x + 1][now_y - 2] == now_field[now_x - 1][now_y - 2] == 0:
        neighbors.append([now_x, now_y - 2, 0, -1])

    if [now_x + 2, now_y] in need_to_visit and now_field[now_x + 2][now_y - 1] == now_field[now_x + 2][now_y + 1] == 0:
        neighbors.append([now_x + 2, now_y, 1, 0])

    if [now_x, now_y + 2] in need_to_visit and now_field[now_x + 1][now_y + 2] == now_field[now_x - 1][now_y + 2] == 0:
        neighbors.append([now_x, now_y + 2, 0, 1])

    if [now_x - 2, now_y] in need_to_visit and now_field[now_x - 2][now_y - 1] == now_field[now_x - 2][now_y + 1] == 0:
        neighbors.append([now_x - 2, now_y, -1, 0])

    # возвращаем в метод, создающий лабиринт координаты соседних НЕПОСЕЩЕННЫХ клеток
    return neighbors


def createMaze(width=20, height=20):
    global need_to_visit, field, now_x, now_y, way
    # создаем заготовки под лабиринт
    create(width, height)

    while len(need_to_visit) > 0:
        # получаем координаты соседей
        now_neighbors = getNeighbors(now_x, now_y, field)

        # когда остается 4 непосещенные клетки
        if len(need_to_visit) <= 4:
            # у алгоритма есть особенность - он не посещает крайние точки лабиринта
            # поэтому у них стены убираем сами
            # эта особенность создает "бахрому" по краям лабиринта
            field[2][1] = 1
            field[height - 2][2] = 1
            field[1][width - 3] = 1
            field[height - 2][width - 3] = 1

            # и чистим список для посещения - лабиринт готов
            need_to_visit = []

            continue

        # если соседи есть
        if len(now_neighbors) > 0:
            # выбираем одного из них
            new_x_y = choice(now_neighbors)

            # извлекаем будущие координаты
            new_x = new_x_y[0]
            new_y = new_x_y[1]

            # если клетка в непосещенных - удаляем ее
            need_to_visit.remove([new_x, new_y])

            # убираем стену между клеткой, на которой мы сейчас и той, куда встанем
            field[now_x + new_x_y[2]][now_y + new_x_y[3]] = 1

            # добавляем новые координаты в "путь"
            way.append([now_x, now_y])

            # обновляем данные о том, на какой мы клетке
            now_x = new_x
            now_y = new_y

        elif len(way) != 0:  # если соседей нет и можно отойти назад по пути
            # меняем нынешние координаты на предыдущие
            new = way[-1]
            now_x = new[0]
            now_y = new[1]

            # удаляем их
            way.pop(-1)
        else:  # иначе выбираем случайную клетку из непосещенных
            new = choice(need_to_visit)
            now_x = new[0]
            now_y = new[1]

    # сохраняем поле
    new_field = field

    # чистим поле
    field = []

    # возвращаем лабиринт
    return new_field

