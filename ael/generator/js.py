def generate(node):

    def generate_program(program):
        for s in program.statements:
            generate(s)

    def generate_print_statement(s):
        print(f"console.log({generate(s.expression)})")

    def generate_assignment(s):
        pass

    # locals()[f"generate_{type(node).__name__.lower()}"]

    return f"JavaScript generation coming soon: {locals()}"
