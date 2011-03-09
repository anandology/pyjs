import pyjs
from compiler import ast
import os, re

def _test_compile_string():
    pyjs.compile_string("1") == "1"
    pyjs.compile_string("x+y") == "x + y" 
    pyjs.compile_string("x = 1") == "x  = 1;"

    pyjs.compile_string("if x == 1: y == x * x") == "if (x == 1) { y = x * x; }"

class BaseTest:
    def __call__(self, code):
        js = pyjs.compile(code).strip()
        return js.replace("\n", " ").replace("  ", " ")

class TestVisitor(BaseTest):
        
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

        assert self("a in b") == "py.in(a, b)"
        assert self("a not in b") == "!py.in(a, b)"

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
        assert self("{'a': 1}") == 'py.dict([["a", 1]])'

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
        assert self("a.x") == "a.x"
        assert self("(a+b).x") == "(a + b).x"

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

    def test_complex_code(self):
        assert self("(1 + 2) * 3") == "(1 + 2) * 3"
        
class TestFunctionVars(BaseTest):
    def test_with_assignment(self):
        assert self("def f(a, b): sum = a + b; return sum") == "function f(a, b) { var sum; sum = a + b; return sum; }"

    def test_with_AugAssign(self):
        assert self("def f(a): sum += a; return sum") == "function f(a) { var sum; sum += a; return sum; }"
        
    def test_globals(self):
        assert self("def f(a): global x; x = a; return x") == "function f(a) { py.globals.x = a; return py.globals.x; }"
        assert self("def f(a): global x; x+= a; return x") == "function f(a) { py.globals.x += a; return py.globals.x; }"
    
def test_samples():
    path = os.path.join(os.path.dirname(__file__), "test_samples.txt")
    text = open(path).read()
    
    for py, js in parse_samples(text):
        yield do_test_compile, py, js
        
def trim_js(js):
    return re.compile("\s+").sub(" ", js).strip().replace(" )", ")")
    
def do_test_compile(py, js):
    js2 = pyjs.compile(py)
    
    js2 = trim_js(js2)
    js = trim_js(js)
    
    template = "Test failed:\n%s\n\nExpected:\n\n%s\n\nGot:\n\n%s\n\n"
    assert js2 == js, template % (py, js, js2)
        
def test_parse_samples():
    assert list(parse_samples("===\na\n---\nb\n")) == [("a", "b")]
    assert list(parse_samples("===\na\naa\n---\nb\nbb\n")) == [("a\naa", "b\nbb")]

def parse_samples(text):
    for test in text.split("==="):
        if "\n---" in test:
            py, js = test.split("\n---", 1)
            
            # strip comments in js. 
            # In python compiler takes care of them anyway.
            js = "\n".join(line for line in js.splitlines() if not line.startswith("#")).strip()
            
            yield py.strip(), js.strip()    
