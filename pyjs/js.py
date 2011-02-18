"""pyjs compiler.
"""
import compiler
from compiler import ast
import json

class CompilerError(Exception):
    pass
    
def compile(code):
    _ast = compiler.parse('""\n' + code)
    return Visitor().visit(_ast)
    
class Visitor:       
    def __init__(self):
        self.indent = ""
         
    def visit(self, node):
        if node is None:
            return ""
            
        nodetype = node.__class__.__name__
        
        f = getattr(self, "visit_" + nodetype, None)
        if f:
            code = f(node)
        else:
            code = self.visit_children(node)
            
        if code is None:
            return ""
        elif isinstance(code, basestring):
            return code
        else:
            return "".join(code)
    
    __call__ = visit
    
    def visit_children(self, node, sep=" "):
        return sep.join(self.visit(n) for n in node.getChildNodes())
        
    # AST node visitors

    def visit_Add(self, node):
        return self(node.left) + " + " + self(node.right)

    def visit_And(self, node):
        return " && ".join(self(n) for n in node.nodes)

    def visit_AssAttr(self, node):
        if node.flags != "OP_ASSIGN":
            raise CompilerError("Unrecognized node: " + repr(node))
        
        if isinstance(node.expr, compiler.ast.Name):
            yield self(node.expr)
        else:
            yield "(" + self(node.expr) + ")"
        
        yield "."
        yield node.attrname

    def visit_AssList(self, node):
        # this will never get called. 
        # visit_Assign takes care of this.
        pass

    def visit_AssName(self, node):
        return node.name

    def visit_AssTuple(self, node):
        # this will never get called. 
        # visit_Assign takes care of this.
        pass

    def visit_Assert(self, node):
        test = self(node.test)
        # when fail is None, use nil in js.
        fail = node.fail and self(node.fail) or "nil"
        
        return "py.assert(%s, %s);" % (test, fail)

    def visit_Assign(self, node):
        left = node.getChildNodes()[0]
        right = node.getChildNodes()[1]
        
        if isinstance(left, (ast.AssList, ast.AssTuple)):
            return self._visit_multiple_assignment(left, right)
        else:
            # TODO: handle subscript and multiple assignments
            return self(left) + " = " + self(right) + ";"
            
    def _visit_multiple_assignment(self, left, right):
        if not isinstance(right, (ast.List, ast.Tuple)):
            raise CompilerError("Expected list or tuple, found %s", rigt.__class__.__name__)
        
        if len(left.getChildNodes()) != len(right.getChildNodes()):
            raise CompilerError("Number of items must be same on both sides for multiple assignment")
            
        yield "py.tmp = ["
        yield ", ".join(self(n) for n in right.getChildNodes())
        yield "]; "
        
        for i, n in enumerate(left.getChildNodes()):
            yield self(n) + " = py.tmp[%d]; " % i

    def visit_AugAssign(self, node):
        left = node.node
        right = node.expr
        return self(left) + " " + node.op + " " + self(right) + ";"

    def visit_Backquote(self, node):
        yield "py.repr("
        yield self(node.expr)
        yield ")"

    def visit_Bitand(self, node):
        return " & ".join(self(n) for n in node.nodes)

    def visit_Bitor(self, node):
        return " | ".join(self(n) for n in node.nodes)

    def visit_Bitxor(self, node):
        return " ^ ".join(self(n) for n in node.nodes)

    def visit_Break(self, node):
        return "break;"

    def visit_CallFunc(self, node):
        f = self(node.node)
        args = ", ".join(self(n) for n in node.args)
        if node.star_args or node.dstar_args:
            return "%s.apply(this, py.make_args([%s], %s, %s))" % (f, args, self(node.star_args) or "nil", self(node.dstar_args) or "nil")
        else:
            return "%s(%s)" % (f, args)

    def visit_Class(self, node):
        pass

    def visit_Compare(self, node):
        yield self(node.expr)
        yield " "
        for op, n in node.ops:
            yield op + " "
            yield self(n) + " "

    def visit_Const(self, node):
        if isinstance(node.value, basestring):
            return json.dumps(node.value)
        else:
            return repr(node.value)

    def visit_Continue(self, node):
        return "continue;"

    def visit_Decorators(self, node):
        pass

    def visit_Dict(self, node):
        pass

    def visit_Discard(self, node):
        return self.visit_children(node)

    def visit_Div(self, node):
        return self(node.left) + " / " + self(node.right)
        
    def visit_Ellipsis(self, node):
        pass

    def visit_Exec(self, node):
        pass

    def visit_FloorDiv(self, node):
        pass

    def visit_For(self, node):
        pass

    def visit_From(self, node):
        pass

    def visit_Function(self, node):
        return "function %s(%s) {\n%s\n}" % (node.name, ", ".join(node.argnames), self.visit(node.code))

    def visit_GenExpr(self, node):
        pass

    def visit_GenExprFor(self, node):
        pass

    def visit_GenExprIf(self, node):
        pass

    def visit_GenExprInner(self, node):
        pass

    def visit_Getattr(self, node):
        pass

    def visit_Global(self, node):
        pass

    def visit_If(self, node):
        children = node.getChildNodes()
        if_part, elif_parts, else_part = children[0], children[1:-1], children[-1]

        for i, (test, code) in enumerate(node.tests):
            if i == 0:
                label = "if"
            else:
                label = "else if"

            yield label
            yield "("
            yield self(test)
            yield ") {"

            yield self(code)
            yield "} "

        if else_part:
            yield "else {"
            yield self(else_part)
            yield "} "

    def visit_IfExp(self, node):
        pass

    def visit_Import(self, node):
        pass

    def visit_Invert(self, node):
        pass

    def visit_Keyword(self, node):
        pass

    def visit_Lambda(self, node):
        pass

    def visit_LeftShift(self, node):
        pass

    def visit_List(self, node):
        pass

    def visit_ListComp(self, node):
        pass

    def visit_ListCompFor(self, node):
        pass

    def visit_ListCompIf(self, node):
        pass

    def visit_Mod(self, node):
        pass

    def visit_Module(self, node):
        return self.visit_children(node)

    def visit_Mul(self, node):
        return self(node.left) + " * " + self(node.right)

    def visit_Name(self, node):
        names = {
            "True": "true",
            "False": "false",
            "None": "nil"
        }
        return names.get(node.name, node.name)

    def visit_Not(self, node):
        return "!" + self(node.expr)

    def visit_Or(self, node):
        return " || ".join(self(n) for n in node.nodes)

    def visit_Pass(self, node):
        pass

    def visit_Power(self, node):
        pass

    def visit_Print(self, node):
        return 'py.print(%s);' % ', '.join(self(n) for n in node.nodes)

    def visit_Printnl(self, node):
        return 'py.print(%s, "\n");' % ', '.join(self(n) for n in node.nodes)

    def visit_Raise(self, node):
        pass

    def visit_Return(self, node):
        return "return %s;" % self.visit(node.value)

    def visit_RightShift(self, node):
        pass

    def visit_Slice(self, node):
        pass

    def visit_Sliceobj(self, node):
        pass

    def visit_Stmt(self, node):
        for n in node.getChildNodes():
            yield self(n) + "\n"

    def visit_Sub(self, node):
        return self(node.left) + " - " + self(node.right)

    def visit_Subscript(self, node):
        pass

    def visit_TryExcept(self, node):
        pass

    def visit_TryFinally(self, node):
        pass

    def visit_Tuple(self, node):
        pass

    def visit_UnaryAdd(self, node):
        return "+" + self(node.expr)

    def visit_UnarySub(self, node):
        return "-" + self(node.expr)

    def visit_While(self, node):
        pass

    def visit_With(self, node):
        pass

    def visit_Yield(self, node):
        pass        
