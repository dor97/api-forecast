import requests
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


BASE_URL = "http://api.openweathermap.org/data/2.5/forecast?"

with open("API_KEY.txt", "r") as f:     #put http://api.openweathermap.org api key in API_KEY.txt file
    API_KEY = f.read()


#showing one chosen day forecast
def one_day_forcast(dfTemp, hour, date, data, dfHumidity):
    while True:
        day = input("choose a date(mm-dd) from " + date[0] + " to " + date[-1] + " to show temp and humidity from " + hour[0] + " to " + hour[-1] + " the next day: ")
        if day not in date:
            print("Not a valid date, try again")
        else:
            description = []
            for ind, i in enumerate(data['list'][date.index(day)*8:]):
                if ind > 7:
                    break
                description.append(i['weather'][0]['description'])
            descriptionSeries = pd.Series(description, index=hour)
            print(descriptionSeries)
            print(descriptionSeries.value_counts())

            plt.figure(figsize=(14,6) ,constrained_layout=True)
            plt.subplot(121)
            plt.title('temperature', fontsize=16)
            plt.xlabel(f'date({day})', fontsize=14)
            plt.ylabel('Celsius', fontsize=14)
            plt.grid(linestyle=':')
            plt.plot(hour, dfTemp[day], '.-')

            plt.subplot(122)
            plt.title('Humidity', fontsize=16)
            plt.xlabel(f'date({day})', fontsize=14)
            plt.ylabel('procent', fontsize=14)
            plt.grid(linestyle=':')
            plt.plot(hour, dfHumidity[day], '.-')

            plt.show()
            
            break

#showing the 5 next days forecast
def all_days_forcast(dfTemp, hour, date):
    plt.title('5 days temperature forcast', fontsize=16)
    plt.xlabel('hours', fontsize=14)
    plt.ylabel('Celsius', fontsize=14)
    
    plt.plot(hour, dfTemp.iloc[:,0], '.-', label=date[0])
    plt.plot(hour, dfTemp.iloc[:,1], '.-', label=date[1])
    plt.plot(hour, dfTemp.iloc[:,2], '.-',  label=date[2])
    plt.plot(hour, dfTemp.iloc[:,3], '.-', label=date[3])
    plt.plot(hour, dfTemp.iloc[:,4], '.-', label=date[4])
    plt.grid(linestyle=':')
    plt.legend(fontsize=14)
    plt.show()


#showing 5 next days forecast in 5 different grafs
def all_days_forcast_diffrent_grafse(dfTemp, hour, date):
    plt.figure(figsize=(14,6) ,constrained_layout=True)
    for i in range(5):
        one_day_forcast_diffrent_grafse(dfTemp, hour, date, i)
    plt.show()

#plot one day forecast
def one_day_forcast_diffrent_grafse(dfTemp, hour, date, i):
    plt.subplot(231+i)
    plt.title(f'date-{date[i]}', fontsize=10)
    plt.xlabel('hours', fontsize=7)
    plt.ylabel('Celsius', fontsize=7)

    plt.plot(hour, dfTemp.iloc[:,i], '.-', label=date[i])
    plt.grid(linestyle=':')


#showing multiple days forecast on one graf
def all_day_one_graf(dfTemp, dateAndHour):
    l = []

    for i in range(5):
        l.extend(dfTemp.iloc[:,i])

    plt.figure(figsize=(14,9) ,constrained_layout=True)
    plt.subplot(111)
    plt.xlabel('day-hour', fontsize=14)
    plt.ylabel('Celsius', fontsize=14)
    plt.grid(linestyle=':')
    answer = input("Do you want to see all data(yes) or a part of the data avelbol(no)?: ")
    if answer != 'no':
        plt.title(f"from-{dateAndHour[0]} to-{dateAndHour[-1]}", fontsize=16)
        plt.plot(dateAndHour[:], l[:], '.-')
    else:
        print(dateAndHour)
        while True:
            answer = input("chose a date(dd-hh) from the list above to start and date(dd-hh) to end(with a space btween them): ")
            answer = answer.split(' ')
            if len(answer) == 2 and answer[0] in dateAndHour and answer[1] in dateAndHour:
                dateStart = dateAndHour.index(answer[0])
                dateEnd = dateAndHour.index(answer[1])
                if dateEnd > dateStart:
                    if dateEnd == len(dateAndHour):
                        plt.title(f"from-{dateAndHour[dateStart]} to-{dateAndHour[dateEnd]}", fontsize=16)
                        plt.plot(dateAndHour[dateStart:], l[dateStart:], '.-')
                    else:
                        plt.title(f"from-{dateAndHour[dateStart]} to-{dateAndHour[dateEnd]}", fontsize=16)
                        plt.plot(dateAndHour[dateStart:dateEnd+1], l[dateStart:dateEnd+1], '.-')
                else:
                    print("End date need to be after start date, try again")
                    continue
                break
            else:
                print("Not a valid date, try again")
    plt.show()


