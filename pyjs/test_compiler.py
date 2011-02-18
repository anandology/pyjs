import pyjs
from compiler import ast

def _test_compile_string():
    pyjs.compile_string("1") == "1"
    pyjs.compile_string("x+y") == "x + y" 
    pyjs.compile_string("x = 1") == "x  = 1;"

    pyjs.compile_string("if x == 1: y == x * x") == "if (x == 1) { y = x * x; }"


class TestVisitor:
    def __call__(self, code):
        return pyjs.compile(code).strip()
        
    def test_Add(self):
        assert self("1 + 2") == "1 + 2"

    def test_And(self):
        assert self("a and b") == "a && b"
        assert self("a and b and c") == "a && b && c"

    def test_AssAttr(self):
        assert self("a.x = 1") == "a.x = 1;"
        assert self("(a+b).x = 1") == "(a + b).x = 1;"

    def test_AssList(self):
        assert self("[a, b] = b, a") == "py.tmp = [b, a]; a = py.tmp[0]; b = py.tmp[1];"

    def test_AssName(self):
        assert self("a = 1") == "a = 1;"

    def test_AssTuple(self):
        assert self("a, b = b, a") == "py.tmp = [b, a]; a = py.tmp[0]; b = py.tmp[1];"

    def test_Assert(self):
        assert self("assert True") == "py.assert(true, nil);"

    def test_Assign(self):
        assert self("a = 1") == "a = 1;"

    def test_AugAssign(self):
        assert self("a += 1") == "a += 1;"

    def test_Backquote(self):
        assert self("`a`") == "py.repr(a)"

    def test_Bitand(self):
        assert self("a & b") == "a & b"

    def test_Bitor(self):
        assert self("a | b") == "a | b"

    def test_Bitxor(self):
        assert self("a ^ b") == "a ^ b"

    def test_Break(self):
        assert self("break") == "break;"

    def test_CallFunc(self):
        assert self("f(1)") == "f(1)"
        assert self("f(1, 2, *a, **kw)") == "f.apply(this, py.make_args([1, 2], a, kw))"

    def test_Class(self):
        pass

    def test_Compare(self):
        assert self("a == b") == "a == b"
        assert self("a < b <= c") == "a < b <= c"

    def test_Const(self):
        assert self("1") == "1"
        assert self("'a'") == '"a"'
        #assert self('"a"') == '"a"'
        assert self('x + "a"') == 'x + "a"'

    def test_Continue(self):
        assert self("continue") == "continue;"

    def test_Decorators(self):
        pass

    def test_Dict(self):
        assert self("{'a': 1}") == '{"a": 1}'

    def test_Discard(self):
        pass

    def test_Div(self):
        assert self("a / b") == "a / b"

    def test_Ellipsis(self):
        pass

    def test_Exec(self):
        pass

    def test_FloorDiv(self):
        assert self("a // b") == "py.floordiv(a, b)"

    def test_For(self):
        pass

    def test_From(self):
        pass

    def test_Function(self):
        pass

    def test_GenExpr(self):
        pass

    def test_GenExprFor(self):
        pass

    def test_GenExprIf(self):
        pass

    def test_GenExprInner(self):
        pass

    def test_Getattr(self):
        pass

    def test_Global(self):
        pass

    def test_If(self):
        pass

    def test_IfExp(self):
        pass

    def test_Import(self):
        pass

    def test_Invert(self):
        pass

    def test_Keyword(self):
        pass

    def test_Lambda(self):
        pass

    def test_LeftShift(self):
        pass

    def test_List(self):
        pass

    def test_ListComp(self):
        pass

    def test_ListCompFor(self):
        pass

    def test_ListCompIf(self):
        pass

    def test_Mod(self):
        pass

    def test_Module(self):
        pass

    def test_Mul(self):
        pass

    def test_Name(self):
        assert self("a") == "a"
        assert self("a_b") == "a_b"
        
        assert self("True") == "true"
        assert self("False") == "false"
        assert self("None") == "nil"

    def test_Not(self):
        assert self("not a") == "!a"

    def test_Or(self):
        pass

    def test_Pass(self):
        pass

    def test_Power(self):
        pass

    def test_Print(self):
        assert self("print x,") == 'py.print(x);'
        assert self("print x, y,") == 'py.print(x, y);'

    def test_Printnl(self):
        assert self("print x") == 'py.print(x, "\n");'
        assert self("print x, y") == 'py.print(x, y, "\n");'
    
    def test_Raise(self):
        pass
    def test_Return(self):
        assert self("return x") == "return x;"
        assert self("return x+y") == "return x + y;"

    def test_RightShift(self):
        pass

    def test_Slice(self):
        pass

    def test_Sliceobj(self):
        pass

    def test_Stmt(self):
        pass

    def test_Sub(self):
        pass

    def test_Subscript(self):
        pass

    def test_TryExcept(self):
        pass

    def test_TryFinally(self):
        pass

    def test_Tuple(self):
        pass

    def test_UnaryAdd(self):
        assert self("+1") == "+1"
        assert self("+a") == "+a"

    def test_UnarySub(self):
        assert self("-1") == "-1"
        assert self("-a") == "-a"

    def test_While(self):
        pass

    def test_With(self):
        pass

    def test_Yield(self):
        pass


