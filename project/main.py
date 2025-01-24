from locale_json import *
import turing_machine
import tm_tmio_yaml
import tm_formal
import tm_jflap

import enum
from pathlib import Path

tm_list = []  # list of Turing Machines
locale = load_locale("locale.json")

class State(enum.Enum):
    MAIN_INTRO = 0
    MAIN_GETOPTION = 1
    TM_IMPORT = 2
    TM_EXPORT = 3
    EXIT = -1

def main():
    state = State.MAIN_INTRO

    while True:
        if state == State.MAIN_INTRO:
            state = intro()
        elif state == State.MAIN_GETOPTION:
            state = getoption()
        elif state == State.TM_IMPORT:
            state = import_tm()
        elif state == State.TM_EXPORT:
            state = export_tm()
        elif state == State.EXIT:
            break


# states
def intro() -> State:
    print_message("info", "intro", locale)
    return State.MAIN_GETOPTION

def getoption():
    print_message("info", "getoption", locale)
    option = input("Select an option: ")
    if option == "1":
        return State.TM_IMPORT
    elif option == "2":
        return State.TM_EXPORT
    elif option == "3":
        return State.EXIT
    else:
        print_message("error", "invalid_option", locale)
        return State.MAIN_GETOPTION

def import_tm() -> State:
    print_message("info", "ask_for_file", locale)

    file_name = input().strip()

    if not Path(file_name).is_file():
        print_message("error", "file_not_found", locale)
        return State.MAIN_GETOPTION

    tm = turing_machine.TuringMachine()

    if Path(file_name).suffix == ".yaml":
        status = tm_tmio_yaml.read(tm, file_name)
    elif Path(file_name).suffix == ".jff":
        status = tm_jflap.read(tm, file_name)
    elif Path(file_name).suffix == ".txt":
        print_message("error", "turing_machine_not_supported", locale)
        status = 0
    else:
        print_message("error", "file_invalid_type", locale)
        status = 0
        return State.MAIN_GETOPTION

    if tm.check() is False:
        print_message("error", "turing_machine_invalid", locale)
        return State.MAIN_GETOPTION

    if status == 0:
        pass

    tm_list.append(tm)

    print_message("info", "turing_machine_imported", locale)
    print("Index: %d" % (len(tm_list)))

    return State.MAIN_GETOPTION

def export_tm() -> State:

    if len(tm_list) == 0:
        print_message("error", "turing_machine_no_to_export", locale)
        return State.MAIN_GETOPTION

    elif len(tm_list) > 1:
        print_message("info", "ask_for_turing_machine", locale)
        for i, tm in enumerate(tm_list):
            print(f"{i + 1}. {tm.name}")
        print()
        option = int(input("Select an option: ").strip())
        if option < 1 or option > len(tm_list):
            print_message("error", "invalid_option", locale)
            return State.MAIN_GETOPTION

        tm = tm_list[option - 1]
    else:
        tm = tm_list[0]

    print_message("info", "export_options", locale)

    option = int(input("Select an option: ").strip())

    print_message("info", "ask_for_file", locale)

    file_name = input().strip()
    if file_name == "":
        file_name = "output"

    if option == 1:
        tm_tmio_yaml.write(tm, file_name)
    elif option == 2:
        tm_formal.write(tm, file_name)
    elif option == 3:
        tm_jflap.write(tm, file_name)
    else:
        print_message("error", "invalid_option", locale)

    return State.MAIN_GETOPTION


# start program
if __name__ == "__main__":
    main();
