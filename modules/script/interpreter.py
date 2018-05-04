"""
Core of the NestScript interpreter.
"""

import asyncio
from collections import defaultdict

import operator
from . import tokens, exceptions

OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "==": operator.eq,
    "!=": operator.ne,
    "<=": operator.le,
    ">=": operator.ge,
    "<": operator.lt,
    ">": operator.gt,
}


class NodeVisitor:

    async def visit(self, node):
        if isinstance(node, tokens.Token):
            method_name = "visit_" + type(node).__name__
            visitor = getattr(self, method_name, self.generic_visit)
            result = visitor(node)
            return await result if asyncio.iscoroutine(result) else result
        else:
            return node

    @staticmethod
    def generic_visit(node):
        raise AttributeError("No visit_{} method".format(type(node).__name__))


class Interpreter(NodeVisitor):

    def __init__(self, scope: dict = None, protected: list = None):
        self.preserved_scope = scope if scope else {}
        self.protected = protected if protected else []
        self.scope = None
        self.ctx = None
        self.counts = None

    async def visit_Op(self, node):
        left = await self.visit(node.left)
        right = await self.visit(node.right)
        return OPERATORS[node.sign](left, right)

    async def visit_Compound(self, node):
        for child in node.stmts:
            _ = await self.visit(child)
        else:
            return
        return _

    async def visit_While(self, node):
        while await self.visit(node.cond):
            self.counts["while"] += 1
            if self.counts["while"] > 100:
                raise exceptions.WhileProtection(100)
            await self.visit(node.compound)

    async def visit_If(self, node):
        b = await self.visit(node.cond)
        if b:
            await self.visit(node.compound)
        else:
            await self.visit(node.else_)

    async def visit_Else(self, node):
        await self.visit(node.compound)

    async def visit_Assign(self, node):
        var_name = node.variable.name
        val = await self.visit(node.value)

        if isinstance(val, list):
            val = [await self.visit(item) for item in val]

        self.scope[var_name] = val

    async def visit_Var(self, node):
        var_name = node.name
        if isinstance(var_name, tokens.Token):
            return await self.visit(var_name)

        val = self.scope.get(var_name)

        if val is None:
            raise NameError(repr(var_name))

        return val

    async def visit_Call(self, node: tokens.Call):
        func = await self.visit(node.function.name)
        if isinstance(func, str):
            func = self.scope.get(func)

        # Protected functions get context as first argument, and are counted.
        if func in self.protected:
            args = [self.ctx]
            self.counts[func.__name__] += 1
            if self.counts[func.__name__] > 3:
                raise exceptions.CallProtection(max_allowed=3)
        else:
            args = []

        args.extend([await self.visit(arg) for arg in node.args])

        kwargs = {
            key: await self.visit(arg) for key, arg in node.kwargs.items()
        }

        # Protect ctx from being overriden.
        kwargs.pop("ctx", None)
        ret = func(*args, **kwargs)

        return await ret if asyncio.iscoroutine(ret) else ret

    def visit_GetAttr(self, node):
        item = self.scope[node.path[0]]
        for index in node.path[1:]:
            item = getattr(item, index)
        return item

    async def visit_SetAttr(self, node):
        n = node.parent
        r = node.child
        v = await self.visit(node.value)
        setattr(self.scope[n], r, v)

    async def visit_Program(self, node):
        for stmt in node.stmts:
            await self.visit(stmt)

    async def interpret(self, ctx, ast, scope: dict = None):
        """
        Interpret an AST.
        """
        self.scope = self.preserved_scope.copy()
        if self.protected:
            self.scope.update({f.__name__: f for f in self.protected})

        self.ctx = ctx
        self.counts = defaultdict(int)

        if scope:
            self.scope.update(scope)

        return await self.visit_Program(ast)

    async def visit_ByIndex(self, node):
        item = self.scope.get(node.name)
        for index in node.indices:
            item = item.__getitem__(await self.visit(index))
        return item


# TODO: Stop using asyncio.get_event_loop
class InterpreterPool:
    """
    Provide a pool for interpreters that share a common "stdlib".
    """

    def __init__(
        self, stdlib: dict = None, protected: dict = None, pool_size=10
    ):
        self._pool = asyncio.Queue()
        loop = asyncio.get_event_loop()
        for _ in range(pool_size):
            instance = Interpreter(stdlib, protected)
            loop.run_until_complete(self._pool.put(instance))

    async def interpret(self, ctx, ast, methods=None):
        """|coro|

        Fetch an interpreter and run a program.

        Parameters
        ----------
        ctx:
            Context of the interpreter.
        ast:
            The AST to interpret.
        methods:
            Python methods to bind.
        """
        interpreter = await self._pool.get()
        await interpreter.interpret(ctx, ast, methods)
        await self._pool.put(interpreter)
