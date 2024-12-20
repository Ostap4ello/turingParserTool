class TuringMachine:
    name: str
    states: list[str]
    input_alphabet: list[str]
    tape_alphabet: list[str]
    start_state: str
    # (old_state, input_symbol) : (new_state, output_symbol, direction)
    transition_table: dict[tuple[str, str], tuple[str, str, str]]
    accept_state: list[str]

    def __init__(self):
        self.name = "none"
        self.states = []
        self.input_alphabet = []
        self.tape_alphabet = []
        self.start_state = ""
        self.transition_table = {}
        self.accept_state = []

    def check(self) -> bool:
        if self.start_state not in self.states:
            print("Start state not in states")
            return False
        for accept_state in self.accept_state:
            if accept_state not in self.states:
                print("Accept state not in states")
                return False

        for (old_state, input_symbol), \
                (new_state, output_symbol, direction) \
                in self.transition_table.items():

            if old_state not in self.states:
                print("Old state not in states")
                return False
            if new_state not in self.states:
                print("New state not in states")
                return False
            if input_symbol not in self.input_alphabet:
                print("Input symbol not in input alphabet")
                return False
            if output_symbol not in self.tape_alphabet:
                print("Output symbol not in tape alphabet")
                return False
            if direction not in ["Left", "Right"]:
                print("Invalid direction")
                return False

        return True

    def print(self):
        if self.check() is False:
            print("Turing Machine is not valid")
            return

        print(f"Name: {self.name}")
        print(f"Input Alphabet: {self.input_alphabet}")
        print(f"Tape Alphabet: {self.tape_alphabet}")
        print(f"Start State: {self.start_state}")
        print(f"Accept State: {self.accept_state}")
        print("Transition Table:")
        for (old_state, input_symbol), \
                (new_state, output_symbol, direction) \
                in self.transition_table.items():

            print(f"({old_state}, {input_symbol}) \
            -> ({new_state}, {output_symbol}, {direction})")
