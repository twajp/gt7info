import os
import csv
import datetime
import requests
from jinja2 import Environment, FileSystemLoader


def LoadCSV(directory, filename):
    url = "https://raw.githubusercontent.com/ddm999/gt7info/web-new/_data/"
    urlData = requests.get(url+directory+filename).content
    data = []

    with open(filename, mode="wb") as f:
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
                            carid = carList[j][0]
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
                                {"makername": makername, "carid": carid, "carname": carname, "price": price, "price_in_jpy": price_in_jpy, "isOld": isOld})
    return res


carList = LoadCSV("db/", "cars.csv")
makerList = LoadCSV("db/", "maker.csv")
today = datetime.datetime.utcnow().date()
# start_date = datetime.date(year=2022,month=6,day=28)
# how_many_days = (today-start_date).days + 1
how_many_days = 14
data = []

for i in range(how_many_days):
    date_to_import = today - datetime.timedelta(i)
    filename = date_to_import.strftime("%y-%m-%d")+".csv"

    data_used = LoadCSV("used/", filename)
    data_legend = LoadCSV("legend/", filename)

    list_used = MakeNewCarList(data_used, carList, makerList)
    list_legend = MakeNewCarList(data_legend, carList, makerList)

    data.append({
        "date": date_to_import.strftime("%Y/%-m/%-d"),
        "list_used": list_used,
        "list_legend": list_legend,
    })


env = Environment(loader=FileSystemLoader("."))
template = env.get_template("template.html")

rendered = template.render({"data": data, "price": "global"})
rendered_jp = template.render({"data": data, "price": "jp"})
rendered_noprice = template.render({"data": data, "price": "no"})

if not os.path.exists("html"):
    os.makedirs("html")

with open("html/index.html", "w") as f:
    f.write(rendered)

with open("html/jp.html", "w") as f:
    f.write(rendered_jp)

with open("html/noprice.html", "w") as f:
    f.write(rendered_noprice)
