import turing_machine


def write(turing: turing_machine.TuringMachine, file_name: str):
    with open(file_name, "w") as f:
        f.write("TM1 = (Q, T, B, Σ, δ, q0, F)\n")

        row = "Q = { "
        for state in turing.states:
            row += state + ", "
        row += "}\n"
        f.write(row)

        row = "T = { "
        for symbol in turing.tape_alphabet:
            row += symbol + ", "
        row += "}\n"
        f.write(row)

        f.write("B = ''\n")

        row = "Σ = { "
        for symbol in turing.input_alphabet:
            row += symbol + ", "
        row += "}\n"
        f.write(row)

        row = "δ = {\n"
        for (oldstate, input), (newstate, output, direction) \
                in turing.transition_table.items():
            row += f"    ({oldstate}, {input}) -> \
                ({newstate}, {output}, {direction})\n"
        row += "}\n"
        f.write(row)

        f.write(f"q0 = {turing.start_state}\n")

        row = "F = { "
        for state in turing.accept_state:
            row += state + " "
        row += "}\n"
        f.write(row)

        print(f"tm_formal: data written to {file_name}")
