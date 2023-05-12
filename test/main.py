from pulp import *

def inputAuto():
    global warehouses
    global supply
    global projects
    global demand
    global costs

    warehouses = ["a1", "a2", "a3"]

    supply = {"a1": 150, "a2": 320, "a3": 400}

    projects = ["b1", "b2", "b3", "b4", "b5"]

    demand = {
        "b1": 100,
        "b2": 120,
        "b3": 100,
        "b4": 200,
        "b5": 300,
    }


    costs = [
        [2, 5, 3, 6, 1],  # Производители
        [1, 1, 4, 4, 2],
        [4, 1, 2, 3, 5]
    ]  # Потребители


def inputFromKeyboard():
    global warehouses
    global supply
    global projects
    global demand
    global costs


    countOfWareHouses = int(input("Введите кол-во производителей (ai): "))

    for i in range(countOfWareHouses):
        warehouses.append("a" + str((i + 1)))

    countOfprojects = int(input("Введите кол-во потребителей (bi): "))

    for i in range(countOfprojects):
        projects.append("b" + str((i + 1)))

    for ware in warehouses:
        supply[ware] = int(input("Введите кол-во единиц продукции для {} :".format(ware)))

    for proj in projects:
        demand[proj] = int(input("Введите кол-во единиц продукции для {} :".format(proj)))

    costs = [[0 for j in range(len(projects))] for i in range(len(warehouses))]
    for i in range(len(warehouses)):
        for j in range(len(projects)):
            costs[i][j] = int(input("Введите цену стоимости перевозок для {}{} :".format(i, j)))

# Вывод результатов решения
def outputResult():
    print("{:<10}".format("ai/bi"),end="")
    for proj in projects:
        print("{:<10}".format(proj), end="")

    print()
    a = 0
    ware = 0
    print("{:<10}".format(warehouses[ware]), end="")
    for v in prob.variables():
        if a != len(projects) :
            print("{:<10}".format(v.varValue), end="")
            a += 1
        else:
            print()
            if ware != len(warehouses) - 1:
                ware += 1
                print("{:<10}".format(warehouses[ware]), end="")
                a = 1
                print("{:<10}".format(v.varValue), end="")




def makeCloseTask():
    global warehouses
    global supply
    global projects
    global demand
    global costs

    supSum = 0
    demSum = 0
    for v in supply.values():
        supSum += v
    for v in demand.values():
        demSum += v

    if supSum == demSum:
        print("Задача закрытого типа!")
    if supSum < demSum:
        print("Задача открытого типа. Делаем закрытой!")
        warehouses.append("a{}".format(len(supply.keys())+1))
        supply["a{}".format(len(supply.keys())+1)] = demSum - supSum
        bufArray = []
        for dem in demand:
            bufArray.append(0)
        costs.append(bufArray)
        print("Добавлен производитель с единицой {}. Задача стала закрытой".format(demSum - supSum))
    if demSum < supSum:
        print("Задача открытого типа. Делаем закрытой!")
        projects.append("b{}".format(len(demand.keys()) + 1))
        demand["b{}".format(len(demand.keys()) + 1)] = supSum - demSum
        bufArray = []
        for sup in supply:
            bufArray.append(0)
        for i in range(len(costs)):
            costs[i].append(0)
        print("Добавлен покупатель с единицой {}. Задача стала закрытой".format(supSum - demSum))


# Создание объекта задачи
prob = LpProblem("Transportation Problem", LpMinimize)
warehouses = [] # производители
supply = {} # единицы производителей
projects = [] # покупатели
demand = {} # единицы покупателей
costs = [] # стоимость перевозок

#inputFromKeyboard()
inputAuto()
makeCloseTask()
# Создание словаря стоимостей перевозок
costs = makeDict([warehouses, projects], costs, 0)

# Создание переменных решения - количество единиц продукции, перевозимых из каждого производителя в каждого потребителя
route_vars = LpVariable.dicts("Route", (warehouses, projects), 0, None, LpInteger)

# Определение функции целевой функции
prob += lpSum([route_vars[w][b] * costs[w][b] for w in warehouses for b in projects])

# Определение ограничений максимальной поставки продукции для каждого производителя
for w in warehouses:
    prob += lpSum([route_vars[w][b] for b in projects]) <= supply[w]

# Определение ограничений минимальной потребности продукции для каждого потребителя
for b in projects:
    prob += lpSum([route_vars[w][b] for w in warehouses]) >= demand[b]

# Решение задачи
prob.solve()

# вывод результата в виде таблицы
print("Последня таблица:")
outputResult()

#Вывод итогового результата
print("\n\nИтоговая матрица:")
a = 0
ware = 0
for v in prob.variables():
    if a != len(projects) :
        print("{:<10}".format(v.varValue), end="")
        a += 1
    else:
        print()
        if ware != len(warehouses) - 1:
            ware += 1
            a = 1
            print("{:<10}".format(v.varValue), end="")


print("\n\nИтоговый результат = ", value(prob.objective))