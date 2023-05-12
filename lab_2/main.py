import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue

graph = {}
isGraphOrientired = True
filename = ""

while True:
    graphInfo = input("Введите какой хотите выбрать граф(1 - ориентированный; 2 - не ориентированный): ")
    if graphInfo == '1':
        filename = "OrientedGraph.txt"
        G = nx.DiGraph()
        isGraphOrientired = True
        break
    elif graphInfo == '2':
        filename = "NonOrientedGraph.txt"
        G = nx.Graph()
        isGraphOrientired = False
        break
    else:
        print("Вы ввели неверный код. Повторите попытку")



with open(filename, "r") as file:
    for line in file:
        if len(line) != 0:
            if len(line) > 2:
                fromNode = line[0]
                toNode = line[5]
                G.add_edge(fromNode,toNode)
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

listOfNodes = []
print("Список смежности:")
for key in graph.keys():
    print("{} : {}".format(key,graph[key]))
    listOfNodes.append(key)


def bfs(graph, start):

    for i in range(0, len(listOfNodes)):
        numLevel.append(-1)
    visited = set()  # Множество посещенных вершин
    queue = Queue()  # Очередь вершин, которые нужно посетить
    preds = {}  # Словарь предшественников каждой вершины

    visited.add(start)  # Помещаем начальную вершину в множество посещенных
    queue.put(start)  # Помещаем начальную вершину в очередь

    while len(visited) != len(listOfNodes):
        if len(visited) == 1: True
        else:
            for node in listOfNodes:
                if node not in visited:
                    visited.add(node)
                    queue.put(node)
                    break
        while not queue.empty():
            vertex = queue.get()  # Извлекаем вершину из очереди
            # Обходим все соседние вершины
            for neighbor in graph[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)  # Помечаем соседнюю вершину как посещенную
                    queue.put(neighbor)  # Добавляем соседнюю вершину в очередь
                    preds[neighbor] = vertex # Сохраняем предшественника соседней вершины
                    if numLevel[int(neighbor) - 1] == -1:
                        numLevel[int(neighbor) - 1] = numLevel[int(vertex) - 1] + 1 #сохранение уровня

    for i in range(0,len(numLevel)):
        numLevel[i] += 1
    return preds

numLevel = []
startNode = input("Введите начальную вершину: ")
preds = bfs(graph,startNode)
result = set(preds.keys())  # Множество всех вершин, до которых можно добраться
result.add(startNode)  # Добавляем начальную вершину


print("Вершины, в которые есть пути из {}:".format(startNode))
strResult = ""
for node in result:
    if node != startNode:
        strResult += "{} ".format(node)
print(strResult)


# дерево поиска
if isGraphOrientired:
    T = nx.DiGraph()
else:
    T = nx.Graph()

for node in result:
    if node in preds:
        T.add_edge(preds[node], node)


plt.figure("Изначальный граф")
nx.draw(G,with_labels=True)


# Матрица смежности дерева
print("Матрица смежности дерева поиска")
NodesInTree = []
for key in preds.keys():
    if (key not in NodesInTree):
        NodesInTree.append(key)
    if (preds[key] not in NodesInTree):
        NodesInTree.append(preds[key])


matrixOfTree = []

for i in range(0, len(NodesInTree)):
    list = []
    for j in range(0, len(NodesInTree)):
        list.append(0)
    matrixOfTree.append(list)


for key in preds.keys():
    if isGraphOrientired:
        matrixOfTree[int(preds[key])-1][int(key)-1] = 1
    else:
        matrixOfTree[int(preds[key]) - 1][int(key) - 1] = 1
        matrixOfTree[int(key) - 1][int(preds[key]) - 1] = 1

strForShowMatrix = "\t"
NodesInTree.sort()
for node in NodesInTree:
    strForShowMatrix += "{}\t".format(node)
print(strForShowMatrix)
for i in range(0, len(NodesInTree)):
    print(NodesInTree[i],end=" ")
    for j in range(0, len(NodesInTree)):
        print("\t{}".format(matrixOfTree[i][j]),end="")
    print()


#словарь предков в массив

ptrList = []
for item in listOfNodes:
    ptrList.append('0')

for i in range(0,len(listOfNodes)):
    for key in preds:
        if key == listOfNodes[i]:
            ptrList[i] = preds[key]



#Печать таблицы результата
print("\n\nКорень поиска: {}".format(startNode))

print("node:",end="")
for item in listOfNodes:
    print("\t{}".format(item),end=" ")

print("\nnum:",end="")
for item in numLevel:
    print("\t{}".format(item), end=" ")

print("\nptr:",end="")
for item in ptrList:
    print("\t{}".format(item), end=" ")

print("\n")
#Вывод дерева поиска
plt.figure("Дерево поиска")
nx.draw(T, with_labels=True)
plt.show()

