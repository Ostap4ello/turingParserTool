import turing_machine
import xml.etree.ElementTree as ElementTree
import xml.dom.minidom as minidom


def write(turing: turing_machine.TuringMachine, file_name: str):
    # jflap uses id's for states, so we need to map the states to id's
    state_to_id = {}
    id = 0
    for state in turing.states:
        state_to_id[state] = id
        id += 1

    # jflap neeeds x and y coordinates for states - dummy values
    state_to_position = {}
    x = 0
    y = 0
    x_spacing = 50
    y_spacing = 30
    width_in_states = int((len(turing.states) ** 0.5) + 1)
    for state in turing.states:
        state_to_position[state] = (x, y)
        x += x_spacing
        if x > width_in_states * x_spacing:
            x = 0
            y += y_spacing

    # create xml structure
    root = ElementTree.Element("structure")
    root.set("version", "1.0")
    root.set("encoding", "UTF-8")
    root.set("standalone", "no")
    ElementTree.SubElement(root, "type").text = "turing"

    table = ElementTree.SubElement(root, "automaton")
    for state in turing.states:
        state_entry = ElementTree.SubElement(table, "state")
        state_entry.set("id", str(state_to_id[state]))
        state_entry.set("name", state)
        ElementTree.SubElement(state_entry, "x").text = \
            str(state_to_position[state][0])
        ElementTree.SubElement(state_entry, "y").text = \
            str(state_to_position[state][1])

        if state == turing.start_state:
            ElementTree.SubElement(state_entry, "initial")
        if state in turing.accept_state:
            ElementTree.SubElement(state_entry, "final")

    for (old_state, input), (
        new_state,
        output,
        direction,
    ) in turing.transition_table.items():
        if input == " ":
            input = ""
        if output == " ":
            output = ""

        table_entry = ElementTree.SubElement(table, "transition")
        ElementTree.SubElement(table_entry, "from").text \
            = str(state_to_id[old_state])
        ElementTree.SubElement(table_entry, "to").text = \
            str(state_to_id[new_state])
        ElementTree.SubElement(table_entry, "read").text = input
        ElementTree.SubElement(table_entry, "write").text = output
        ElementTree.SubElement(table_entry, "move").text = direction[0].upper()

    # write to file
    string = ElementTree.tostring(root, "utf-8")
    xml = minidom.parseString(string)
    pretty_xml = xml.toprettyxml(indent="  ")

    with open(file_name, "wb") as f:
        f.write(pretty_xml.encode("UTF-8"))

    print(f"tm_jflap: data written to {file_name}")


def read(turing: turing_machine.TuringMachine, file_name: str):
    tree = ElementTree.parse(file_name)
    root = tree.getroot()

    # read states and map ro id's
    id_to_state = {}
    for state in root.findall("automaton/state"):
        name = str(state.get("name")).strip()
        id = state.get("id")
        id_to_state[id] = name

        turing.states.append(name)

        if "initial" in state.attrib:
            turing.start_state = name
        if "final" in state.attrib:
            turing.accept_state.append(name)

    # read transitions
    for transition in root.findall("automaton/transition"):
        # Find elements and handle missing cases
        from_elem = transition.find("from")
        from_state = (
            id_to_state[int(from_elem.text)]
            if from_elem is not None and from_elem.text is not None
            else "undefined"
        )

        to_elem = transition.find("to")
        to_state = (
            id_to_state[int(to_elem.text)]
            if to_elem is not None and to_elem.text is not None
            else "undefined"
        )

        read_elem = transition.find("read")
        read = (
            id_to_state[int(read_elem.text)]
            if read_elem is not None and read_elem.text is not None
            else "undefined"
        )

        write_elem = transition.find("write")
        write = (
            id_to_state[int(write_elem.text)]
            if write_elem is not None and write_elem.text is not None
            else "undefined"
        )

        move_elem = transition.find("move")
        move = (
            id_to_state[int(move_elem.text)]
            if move_elem is not None and move_elem.text is not None
            else "undefined"
        )

        # Debug output for missing or default values
        if "undefined" in (from_state, to_state, read, write, move):
            print(
                f"Warning: Missing elements in transition. Parsed values: "
                f"from={from_state}, to={to_state}, read={read}, \
                write={write}, move={move}"
            )

        # Process the transition
        print(
            f"Transition: from={from_state}, to={to_state}, read={read}, \
            write={write}, move={move}"
        )

        turing.transition_table[(from_state, read)] = (to_state, write, move)

    print(f"tm_jflap: data read from {file_name}")
