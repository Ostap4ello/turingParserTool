import turing_machine
import tm_tmio_yaml
import tm_formal
import tm_jflap

from pathlib import Path


tm_list = []  # list of Turing Machines


def getoption():
    print("")
    print("Please select an option:")
    print("1. Import a Turing Machine")
    print("2. Export a Turing Machine")
    print("3. Exit")
    option = input("Select an option: ")
    return option


def import_tm():
    print("")
    print("Please enter file name: ")
    file_name = input().strip()

    if not Path(file_name).is_file():
        print("File not found")
        return

    tm = turing_machine.TuringMachine()
    if Path(file_name).suffix == ".yaml":
        tm_tmio_yaml.read(tm, file_name)
    elif Path(file_name).suffix == ".xml":
        # tm = tm_jflap.read(file_name)
        print("JFLAP import not supported yet")
    elif Path(file_name).suffix == ".txt":
        # tm = tm_formal.read(file_name)
        print("Formal import not supported yet")
    else:
        print("Invalid file type")
        return

    if tm.check() is False:
        print("Turing Machine is not valid")
        return

    tm_list.append(tm)

    print("Turing Machine imported successfully, as index", len(tm_list)-1)


def export_tm():
    if len(tm_list) == 0:
        print("No Turing Machines to export")
        return

    elif len(tm_list) > 1:
        print("Please select Turing Machine:")
        for i, tm in enumerate(tm_list):
            print(f"{i + 1}. {tm.name}")
        print("")
        option = int(input("Select an option: ").strip())
        if option < 1 or option > len(tm_list):
            print("Invalid option")
            return

        tm = tm_list[option - 1]
    else:
        tm = tm_list[0]

    print("Please select Export type:")
    print("1. Export to YAML")
    print("2. Export to Formal")
    print("3. Export to JFLAP")

    option = int(input("Select an option: ").strip())

    print("Please enter file name (if blank):")

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
        print("Invalid option")
        return


if __name__ == "__main__":

    print("Hello, user!")
    print("This is a Turing Machine Parser")

    while True:
        option = getoption().strip()
        if option == "1":
            import_tm()
        elif option == "2":
            export_tm()
        elif option == "3":
            break
