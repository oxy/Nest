from typing import Union
from dataclasses import dataclass


class Token:
    """
    Base class from which any tokens are derived.
    """
    pass


@dataclass(eq=False)
class Var(Token):
    """
    Represents a variable.
    """
    name: Union[str, "GetAttr", "ByIndex"]


class ByIndex(Token):
    """
    Access a variable in scope by index.
    """

    def __init__(self, name: str, *indices):
        self.name = name
        self.indices = indices

    def __repr__(self):
        return f"ByIndex({self.name}[{'.'.join(str(index) for index in self.indices)}])"


class GetAttr(Token):
    """
    Get an attribute from the scope.
    """

    def __init__(self, *path):
        if not path:
            raise ValueError
        self.path = path

    def __repr__(self):
        return f"GetAttr({'.'.join(str(index) for index in self.path)})"


@dataclass(eq=False)
class Assign(Token):
    """
    Represents an assignment.
    """

    def __init__(self, variable: Var, value):
        self.variable = variable
        self.value = value

    def __repr__(self):
        return f"Assign({self.variable} = {self.value})"


class Op(Token):
    """
    An operator for an expression.
    """

    def __init__(self, left, sign: str, right):
        self.left = left
        self.right = right
        self.sign = sign

    def __repr__(self):
        return f"Op({self.left} {self.sign} {self.right})"


# TODO: multiple levels deep
class SetAttr(Token):
    """
    Set the value of an attribute.
    """

    def __init__(self, parent, child, value):
        self.parent = parent
        self.child = child
        self.value = value

    def __repr__(self):
        return (f"GetAttr({self.parent}." f"{self.child} = {self.value})")


class Compound(Token):
    """
    Represents a block of statements.
    """

    def __init__(self, stmts):
        self.stmts = stmts

    def __repr__(self):
        return "{" + ",".join(str(i) for i in self.stmts) + "}"


class Call(Token):
    """
    Represents a call to an external function.
    """

    def __init__(self, node, args: list, kwargs: dict):
        self.function = node
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        return f"Call({self.function}, {self.args}, {self.kwargs})"


class If(Token):
    """
    Represents a conditional (if) clause.
    """

    def __init__(self, cond: Op, compound: Compound, else_: Compound = []):
        self.cond = cond
        self.compound = compound
        self.else_ = else_

    def __repr__(self):
        return f"If({self.cond}, {self.compound}, {self.else_})"


class While(Token):

    def __init__(self, cond, compound):
        self.cond = cond
        self.compound = compound

    def __repr__(self):
        return f"While({self.cond}, {self.compound})"


class Program(Token):

    def __init__(self, stmts):
        self.stmts = stmts

    def __repr__(self):
        return "Program(" + ", ".join(str(i) for i in self.stmts) + ")"
