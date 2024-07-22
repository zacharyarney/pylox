import sys
from lexer import Scanner


class Lox:
    def run(self, source: str):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        for token in tokens:
            print(token)

    def run_file(self, path: str):
        try:
            with open(path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    self.run(line)
        except FileNotFoundError:
            print(f"File not found: {path}")
            sys.exit(66)

    def run_prompt(self):
        while True:
            try:
                source = input("> ")
                if source.endswith("{"):
                    while not source.endswith("}"):
                        source += input("... ")
                self.run(source)
            except EOFError:
                print("\nExiting...")
                break
            except KeyboardInterrupt:
                print("\nExiting...")


if __name__ == "__main__":
    lox = Lox()
    if len(sys.argv) > 2:
        print("Usage: lox [script]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        lox.run_file(sys.argv[1])
    else:
        lox.run_prompt()
