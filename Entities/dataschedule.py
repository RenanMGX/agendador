import os
import json
from datetime import datetime
from exception.exception_person import Error, Pass

class DataSchedule():
    def __init__(self, pathFile = f"{os.getcwd()}\\agendador_dados.json"):
        self.__pathFile = pathFile
        if not os.path.exists(self.__pathFile):
            with open(self.__pathFile, 'w') as file:
                dataTest = []
                json.dump(dataTest, file)
        self.__recurrenceValid = [
            "daily",
            "monday",
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

