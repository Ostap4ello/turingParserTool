import turing_machine
import tempfile
import yaml
import re


def expand_list_keys(input_file_path, output_file_path):
    """
    Reads a YAML-like file, expands list keys, and writes the modified file.
    Example: ['key1', 'key2']: value -> key1: value and key2: value
    """
    with open(input_file_path, "r") as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:

        indent = len(line) - len(line.lstrip())
        # Match lines with list keys (e.g., ['key1', 'key2']: value)
        match = re.match(r"^\s*\[(.+)\]\s*:\s*(.+)", line)
        if match:
            keys = match.group(1).split(",")  # Extract the keys inside []
            value = match.group(2).strip()  # Extract the value after :
            for key in keys:
                # Write each key-value pair as a separate line
                updated_lines.append(f"{' ' * indent}{key.strip()}: {value}\n")
        else:
            # Keep other lines as-is
            updated_lines.append(line)

    # Write the updated content to the output file
    with open(output_file_path, "w") as f:
        f.writelines(updated_lines)


def read(file_name) -> turing_machine.TuringMachine:
    # substitute ['key1', 'key2']: value -> key1: value and key2: value,
    # as the yaml parser does not support list keys
    tmp_file = tempfile.NamedTemporaryFile(delete=True)
    expand_list_keys(file_name, tmp_file.name)

    # Load the updated YAML file
    with open(tmp_file.name, "r") as f:
        tmpdata = yaml.full_load(f)

        # Parse the YAML data
        turing = turing_machine.TuringMachine()

        if turing.name.strip() == "":
            turing.name = "none"

        turing.start_state = tmpdata["start state"]

        for oldstate, info in tmpdata.table.items():
            # fill turing.states
            if oldstate not in turing.states:
                turing.states.append(oldstate)
            if info is None:
                continue    # skip empty states

            for input, command in info.items():
                # fill turing.input_alphabet
                if input not in turing.input_alphabet:
                    turing.input_alphabet.append(input)

                # output
                if "write" in command.keys():
                    if command["write"] not in turing.tape_alphabet:
                        turing.tape_alphabet.append(command["write"])
                    output = command["write"]
                else:
                    output = input
                # move direction and new state
                if "R" in command:
                    direction = "Right"
                    newstate = command["R"]
                elif "L" in command:
                    direction = "Left"
                    newstate = command["L"]
                else:
                    print(f"tm_tmio_yaml: No direction provided for \
                        {oldstate}, {input}")
                    exit(1)

                # put entry into the table
                turing.transition_table[(oldstate, input)] = \
                    (newstate, output, direction)

        # add missing accept state
        if turing.accept_state == []:
            if "accept" in turing.states:
                turing.accept_state.append("accept")
            # else:
            #     print("No accept state provided, provide one")
            #     print("States:")
            #     for state in turing.states:
            #         print(state, end=", ")
            #     print()
            #     for i in range(3):
            #         print("Select accept state: ", end="")
            #         accept = input()
            #         if accept in turing.states:
            #             turing.accept_states.append(accept)
            #             break
            #         else:
            #             print("Invalid state")

    if turing.check() is False:
        print("tm_tmio_yaml: Turing Machine is not valid")
        exit(1)

    print("tm_tmio_yaml: Data read successfully")
    return turing


def write(turing: turing_machine.TuringMachine, file_name="none"):

    if file_name == "none":
        print("No file path provided")
        return

    with open(file_name, "w") as f:
        f.write(f"name: {turing.name}\n")
        f.write(f"start state: {turing.start_state}\n")
        f.write("table:\n")

        # sort the transition table by oldstate
        table = dict(sorted(turing.transition_table.items(),
                            key=lambda x: x[0][0]))

        current_oldstate = ""
        states = turing.states
        # current_newstate, current_output, current_direction = "", "", ""
        for (oldstate, input), (newstate, output, direction) \
                in table.items():
            if oldstate != current_oldstate:
                current_oldstate = oldstate
                states.remove(oldstate)
                f.write(f"  {oldstate}:\n")

            if input == "":
                input = " "
            if output == "":
                output = " "
            if direction == "Left":
                direction = "L"
            elif direction == "Right":
                direction = "R"

            if input == output:
                f.write("    %s: {%s: \"%s\"}\n" % (
                    input, direction, newstate))
            else:
                f.write("    %s: {%s: \"%s\", write: \"%s\"}\n" % (
                    input, direction, newstate, output))
        for state in states:
            f.write(f"  {state}:\n")
    print("tm_tmio_yaml: Data written successfully")


# def read_old(file_name="none") -> dict[str, any]:
#     if file_name == "none":
#         print("No file path provided")
#         return {}
#
#     tmp_file = file_name + ".tmp"
#
#     # Expand list keys in the file
#     expand_list_keys(file_name, tmp_file)
#
#     # Load the updated YAML file
#     with open(tmp_file, "r") as f:
#         tmpdata = yaml.full_load(f)
#
#     data = {
#         "name": "none",
#         "states": [],
#         "input_alphabet": [],
#         "tape_alphabet": [],
#         "start_state": "",
#         "accept_states": [],
#         "transition_table": {}
#     }
#
#     # Parse the YAML data
#
#     # print("Select name of the Turing Machine: ", end="")
#     # data["name"] = input()
#     if data["name"].strip() == "":
#         data["name"] = "none"
#
#     if "start state" not in tmpdata:
#         print("No start state provided")
#         return {}
#     data["start_state"] = tmpdata["start state"]
#
#     for oldstate, info in tmpdata["table"].items():
#         # fill oldstate
#         if oldstate not in data["states"]:
#             data["states"].append(oldstate)
#         if info is None:
#             continue    # skip empty states
#
#         for input, command in info.items():
#             # output
#             if "write" in command.keys():
#                 if command["write"] not in data["tape_alphabet"]:
#                     data["tape_alphabet"].append(command["write"])
#                 output = command["write"]
#             else:
#                 output = input
#             # direction and new state
#             if "R" in command:
#                 direction = "Right"
#                 newstate = command["R"]
#             elif "L" in command:
#                 direction = "Left"
#                 newstate = command["L"]
#             else:
#                 print("No direction provided")
#                 return {}
#             # entry in table
#             data["transition_table"][(oldstate, input)] = \
#                 (newstate, output, direction)
#
#             # fill states, input_alphabet and tape_alphabet
#             if input not in data["input_alphabet"]:
#                 data["input_alphabet"].append(input)
#             if input not in data["tape_alphabet"]:
#                 data["tape_alphabet"].append(input)
#             if newstate not in data["states"]:
#                 data["states"].append(newstate)
#
#     # add missing accept state
#     if data["accept_states"] == []:
#         if "accept" in data["states"]:
#             data["accept_states"].append("accept")
#         # else:
#         #     print("No accept state provided, provide one")
#         #     print("States:")
#         #     for state in data["states"]:
#         #         print(state, end=", ")
#         #     print()
#         #     for i in range(3):
#         #         print("Select accept state: ", end="")
#         #         accept = input()
#         #         if accept in data["states"]:
#         #             data["accept_states"].append(accept)
#         #             break
#         #         else:
#         #             print("Invalid state")
#
#     if len(data["accept_states"]) == 0:
#         print("No accept state provided")
#         return {}
#
#     print("turing-yaml: Data read successfully")
#     return data
#
#
# def write(data: dict[str, any], file_name="none"):
#
#     if file_name == "none":
#         print("No file path provided")
#         return
#
#     print("haha not implemented yet, all I can do is print the data")
#     print(data)
