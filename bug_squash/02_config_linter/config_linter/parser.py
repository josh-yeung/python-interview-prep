import ast
def parse_config(source: str, filename: str = "<config>") -> ast.Module:
    return ast.parse(source, filename=filename, mode="exec")


def read_and_parse(filepath: str) -> ast.Module:
    with open(filepath, "r", encoding="utf-8") as handle:
        source = handle.read()
    return parse_config(source, filename=filepath)