#showing the min max and mean fortcast for next 5 days
def min_max_mean_fortcast(dfTemp, date, dfHumidity):
    
    minTemp = [np.min(dfTemp[i].values) for i in dfTemp]
    maxTemp = [np.max(dfTemp[i].values) for i in dfTemp]
    meanTemp = [np.mean(dfTemp[i].values) for i in dfTemp]
    
    minHumidity = [np.min(dfHumidity[i].values) for i in dfHumidity]
    maxHumidity = [np.max(dfHumidity[i].values) for i in dfHumidity]
    meanHumidity = [np.mean(dfHumidity[i].values) for i in dfHumidity]

    plt.figure(figsize=(10,4) ,constrained_layout=True)

    x_axis = np.arange(len(date))

    plt.subplot(121)
    plt.title('temperature', fontsize=16)
    plt.bar(x_axis-0.20 , minTemp, width=0.2, label = 'min')
    plt.bar(x_axis, maxTemp, width=0.2, label = 'max')
    plt.bar(x_axis+0.20, meanTemp, width=0.2, label = 'mean')
    plt.grid(linestyle=':')
    plt.xticks(x_axis,date)
    plt.legend()

    plt.subplot(122)
    plt.title('Humidity', fontsize=16)
    plt.bar(x_axis-0.20 , minHumidity, width=0.2, label = 'min')
    plt.bar(x_axis, maxHumidity, width=0.2, label = 'max')
    plt.bar(x_axis+0.20, meanHumidity, width=0.2, label = 'mean')
    plt.grid(linestyle=':')
    plt.xticks(x_axis,date)
    plt.legend()

    plt.show()



if __name__ == "__main__":
    city = input("Enter a city name: ")
    url = BASE_URL + "q=" + city  + "&appid=" + API_KEY

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        tempDic = {}
        date = []
        temp = []
        hour = []
        dateAndHour = []
        humidityDic = {}
        humidity = []
        for ind ,i in enumerate(data['list']):
            if ind < 8:
                hour.append(i['dt_txt'][11:16])
            temp.append(round(i['main']['temp'] - 273.15, 2))
            humidity.append(i['main']['humidity'])
            if ind % 8 == 0:
                date.append(i['dt_txt'][5:10])
            dateAndHour.append('-'.join(i['dt_txt'][8:13].split(' ')))
            if (ind + 1) % 8 == 0:
                tempDic[date[-1]] = temp
                temp = []
                humidityDic[date[-1]] = humidity
                humidity = []


        dfHumidity = pd.DataFrame(humidityDic, index=hour)
        dfTemp = pd.DataFrame(tempDic, index=hour)
        print("Temperature table(celsius):")
        print(dfTemp)
        print("Humidity table:")
        print(dfHumidity)
        
        print('''chose which forcast you want
        1)one day forcast
        2)all days forcast
        3)all days forcast in diffrent grafs
        4)all days forcast one graf
        5)min max and mean fortcast all days''')
        
        while True:
            try:
                option = int(input("pick the corresponding number: "))
            except ValueError:
                print("enter a valid number")
                continue
            else:
                if(option > 5 or option < 1):
                    print('enter a number btween 1 to 5')
                else:
                    break
        if(option == 1):
            one_day_forcast(dfTemp, hour, date, data, dfHumidity)
        elif(option == 2):
            all_days_forcast(dfTemp, hour, date)
        elif(option == 3):
            all_days_forcast_diffrent_grafse(dfTemp, hour, date)
        elif(option == 4):
            all_day_one_graf(dfTemp, dateAndHour)
        elif(option == 5):
            min_max_mean_fortcast(dfTemp, date, dfHumidity)


    else:
        print("An error ocurred.")
        print(response.status_code)