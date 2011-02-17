pyjs: Python to Javascript compiler
===================================

pyjs compiles Python code into Javascript.

    >>> import pyjs

    >>> print pyjs.compile("def square(x): return x*x")
    function square(x) {
        return x*x;
    }

Release Plan
============

**0.1**

* Compiles all python code
* Not supported: imports, classes, yield, list comprehensions, generator expression, nested scopes, keyword arguments, ellipses, exec

**0.2**

* nested scopes
* keyword arguments