from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def cash_rest():
    rest = pd.read_excel('table.xlsx', skiprows=3, index_col=1, sheet_name='Склад_остатки')
    price = pd.read_excel('table.xlsx', index_col=1, sheet_name='справочник_товаров')
    rest = pd.merge(rest, price, how='left', on='Наименование товара')
    rest['total'] = rest['Стоимость'] * rest['Остаток на складе']
    total_rest = round(rest['total'].sum())
    return total_rest

def rest_of_good(id):
    rest = pd.read_excel('table.xlsx', skiprows=3, sheet_name='Склад_остатки')
    price = pd.read_excel('table.xlsx', sheet_name='справочник_товаров')
    rest = pd.merge(rest, price, how='left', on='Наименование товара')
    rest['total'] = rest['Стоимость'] * rest['Остаток на складе']
    res = rest.loc[rest['артикул_y'] == id]
    if rest.empty == True:
        s = "Нет товара с таким артикулом"
    elif res['Остаток на складе'].empty:
        s = "Остатоков этого товара нет на складе"
    else:
        s1 = f"{res['Наименование товара']}"
        n = s1[5:(s1.find("\n"))]
        s2 = f"{res['Остаток на складе']}"
        count = s2[5:(s2.find("\n"))]
        s3 = f"{res['total']}"
        cost = s3[5:(s3.find("\n"))]
        s = f'{n} \t{count} штук\t{cost} рублей'
    return s

def rest_of_controllers():
    rest = pd.read_excel('table.xlsx', skiprows=3, index_col=False, sheet_name='Склад_остатки')
    res = rest.loc[(rest['Наименование товара'].str.contains("Контроллер |контроллер "))]
    res = res[['Наименование товара', 'Остаток на складе']]
    res = res.groupby(['Наименование товара'], as_index=False, sort=False).agg('sum')
    name = res['Наименование товара'].to_frame()
    count = res['Остаток на складе'].to_frame()
    s = ""
    for i in range(0, name['Наименование товара'].count()):
        if np.isnan(count['Остаток на складе'][i]) or count['Остаток на складе'][i] == 0:
            continue
        else:
            s += f"{name['Наименование товара'][i]} {count['Остаток на складе'][i]} штук\n"
    if s == "":
        return "Нет остатков контроллеров на складе"
    return s

def shipments(n):
    warehouse_move = pd.read_excel('table.xlsx', sheet_name='Движение_склад')
    price = pd.read_excel('table.xlsx', sheet_name='справочник_товаров')
    if n == 0:
        warehouse_move = warehouse_move[ datetime.today() - pd.to_datetime(warehouse_move['Дата']) <= timedelta(days=7)]
    elif n == 1:
        warehouse_move = warehouse_move[warehouse_move['Дата'].dt.month == datetime.now().month]
    warehouse_move = pd.merge(warehouse_move, price, how='left', on='Наименование товара')
    warehouse_move['sum'] = warehouse_move['Стоимость'] * warehouse_move['Расход кол-во']
    res = warehouse_move[['Наименование товара', 'Расход кол-во', 'sum']]
    res = res.groupby(['Наименование товара'], as_index=False, sort=False).agg('sum')
    name = res['Наименование товара'].to_frame()
    count = res['Расход кол-во'].to_frame()
    cost = res['sum'].to_frame()
    s = ""
    for i in range(0, name['Наименование товара'].count()):
        if np.isnan(count['Расход кол-во'][i]) or count['Расход кол-во'][i] == 0:
            continue
        else:
            s += f"{name['Наименование товара'][i]} {count['Расход кол-во'][i]} штук {cost['sum'][i]} рублей\n"
    if s == "":
        return "Нет отгрузок за данный период времени"
    return s

def delivery(n):
    warehouse_move = pd.read_excel('table.xlsx', sheet_name='Движение_склад')
    if n == 0:
        warehouse_move = warehouse_move[ datetime.today() - pd.to_datetime(warehouse_move['Дата']) <= timedelta(days=7)]
    elif n == 1:
        warehouse_move = warehouse_move[warehouse_move['Дата'].dt.month == datetime.now().month]
    price = pd.read_excel('table.xlsx', sheet_name='справочник_товаров')
    warehouse_move = pd.merge(warehouse_move, price, how='left', on='Наименование товара')
    warehouse_move['sum'] = warehouse_move['Стоимость'] * warehouse_move['Приход кол-во']
    res = warehouse_move[['Наименование товара', 'Приход кол-во', 'sum']]
    res = res.groupby(['Наименование товара'], as_index=False, sort=False).agg('sum')
    name = res['Наименование товара'].to_frame()
    count = res['Приход кол-во'].to_frame()
    cost = res['sum'].to_frame()
    s = ""
    for i in range(0, name['Наименование товара'].count()):
        if np.isnan(count['Приход кол-во'][i]) or count['Приход кол-во'][i] == 0:
            continue
        else:
            s += f"{name['Наименование товара'][i]} {count['Приход кол-во'][i]} штук {cost['sum'][i]} рублей\n"
    if s == "":
        return "Нет поступлений за данный период времени"
    return s