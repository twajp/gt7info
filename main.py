import datetime
import requests
import csv
import os
import sys


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
                            price_in_jpy = format(int(data[i][1])*100, ",")

                            res.append(
                                {"makername": makername, "carname": carname, "price_in_jpy": price_in_jpy})
    return res


def PrintNewCarList(new_car_list):
    maxlen = {"makername": 13, "carname": 32, "price_in_jpy": 10}

    for car in new_car_list:
        if maxlen["makername"] < len(car["makername"]):
            maxlen["makername"] = len(car["makername"])
        if maxlen["carname"] < len(car["carname"]):
            maxlen["carname"] = len(car["carname"])
        if maxlen["price_in_jpy"] < len(car["price_in_jpy"]):
            maxlen["price_in_jpy"] = len(car["price_in_jpy"])

    for car in new_car_list:
        makername = car["makername"].ljust(maxlen["makername"]+3)
        carname = car["carname"].ljust(maxlen["carname"]+3)
        price_in_jpy = car["price_in_jpy"].rjust(maxlen["price_in_jpy"]+3)
        message = f"{makername}{carname}{price_in_jpy}"

        try:
            carYear = int(car["carname"][-2:])
            if carYear >= 29 or carYear == 0:
                print(f"\033[91m{message}\033[0m")
            else:
                print(f"{message}")
        except:
            print(f"\033[93m{message}\033[0m")

    if len(new_car_list) == 0:
        print("No new cars available.")

    print()


carList = LoadCSV("db/", "cars.csv")
makerList = LoadCSV("db/", "maker.csv")
today = datetime.datetime.utcnow().date()

how_many_days = 5
if len(sys.argv) > 1:
    how_many_days = int(sys.argv[1])

for i in reversed(range(how_many_days)):
    date_to_import = today - datetime.timedelta(i)
    filename = date_to_import.strftime("%y-%m-%d")+".csv"

    data_used = LoadCSV("used/", filename)
    data_legend = LoadCSV("legend/", filename)

    list_used = MakeNewCarList(data_used, carList, makerList)
    list_legend = MakeNewCarList(data_legend, carList, makerList)

    print(f"====={date_to_import}=====".center(64))
    print("---Used Car Dealership---".center(64))
    PrintNewCarList(list_used)

    print("---Legendary Dealership---".center(64))
    PrintNewCarList(list_legend)
    print()
