import math
import networkx as nx
import matplotlib.pyplot as plt

# определение ноды с наименьшим весом
def arg_min(T, S):
    amin = -1
    m = math.inf  # максимальное значение
    for i, t in enumerate(T):
        if t < m and i not in S:
            m = t
            amin = i

    return amin

def showMatrix(listOfNodes,R):
    # матрица смежности
    matrixFirstGraph = []

    for i in range(0,len(listOfNodes)):
        list = []
        for j in range(0, len(listOfNodes)):
            list.append('0')
        matrixFirstGraph.append(list)


    # заполнение матрицы смежности
    for i in range(0, len(listOfNodes)):
        curNodeRaw = listOfNodes[i]
        for j in range(0, len(listOfNodes)):
            curNodeKol = listOfNodes[j]
            for item in R:
                if (item[1] == curNodeRaw) and (item[2] == curNodeKol):
                    matrixFirstGraph[i][j] = item[0]
        # В случае неориентированного
        # for i in range(0, len(listOfNodes)):
        #     curNodeKol = listOfNodes[i]
        #     for j in range(0, len(listOfNodes)):
        #         curNodeRaw = listOfNodes[j]
        #         for item in R:
        #             if (item[1] == curNodeRaw) and (item[2] == curNodeKol):
        #                 matrixFirstGraph[i][j] = item[0]

    #Вывод матрицы
    strForShowMatrix = "\t"
    for node in listOfNodes:
        strForShowMatrix += "{}\t".format(node)
    print(strForShowMatrix)

    for i in range(0, len(listOfNodes)):
        str = "\t"
        for j in range(0, len(listOfNodes)):
            str += "{}\t".format(matrixFirstGraph[i][j])
        print(listOfNodes[i],str)

    return matrixFirstGraph

#Чтение данных из файла
R = []
graph = {}
G = nx.DiGraph()

with open("input.txt", "r") as file:
    for line in file:
        if len(line) != 0:

            if len(line) > 2:
                fromNode = line[0]
                toNode = line[5]
                str = ""
                for i in range(7, len(line)):
                    str += line[i]
                    print("type of: {}".format)
                G.add_edge(fromNode, toNode, weight=str)

                R.append((int(str),int(fromNode),int(toNode)))

                buf = []
                if line[0] in graph :
                    buf = graph[line[0]]
                    buf.append(line[5])
                    graph[line[0]] = buf
                else:
                    buf.append(line[5])
                    graph[line[0]] = buf
            else:
                graph[line[0]] = ''
                G.add_node(line[0])


#преобразование в матрицу смежности
for item in R:
    bufList = []
    if item[1] in graph:
        bufList = graph[item[1]]
        if item[2] in bufList:
            graph[item[1]] = bufList
        else:
            bufList.append(item[2])
            graph[item[1]] = bufList
    else:
        bufList.append(item[2])
        graph[item[1]] = bufList

# список вершин
listOfNodes = []

for item in R:
    if item[1] not in listOfNodes:
        listOfNodes.append(item[1])
    if item[2] not in listOfNodes:
        listOfNodes.append(item[2])

#Вывод матрицы смежности

print("Матрица смежности графа:")
D = showMatrix(listOfNodes,R)

#преобразование матрицы для работы алгоритма Дейкстры
for i in range(0,len(listOfNodes)):
    for j in range(0,len(listOfNodes)):
        if D[i][j] == '0':
            if j == i:
                D[i][j] = 0
            else:
                D[i][j] = math.inf


# Визуализация изначального графа

# Определение позиций узлов
pos = nx.spring_layout(G)

# Получение весов ребер
edge_labels = nx.get_edge_attributes(G, 'weight')

plt.figure("Изначальный граф")
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
nx.draw_networkx_labels(G, pos)


listOfDicts = []
v = 0
start = v
#Алгоритм Дейкстры

for i in range(0, len(listOfNodes)):
    dict = {}
    N = len(D)  # число вершин в графе
    T = [math.inf]*N   # последняя строка таблицы

    end = i
    v = start
    S = {v}     # просмотренные вершины
    T[v] = 0    # нулевой вес для стартовой вершины
    M = [0]*N   # оптимальные связи между вершинами

    while v != -1:
        for j, dw in enumerate(D[v]):   # перебираем все связанные вершины с вершиной v
            if j not in S:           # если вершина еще не просмотрена
                w = T[v] + dw        # формируем вес по формуле -> вес вершины + вес дуги
                if w < T[j]:
                    T[j] = w
                    M[j] = v         # связываем вершину j с вершиной v

        v = arg_min(T, S)            # выбираем следующий узел с наименьшим весом
        if v >= 0:                    # выбрана очередная вершина
            S.add(v)                 # добавляем новую вершину в рассмотрение



    # формирование оптимального маршрута:
    P = [end]
    while end != start:
        end = M[P[-1]]
        P.append(end)

    for i in range(0, len(P)):
        P[i]+=1
    P = list(reversed(P))

    for i in range(0, len(P)-1):
        dict[P[i]] = P[i+1]
    listOfDicts.append(dict)

print("Минимальное длины до других вершин из вершины {}:".format(start+1))
for i in range(0, len(listOfNodes)):
    print("До вершины {}: {}".format(listOfNodes[i],T[i]))


print(listOfDicts)
print("Списки смежности маршрутов")
for i in range(0,len(listOfDicts)):
    print("{} вершина".format(i+1), listOfDicts[i])


# Визуализация Дерева

newG = nx.DiGraph()

for dict in listOfDicts:
    for key in dict.keys():
        newG.add_edge(key,dict[key])

plt.figure("Дерево оптимального маршрута")
nx.draw(newG,with_labels=True)

plt.show()

'''

1 -> 2 2
1 -> 3 7
1 -> 4 4
1 -> 5 6
2 -> 4 1
2 -> 3 4
2 -> 5 2
4 -> 2 2
4 -> 5 1
5 -> 3 1

'''