"""Tests the runtime using python-spidermonkey.
"""
import pyjs

import pytest
spidermonkey = pytest.importorskip("spidermonkey")

def jseval(code, **env):
    """Compiles the given python code and executes the generated javascript code in the given environment.
    """
    ctx = spidermonkey.Runtime().new_context()
    for k, v in env.items():
        ctx.add_global(k, v)
    
    jscode = pyjs.compile(code)
    print jscode.strip()
    return ctx.execute(jscode)
    
def test_binary_operations():
    assert jseval("5 + 2") == 7
    assert jseval("5 - 2") == 3
    assert jseval("5 * 2") == 10
    assert jseval("5 / 2") == 2
    
def test_assignment():
    assert jseval("a = 1; b = a+a; b") == 2
    
def test_functions():
    double = jseval("def double(x): return x+x\ndouble")
    assert double(0) == 0
    assert double(1) == 2
    assert double(1.2) == 2.4
