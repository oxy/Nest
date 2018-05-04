import os.path as path

from arpeggio import cleanpeg, PTNodeVisitor, visit_parse_tree
from . import tokens


class Converter(PTNodeVisitor):
    """
    Converter to generate an AST from a parse tree.
    """

    @staticmethod
    def visit_factor(_, children):
        if len(children) == 1:
            return children[0]

        return (
            tokens.Op(-1, "*", children[1])
            if children[0] == "-"
            else children[1]
        )

    @staticmethod
    def visit_term(_, children):
        expr = children[0]

        for i in range(2, len(children), 2):
            expr = tokens.Op(expr, children[i - 1], children[i])

        return expr

    @staticmethod
    def visit_expr(_, children):
        expr = children[0]
        for i in range(2, len(children), 2):
            expr = tokens.Op(expr, children[i - 1], children[i])

        return expr

    @staticmethod
    def visit_program(_, children):
        return tokens.Program(children)

    @staticmethod
    def visit_stmt(_, children):
        if len(children) == 1:
            return children[0]
        return children

    @staticmethod
    def visit_compound(_, children):
        return tokens.Compound(children)

    @staticmethod
    def visit_assign(_, children):
        if isinstance(children[1], tokens.GetAttr):
            return tokens.SetAttr(
                children[0].parent, children[0].child, children[1]
            )
        return tokens.Assign(children[0], children[1])

    @staticmethod
    def visit_attr(_, children):
        return tokens.GetAttr(*children)

    @staticmethod
    def visit_integer(node, _):
        return int(node.value)

    @staticmethod
    def visit_float(node, _):
        return float(node.value)

    @staticmethod
    def visit_call(_, children):
        function = children[0]
        args = []
        kwargs = {}
        end_of_args = False
        for child in children[1:]:
            if isinstance(child, dict):
                end_of_args = True
                kwargs.update(child)
            elif not end_of_args:
                args.append(child)
            else:
                raise ValueError(
                    "Positional argument follows keyword argument."
                )

        return tokens.Call(function, args, kwargs)

    @staticmethod
    def visit_string(_, children):
        return children[0] if children else ""

    @staticmethod
    def visit_array(_, children):
        return children

    @staticmethod
    def visit_cond(_, children):
        expr = children[0]
        for i in range(2, len(children), 2):
            expr = tokens.Op(expr, children[i - 1], children[i])

        return expr

    @staticmethod
    def visit_var(_, children):
        return tokens.Var(*children)

    @staticmethod
    def visit_if(_, children):
        return tokens.If(*children)

    @staticmethod
    def visit_while(_, children):
        if len(children) == 1:
            return tokens.While(children[0], [])
        return tokens.While(*children)

    @staticmethod
    def visit_byindex(_, children):
        return tokens.ByIndex(*children)

    @staticmethod
    def visit_kwarg(_, children):
        return {children[0]: children[1]}


with open(
    path.realpath(path.join(__file__, path.pardir, "language.peg"))
) as file:
    parser = cleanpeg.ParserPEG(file.read(), "program")

converter = Converter()


def parse(code: str):
    parsetree = parser.parse(code)
    return visit_parse_tree(parsetree, converter)
