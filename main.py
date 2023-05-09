import os
import csv
import datetime
import requests
from jinja2 import Environment, FileSystemLoader


def LoadCSV(directory, filename):
    url = "https://raw.githubusercontent.com/ddm999/gt7info/web-new/_data/"
    urlData = requests.get(url+directory+filename).content
    data = []

    with open(filename, mode="wb") as f:  # wb でバイト型を書き込める
        f.write(urlData)

    with open(filename) as f:
        for row in csv.reader(f):
            data.append(row)

    os.remove(filename)

    return data


def MakeNewCarList(data, carList, makerList):
    res = []
    for i in range(len(data)):
        if data[i][2] == "new":
            for j in range(len(carList)):
                if data[i][0] == carList[j][0]:
                    for k in range(len(makerList)):
                        if carList[j][2] == makerList[k][0]:
                            makername = makerList[k][1]
                            carname = carList[j][1]
                            price = format(int(data[i][1]), ",")
                            price_in_jpy = format(int(data[i][1])*100, ",")

                            try:
                                carYear = int(carname[-2:])
                                if carYear >= 29 or carYear == 0:
                                    isOld = True
                                else:
                                    isOld = False
                            except:
                                isOld = None

                            res.append(
                                {"makername": makername, "carname": carname, "price": price, "price_in_jpy": price_in_jpy, "isOld": isOld})
    return res


def PrintNewCarList(new_car_list):
    for car in new_car_list:
        makername = car["makername"]
        carname = car["carname"]
        price_in_jpy = car["price_in_jpy"]

        message = f"{makername}{carname}{price_in_jpy}"
        print(message)

    if len(new_car_list) == 0:
        print("No new cars available.")

    print()


carList = LoadCSV("db/", "cars.csv")
makerList = LoadCSV("db/", "maker.csv")
today = datetime.datetime.utcnow().date()
start_date = datetime.date(year=2022,month=3,day=3)

# how_many_days = (today-start_date).days + 1
how_many_days = 10
data = []

for i in range(how_many_days):
    date_to_import = today - datetime.timedelta(i)
    filename = date_to_import.strftime("%y-%m-%d")+".csv"

    data_used = LoadCSV("used/", filename)
    data_legend = LoadCSV("legend/", filename)

    list_used = MakeNewCarList(data_used, carList, makerList)
    list_legend = MakeNewCarList(data_legend, carList, makerList)

    data.append({
        # "%Y/%-m/%-d"
        "date": date_to_import.strftime("%Y/%m/%d"),
        "list_used": list_used,
        "list_legend": list_legend,
    })

#テンプレート読み込み
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.tpl')

#レンダリングして出力
rendered = template.render({"data": data})
print(rendered)
# print(data)
 
# html出力
with open('result.html', 'w') as f:
    f.write(rendered)
