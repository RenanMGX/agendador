import subprocess
from time import sleep
import json
from getpass import getuser
from copy import deepcopy
import schedule
from datetime import datetime
import os
import traceback
import multiprocessing

def data_file_path():
    with open(f"C:\\Users\\{getuser()}\\.agendador_config\\config.json" , 'r')as file:
        return read_schedule(json.load(file)['scheduleFile'])

def read_schedule(path):
    with open(path, 'r')as file:
        return json.load(file)

class ExecuteList():
    def __init__(self, name, path_file, day=None, log_path="log_execution.csv"):
        self.__log_path = log_path
        self.__day = day
        self.__name = name
        self.__path_file = path_file

        cwd= deepcopy(path_file).split("/")
        cwd.pop(-1)
        self.__cwd = "/".join(cwd)

        if not os.path.exists(self.__log_path):
            with open(self.__log_path, 'w')as file:
                file.write(f"Date;Name;Path;Status;Description\n")
        
        self.start()
        
    def log(self,status, descri=""):
        with open(self.__log_path, 'a')as file:
            file.write(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')};{self.__name};{self.__path_file};{status};{descri}\n")

    def start(self):
        if self.__day != None:
            if not (int(self.__day) == datetime.now().day):
                return 
        
        try:
            print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - the program '{self.__name}' has been started!")
            
            # QUEUE = multiprocessing.Queue()
            # thread = multiprocessing.Process(target=multi_start, args=(QUEUE, self.__path_file, self.__cwd))
            # thread.start()
            
            # retorno_file:dict = QUEUE.get()
            
            # process:subprocess.Popen = retorno_file["process"]
            # stderr:str = retorno_file["stderr"]
            
            process = subprocess.Popen(['python', self.__path_file], shell=True, cwd=self.__cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                #print(f"\n{stdout}\n")
                self.log("OK")
            else:
                #print(f"Erro durante a execução. Código de retorno: {process.returncode}")
                stderr = stderr.replace('\n', f"\n{' '*22}")
                print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - an error ocurred with program '{self.__name}': \n{' '*22}{stderr} ")
                self.log("Error", stderr.replace("\n", " <br> "))
                #raise stderr
        except Exception:
            error = traceback.format_exc()
            error = error.replace('\n', f"\n{' '*22}")
            print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - the program '{self.__name}' can not be executed! motive: \n{' '*22}{error} ")
            self.log("Error", error.replace("\n", " <br> "))

            
def multi_start(queue:multiprocessing.Queue, path_file, cwd):
    process = subprocess.Popen(['python', path_file], shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    queue.put({"stdout": stdout, "process" : process})
        

    
    
class ScheduleExecute():
    def __init__(self, schedule:list):
        self.__schedule = schedule
        
    def categorization_schedules(self):
        daily_s = [{"time":line['date']['time'], "event" : multiprocessing.Process(target=ExecuteList, args=(line['name'],line['path']))} for line in self.__schedule if line['date']['recurrence'] == "daily"]
        
        monday_s = [{"time":line['date']['time'], "event" : multiprocessing.Process(target=ExecuteList, args=(line['name'],line['path']))} for line in self.__schedule if line['date']['recurrence'] == "monday"]
        tuesday_s = [{"time":line['date']['time'], "event" : multiprocessing.Process(target=ExecuteList, args=(line['name'],line['path']))} for line in self.__schedule if line['date']['recurrence'] == "tuesday"]
        wednesday_s = [{"time":line['date']['time'], "event" : multiprocessing.Process(target=ExecuteList, args=(line['name'],line['path']))} for line in self.__schedule if line['date']['recurrence'] == "wednesday"]
        thursday_s = [{"time":line['date']['time'], "event" : multiprocessing.Process(target=ExecuteList, args=(line['name'],line['path']))} for line in self.__schedule if line['date']['recurrence'] == "thursday"]
        friday_s = [{"time":line['date']['time'], "event" : multiprocessing.Process(target=ExecuteList, args=(line['name'],line['path']))} for line in self.__schedule if line['date']['recurrence'] == "friday"]
        saturday_s = [{"time":line['date']['time'], "event" : multiprocessing.Process(target=ExecuteList, args=(line['name'],line['path']))} for line in self.__schedule if line['date']['recurrence'] == "saturday"]
        sunday_s = [{"time":line['date']['time'], "event" : multiprocessing.Process(target=ExecuteList, args=(line['name'],line['path']))} for line in self.__schedule if line['date']['recurrence'] == "sunday"]
        day_s = [{"time": line['date']['time'], "event" : multiprocessing.Process(target=ExecuteList, args=(line['name'],line['path'], line['date']['recurrence'].split(" ")[1]))} for line in self.__schedule if line['date']['recurrence'].split(" ")[0] == "day"]

        for line in daily_s:
            schedule.every().day.at(line['time']).do(line['event'].start)

        for line in monday_s:
            schedule.every().monday.at(line['time']).do(line['event'].start)

        for line in tuesday_s:
            schedule.every().tuesday.at(line['time']).do(line['event'].start)

        for line in wednesday_s:
            schedule.every().wednesday.at(line['time']).do(line['event'].start)

        for line in thursday_s:
            schedule.every().thursday.at(line['time']).do(line['event'].start)

        for line in friday_s:
            schedule.every().friday.at(line['time']).do(line['event'].start)

        for line in saturday_s:
            schedule.every().saturday.at(line['time']).do(line['event'].start)

        for line in sunday_s:
            schedule.every().sunday.at(line['time']).do(line['event'].start)

        for line in day_s:
            schedule.every().day.at(line['time']).do(line['event'].start)

def print_list_programs(file):
    for line in file:
        print(f"the program '{line['name']}' will be executed in '{line['date']['recurrence']}' at '{line['date']['time']}'")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    path_file = data_file_path()
    create_schedule = ScheduleExecute(path_file)
    create_schedule.categorization_schedules()
    print("Execute Schedule running!\n")

    print_list_programs(path_file)

    print(f'\nnow {datetime.now()}\n')
    while True:
        schedule.run_pending()
        sleep(1)

        time = datetime.now()
        if (time.hour == 0) and (time.minute == 0) and (time.second == 0):
            print_list_programs(path_file)
        elif (time.minute == 0) and (time.second == 0):
            print(f"{time.strftime('%d/%m/%Y %H:%M:%S')} - this program are running!")
