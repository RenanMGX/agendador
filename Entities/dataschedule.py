import os
import json
from datetime import datetime
from exception.exception_person import Error, Pass
from getpass import getuser

class DataSchedule():
    def __init__(self, pathFile = f"{os.getcwd()}\\agendador_dados.json"):
        self.__pathFile = pathFile
        if not os.path.exists(self.__pathFile):
            with open(self.__pathFile, 'w') as file:
                dataTest = []
                json.dump(dataTest, file)

        config_path = f"C:\\Users\\{getuser()}\\.agendador_config\\"
        if not os.path.exists(config_path):
            os.makedirs(config_path)
        with open(config_path + "config.json", 'w')as file:
            json.dump({"scheduleFile": pathFile}, file)

        self.__recurrenceValid = [
            "daily",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
            "day 1",
            "day 2",
            "day 3",
            "day 4",
            "day 5",
            "day 6",
            "day 7",
            "day 8",
            "day 9",
            "day 10",
            "day 11",
            "day 12",
            "day 13",
            "day 14",
            "day 15",
            "day 16",
            "day 17",
            "day 18",
            "day 19",
            "day 20",
            "day 21",
            "day 22",
            "day 23",
            "day 24",
            "day 25",
            "day 26",
            "day 27",
            "day 28",
            "day 29",
            "day 30",
            "day 31",
        ]
    
    def create(self, name, path, time, recurrence="daily"):
        dataTemp: list = self.read()

        if not recurrence in self.__recurrenceValid:
            return Error(f"this recurrence '{recurrence}' is not valid!")
        
        try:
            datetime.strptime(time, "%H:%M")
        except ValueError as error:
            return Error(error)
        
        for data in dataTemp:
            if data['name'] == name:
                return Error(f"this name '{name}' exists, try other.")

        dataForSave = {
            "name" : name,
            "path" : path,
            "date" : {
                "recurrence" : recurrence,
                "time" : time,
            }
        }

        dataTemp.append(dataForSave)
        with open(self.__pathFile, 'w')as file:
            json.dump(dataTemp, file)
            return Pass("save completed!")
        
    def read(self):
        with open(self.__pathFile, 'r')as file:
            return json.load(file)
        
    def update(self, name, path=None, time=None, recurrence=None):
        dataTemp: list = self.read()
        for data in dataTemp:
            if data['name'] == name:
                if path == None:
                    path = data['path']
                if time == None:
                    time = data['date']['time']
                if recurrence == None:
                    recurrence = data['date']['recurrence']

                if not recurrence in self.__recurrenceValid:
                    return Error(f"this recurrence '{recurrence}' is not valid!")
                
                try:
                    datetime.strptime(time, "%H:%M")
                except ValueError as error:
                    return Error(error)
                
                data['path'] = path
                data['date']['time'] = time
                data['date']['recurrence'] = recurrence
            

                with open(self.__pathFile, 'w')as file:
                    json.dump(dataTemp, file)   
                    return Pass("Updated!")
                
        return Error(f"this name '{name}' not found!")
    
    def delete(self, name):
        dataTemp: list = self.read()
        for data in dataTemp:
            if data['name'] == name:
                dataTemp.pop(dataTemp.index(data))
                with open(self.__pathFile, 'w') as file:
                    json.dump(dataTemp, file)
                    return Pass(f"this data '{data['name']} as deleted!")
        
        return Error(f"this name '{name}' not found!")

if __name__ == "__main__":
    data = DataSchedule()
    #data.create(name="Indice2", path="c:\\temp\\test.py", time="08:00")
    for line in data.read():
        print(line)

