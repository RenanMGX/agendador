import sys
import os
import subprocess
from Entities.dataschedule import DataSchedule
from tkinter import filedialog
from time import sleep
from Entities.exception.exception_person import Pass
import multiprocessing

exit_param = [
    "exit",
    "bye",
    "exit()",
    "/e",
    "/b",
]
help_param = [
    "help",
    "/h",
    "-help",
]

read_param = [
    "read",
    "load",
    "/r"
]

create_param = [
    "create",
    "save",
    "/c",
]

update_param = [
    "update",
    "/u",
]

delete_param = [
    "delete",
    "del"
    "/d"
]

    

if __name__ == "__main__":
    data = DataSchedule()

    print("shedule python start\n")
    while True:
        print("Write an command")
        command = input("command: ").lower()
        
        if command in help_param:
            print("Parameters:")
            print(f"    Exit - {exit_param}")
            print(f"    Help - {help_param}")
            print(f"    Read - {read_param}")
            print(f"    Create - {create_param}")
            print(f"    Update - {update_param}")
            print(f"    Delete - {delete_param}")
            print()
        
        elif command in exit_param:
            print("Shutdown the program!")
            sleep(1)
            sys.exit()
        
        elif command in read_param:
            print("List of scheduled programs:\n")
            for line in data.read():
                #print(f"    {line}")
                print(f"the program '{line['name']}' will be executed in '{line['date']['recurrence']}' at '{line['date']['time']}'")
            print()
        
        elif command in create_param:
            print("\nCreate a new schedule line:")
            print("    write a name of program")
            name = str(input("    Name: "))
                
            while True:
                print("\n    select an file")
                sleep(2)
                path = filedialog.askopenfilename()
                sleep(1)
                res = input(f"    this path are correct? '{path}'\n    write (y/n): ").lower()
                if res == "y":
                    break

            print("\n    Set a recurrence")
            print("    case is empty the recurrence are set default 'daily'")
            recurrence = recurrence if (recurrence:=input("    Recurrence: ")) != "" else "daily"
            print("    Set the time")
            time = input("    Time: ")

            if (response:=data.create(name=name, path=path, recurrence=recurrence, time=time).__class__.__name__) == Pass().__class__.__name__:
                print("\n    Schedule line Created!\n")
            else:
                print(f"\n    Error when save this line motive:\n    {response}\n    try again!")

        elif command in update_param:
            print("\nUpdate an schedule line:")
            print("    write a name of program")
            name = str(input("    Name: "))
                
            while True:
                if not (input("    update the file path (y/n)? ").lower() == "y"):
                    path = None
                    break
                print("\n    select an file")
                sleep(2)
                path = filedialog.askopenfilename()

                sleep(1)
                res = input(f"    this path are correct? '{path}'\n    write (y/n): ").lower()
                if res == "y":
                    break

            print("\n    Set a recurrence")
            print("    case is empty the recurrence are not updated")
            recurrence = recurrence if (recurrence:=input("    Recurrence: ")) != "" else None
            print("    Set the time")
            print("    case the time are empty are not updated")
            time = time if (time:=input("    Time: ")) != "" else None

            if (response:=data.update(name=name, path=path, recurrence=recurrence, time=time).__class__.__name__) == Pass().__class__.__name__:
                print("\n    Schedule line has been updated!\n")
            else:
                print(f"\n    Error when updated this line motive:\n    {type(response)}\n    try again!")

        elif command in delete_param:
            print("\nUpdate an schedule line:")
            print("    write a name of program for delete")
            name = input("    Name: ")

            if (response:=data.delete(name=name, path=path, recurrence=recurrence, time=time).__class__.__name__) == Pass().__class__.__name__:
                print("\n    Schedule line has been deleted!\n")
            else:
                print(f"\n    Error when updated this line motive:\n    {type(response)}\n    try again!")

        
        

    