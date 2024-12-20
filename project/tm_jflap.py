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
    width_in_states = int((len(turing.states)**0.5) + 1)
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

    for (old_state, input), (new_state, output, direction) \
            in turing.transition_table.items():
        if input == " ":
            input = ""
        if output == " ":
            output = ""

        table_entry = ElementTree.SubElement(table, "transition")
        ElementTree.SubElement(table_entry, "from").text = \
            str(state_to_id[old_state])
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


# def write_old(data, file_name):
#
#     map = {}
#     x = 0
#     for state in data["states"]:
#         map[state] = x
#         x += 1
#
#     root = ElementTree.Element("structure")
#     root.set("version", "1.0")
#     root.set("encoding", "UTF-8")
#     root.set("standalone", "no")
#     ElementTree.SubElement(root, "type").text = "turing"
#
# # define automaton
#     tab = ElementTree.SubElement(root, "automaton")
#     # define states
#     x = 0
#     y = 0
#     xstep = 50
#     ystep = 30
#     for state in data["states"]:
#         s = ElementTree.SubElement(tab, "state")
#         s.set("id", str(map[state]))
#         s.set("name", state)
#         ElementTree.SubElement(s, "x").text = str(x)
#         ElementTree.SubElement(s, "y").text = str(y)
#
#         if state == data["start_state"]:
#             ElementTree.SubElement(s, "initial")
#         if state in data["accept_states"]:
#             ElementTree.SubElement(s, "final")
#
#         x += xstep
#         if x > 10 * xstep:
#             x = 0
#             y += ystep
#
#     # define transitions
#     for (oldstate, input), (newstate, output, direction) \
#             in data["transition_table"].items():
#         if input == " ":
#             input = ""
#         if output == " ":
#             output = ""
#         t = ElementTree.SubElement(tab, "transition")
#         ElementTree.SubElement(t, "from").text = str(map[oldstate])
#         ElementTree.SubElement(t, "to").text = str(map[newstate])
#         ElementTree.SubElement(t, "read").text = input
#         ElementTree.SubElement(t, "write").text = output
#         ElementTree.SubElement(t, "move").text = direction[0].upper()
#
#     # write to file
#     string = ElementTree.tostring(root, "utf-8")
#     xml = minidom.parseString(string)
#     pretty_xml = xml.toprettyxml(indent="  ")
#
#     with open(file_name, "wb") as f:
#         f.write(pretty_xml.encode("UTF-8"))
#
#     print(f"turing-jflap-xml: Data written to {file_name}")
