import networkx as nx
import matplotlib.pyplot as plt

import time

def krasskalMethod(R):
    start = time.time()  ## точка отсчета времени
    # Красскал подготовка

    Rs = sorted(R, key=lambda x: x[0]) # сортировка по весам ребра
    U = set() # множество соединеных вершин
    D = {} # словарь изолированных групп вершин
    T = [] # список ребер остова

    # Красскал первый этап
    for r in Rs:
        if r[1] not in U or r[2] not in U:  # проверка для исключения циклов в остове
            if r[1] not in U and r[2] not in U: # если обе вершины не соединены, то
                D[r[1]] = [r[1], r[2]]          # формируем в словаре ключ с номерами вершин
                D[r[2]] = D[r[1]]               # и связываем их с одним и тем же списком вершин
            else:
                if not D.get(r[1]):             # если в словаре нет первой вершины, то
                    D[r[2]].append(r[1])        # добавляем в список первую вершину
                    D[r[1]] = D[r[2]]           # и добавляем ключ с номером первой вершины
                else:
                    D[r[1]].append(r[2])        # иначе, все то же самое делаем со второй вершиной
                    D[r[2]] = D[r[1]]

            T.append(r)             # добавляем ребро в остов
            U.add(r[1])             # добавляем вершины в множество U
            U.add(r[2])

    # Красскал второй этап
    for r in Rs:    # проходим по ребрам второй раз и объединяем разрозненные группы вершин
        if r[2] not in D[r[1]]:     # если вершины принадлежат разным группам, то объединяем
            T.append(r)             # добавляем ребро в остов
            gr1 = D[r[1]]
            D[r[1]] += D[r[2]]      # объединем списки двух групп вершин
            D[r[2]] += gr1

    end = time.time() - start  ## время работы программы
    print("Время работы: {} ms".format(end))  ## вывод времени
    return T


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

        for i in range(0, len(listOfNodes)):
            curNodeKol = listOfNodes[i]
            for j in range(0, len(listOfNodes)):
                curNodeRaw = listOfNodes[j]
                for item in R:
                    if (item[1] == curNodeRaw) and (item[2] == curNodeKol):
                        matrixFirstGraph[i][j] = item[0]

    #Вывод матрицы
    strForShowMatrix = "\t"
    for node in listOfNodes:
        strForShowMatrix += "{}\t".format(node)
    print(matrixFirstGraph)
    print(strForShowMatrix)

    weightGraph = 0
    for i in range(0, len(listOfNodes)):
        str = "\t"
        for j in range(0, len(listOfNodes)):
            weightGraph += int(matrixFirstGraph[i][j])
            str += "{}\t".format(matrixFirstGraph[i][j])
        print(listOfNodes[i],str)
    print("Вес графа: {}".format(weightGraph // 2))

G = nx.Graph()
graph = {}
R = []

with open("input.txt", "r") as file:
    for line in file:
        if len(line) != 0:

            if len(line) > 2:
                fromNode = line[0]
                toNode = line[5]
                str = ""
                for i in range(7, len(line)):
                    str += line[i]
                G.add_edge(fromNode, toNode, weight=str)

                R.append((int(str),fromNode,toNode))

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

print("Матрица смежности первого графа:")
showMatrix(listOfNodes,R)

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

#получаем остов
T = krasskalMethod(R)

#список вершин остова
listOfNodes2 = []
for item in T:
    if item[1] not in listOfNodes2:
        listOfNodes2.append(item[1])
    if item[2] not in listOfNodes2:
        listOfNodes2.append(item[2])

print("\nМатрица смежности остова:")
showMatrix(listOfNodes2,T)
newG = nx.Graph()


for r in T:
    newG.add_edge(r[1],r[2],weight=r[0])


# Визуализация остова
# Определение позиций узлов
pos = nx.spring_layout(newG)

# Получение весов ребер
edge_labels = nx.get_edge_attributes(newG, 'weight')

plt.figure("Минимальный остов")
nx.draw_networkx_nodes(newG, pos)
nx.draw_networkx_edges(newG, pos)
nx.draw_networkx_edge_labels(newG, pos, edge_labels=edge_labels)
nx.draw_networkx_labels(newG, pos)

plt.show()

