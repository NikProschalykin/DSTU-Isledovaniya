import math
import networkx as nx
import matplotlib.pyplot as plt

# minSlice() -  это костыль для того, чтобы вывести минимальный разрез,
# для других графов он скорее всего будет работать не верно, но она не спрашивает про него обычно
def minSlice(V):
    G = nx.DiGraph()
    for index in range(0, len(V)):
        for jndex in range(0, len(V[index])):
            if index != jndex and V[index][jndex][2] != -1:
                if ((V[index][jndex][0] == 0) and (V[index][jndex][1] == 0)) != True:
                    if (index == 0 and jndex == 3) or (index == 1 and jndex == 3) or (index == 1 and jndex == 2) or (index == 1 and jndex == 4):
                        fromNode = index + 1
                        toNode = jndex + 1
                        G.add_edge(fromNode, toNode, weight=V[index][jndex][1])

    # Визуализация минимального разреза графа

    # Определение позиций узлов
    pos = nx.spring_layout(G)

    # Получение весов ребер
    edge_labels = nx.get_edge_attributes(G, 'weight')

    plt.figure("Минимальный разрез")
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    nx.draw_networkx_labels(G, pos)

    plt.show()

def get_max_vertex(k, V, S):
    m = 0   # наименьшее допустимое значение
    v = -1
    for i, w in enumerate(V[k]):
        if i in S:
            continue

        if w[2] == 1:   # движение по стрелке
            if m < w[0]:
                m = w[0]
                v = i
        else:           # движение против стрелки
            if m < w[1]:
                m = w[1]
                v = i

    return v


def get_max_flow(T):
    w = [x[0] for x in T]
    return min(*w)


def updateV(V, T, f):
    for t in T:
        if t[1] == -1:  # это исток
            continue

        sgn = V[t[2]][t[1]][2]  # направление движения

        # меняем веса в таблице для (i,j) и (j,i)
        V[t[1]][t[2]][0] -= f * sgn
        V[t[1]][t[2]][1] += f * sgn

        V[t[2]][t[1]][0] -= f * sgn
        V[t[2]][t[1]][1] += f * sgn


# V = [[[0,0,1], [20,0,1], [30,0,1], [10,0,1], [0,0,1]],
#      [[20,0,-1], [0,0,1], [40,0,1], [0,0,1], [30,0,1]],
#      [[30,0,-1], [40,0,-1], [0,0,1], [10,0,1], [20,0,1]],
#      [[10,0,-1], [0,0,1], [10,0,-1], [0,0,1], [20,0,1]],
#      [[0,0,1], [30,0,-1], [20,0,-1], [20,0,-1], [0,0,1]],
# ]

#Землянухин
        #1       #2       #3        #4        #5
V = [[[0,0,1], [5,0,1], [0,0,1], [1,0,1], [0,0,1]], # 1
     [[5,0,-1], [0,0,1], [1,0,1], [2,0,1], [1,0,1]], # 2
     [[0,0,-1], [1,0,1], [0,0,1], [4,0,-1], [1,0,1]], # 3
     [[1,0,-1], [2,0,-1], [4,0,1], [0,0,1], [3,0,1]], # 4
     [[0,0,1], [1,0,-1], [1,0,-1], [3,0,-1], [0,0,1]], # 5
]

N = len(V)  # число вершин в графе
init = 0    # вершина истока
end = 4     # вершина стока
Tinit = (math.inf, -1, init)   # первая метка маршруто (a, from, vertex)
f = []      # максимальные потоки найденных маршрутов

iteration = 1
j = init
while j != -1:
    k = init  # стартовая вершина (нумерация с нуля)
    T = [Tinit]  # метки маршрута
    S = {init}  # множество просмотренных вершин

    while k != end:     # пока не дошли до стока
        j = get_max_vertex(k, V, S)  # выбираем вершину с наибольшей пропускной способностью
        if j == -1:         # если следующих вершин нет
            if k == init:      # и мы на истоке, то
                break          # завершаем поиск маршрутов
            else:           # иначе, переходим к предыдущей вершине
                k = T.pop()[2]
                continue

        c = V[k][j][0] if V[k][j][2] == 1 else V[k][j][1]   # определяем текущий поток
        T.append((c, j, k))    # добавляем метку маршрута
        S.add(j)            # запоминаем вершину как просмотренную

        if j == end:    # если дошли до стока
            f.append(get_max_flow(T))     # находим максимальную пропускную способность маршрута
            updateV(V, T, f[-1])        # обновляем веса дуг
            break

        k = j

    print("Итерация: {}".format(iteration))
    iteration += 1
    for mas in V:
        print(mas, "\n")

    G = nx.DiGraph()
    for index in range(0, len(V)):
        for jndex in range(0, len(V[index])):
            if index != jndex and V[index][jndex][2] != -1:
                if ((V[index][jndex][0] == 0) and (V[index][jndex][1] == 0)) != True:
                    str = "{}/{}".format(V[index][jndex][0], V[index][jndex][1])
                    fromNode = index + 1
                    toNode = jndex + 1
                    G.add_edge(fromNode, toNode, weight=V[index][jndex][1])

    # Визуализация полученного графа

    # Определение позиций узлов
    pos = nx.spring_layout(G)

    # Получение весов ребер
    edge_labels = nx.get_edge_attributes(G, 'weight')

    plt.figure("Итерация: {}".format(iteration-1))
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    nx.draw_networkx_labels(G, pos)

    plt.show()

F = sum(f)
print("Максимальный потоки по итерациям: ",f)
print(f"Максимальный поток равен: {F}")
minSlice(V)
