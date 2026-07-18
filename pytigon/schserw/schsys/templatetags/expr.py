import ast
import html
import operator
import re

from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

register = template.Library()

_SAFE_BUILTINS = {
    "True": True,
    "False": False,
    "None": None,
    "abs": abs,
    "all": all,
    "any": any,
    "bin": bin,
    "bool": bool,
    "chr": chr,
    "dict": dict,
    "divmod": divmod,
    "enumerate": enumerate,
    "filter": filter,
    "float": float,
    "format": format,
    "frozenset": frozenset,
    "hex": hex,
    "int": int,
    "isinstance": isinstance,
    "issubclass": issubclass,
    "iter": iter,
    "len": len,
    "list": list,
    "map": map,
    "max": max,
    "min": min,
    "oct": oct,
    "ord": ord,
    "pow": pow,
    "range": range,
    "reversed": reversed,
    "round": round,
    "set": set,
    "slice": slice,
    "sorted": sorted,
    "str": str,
    "sum": sum,
    "tuple": tuple,
    "zip": zip,
}

_SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.And: lambda a, b: a and b,
    ast.Or: lambda a, b: a or b,
    ast.Not: operator.not_,
    ast.Invert: operator.invert,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
    ast.In: lambda a, b: a in b,
    ast.NotIn: lambda a, b: a not in b,
}

# Allowed attributes for built-in types
_SAFE_ATTRIBUTES = {
    str: {
        "capitalize", "casefold", "center", "count", "encode", "endswith",
        "expandtabs", "find", "format", "format_map", "index", "isalnum",
        "isalpha", "isascii", "isdecimal", "isdigit", "isidentifier",
        "islower", "isnumeric", "isprintable", "isspace", "istitle",
        "isupper", "join", "ljust", "lower", "lstrip", "maketrans",
        "partition", "removeprefix", "removesuffix", "replace", "rfind",
        "rindex", "rjust", "rpartition", "rsplit", "rstrip", "split",
        "splitlines", "startswith", "strip", "swapcase", "title",
        "translate", "upper", "zfill",
    },
    list: {
        "append", "clear", "copy", "count", "extend", "index",
        "insert", "pop", "remove", "reverse", "sort",
    },
    dict: {
        "clear", "copy", "fromkeys", "get", "items", "keys",
        "pop", "popitem", "setdefault", "update", "values",
    },
    tuple: {"count", "index"},
    set: {
        "add", "clear", "copy", "difference", "difference_update",
        "discard", "intersection", "intersection_update", "isdisjoint",
        "issubset", "issuperset", "pop", "remove", "symmetric_difference",
        "symmetric_difference_update", "union", "update",
    },
    frozenset: {
        "copy", "difference", "intersection", "isdisjoint",
        "issubset", "issuperset", "symmetric_difference", "union",
    },
}


def _is_safe_attribute(value, attr):
    """Check if attribute access is allowed."""
    # Block absolutely all attributes starting with '_'
    if attr.startswith("_"):
        raise ValueError(f"Access to private/dunder attribute '{attr}' is forbidden")

    # Check whitelist for built-in types
    for safe_type, safe_attrs in _SAFE_ATTRIBUTES.items():
        if isinstance(value, safe_type):
            if attr not in safe_attrs:
                raise ValueError(
                    f"Attribute '{attr}' is not allowed on {safe_type.__name__}"
                )
            return True

    # For remaining types (e.g. Django models) — block access
    raise ValueError(
        f"Attribute access on type '{type(value).__name__}' is not permitted"
    )


class _SafeEval(ast.NodeVisitor):
    def __init__(self, context):
        self.context = context

    def visit_Expression(self, node):
        """Tree root for ast.parse(..., mode='eval')"""
        return self.visit(node.body)

    def visit_Module(self, node):
        """Tree root for ast.parse(..., mode='exec') — fallback"""
        if len(node.body) != 1:
            raise ValueError("Only single expressions allowed")
        return self.visit(node.body[0])

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_Constant(self, node):
        return node.value

    def visit_Name(self, node):
        if node.id in self.context:
            return self.context[node.id]
        if node.id in _SAFE_BUILTINS:
            return _SAFE_BUILTINS[node.id]
        raise NameError(f"name '{node.id}' is not defined")

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)
        if op_type not in _SAFE_OPS:
            raise ValueError(f"Unsafe operator: {op_type.__name__}")
        return _SAFE_OPS[op_type](left, right)

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        op_type = type(node.op)
        if op_type not in _SAFE_OPS:
            raise ValueError(f"Unsafe operator: {op_type.__name__}")
        return _SAFE_OPS[op_type](operand)

    def visit_BoolOp(self, node):
        result = self.visit(node.values[0])
        op_type = type(node.op)
        for v in node.values[1:]:
            result = _SAFE_OPS[op_type](result, self.visit(v))
        return result

    def visit_Compare(self, node):
        left = self.visit(node.left)
        for op, comparator in zip(node.ops, node.comparators):
            right = self.visit(comparator)
            op_type = type(op)
            if op_type not in _SAFE_OPS:
                raise ValueError(f"Unsafe comparison: {op_type.__name__}")
            if not _SAFE_OPS[op_type](left, right):
                return False
            left = right
        return True

    def visit_IfExp(self, node):
        test = self.visit(node.test)
        if test:
            return self.visit(node.body)
        return self.visit(node.orelse)

    def visit_Subscript(self, node):
        value = self.visit(node.value)
        slice_val = self.visit(node.slice)
        return value[slice_val]

    def visit_Slice(self, node):
        return slice(
            self.visit(node.lower) if node.lower else None,
            self.visit(node.upper) if node.upper else None,
            self.visit(node.step) if node.step else None,
        )

    def visit_List(self, node):
        return [self.visit(e) for e in node.elts]

    def visit_Tuple(self, node):
        return tuple(self.visit(e) for e in node.elts)

    def visit_Dict(self, node):
        return {self.visit(k): self.visit(v) for k, v in zip(node.keys, node.values)}

    def visit_Attribute(self, node):
        value = self.visit(node.value)
        _is_safe_attribute(value, node.attr)
        return getattr(value, node.attr)

    def visit_Call(self, node):
        func = self.visit(node.func)
        args = [self.visit(a) for a in node.args]
        kwargs = {kw.arg: self.visit(kw.value) for kw in node.keywords}
        return func(*args, **kwargs)

    def visit_JoinedStr(self, node):
        parts = []
        for v in node.values:
            parts.append(str(self.visit(v)))
        return "".join(parts)

    def visit_FormattedValue(self, node):
        return self.visit(node.value)

    def generic_visit(self, node):
        raise ValueError(f"Unsafe expression: {type(node).__name__}")


def _safe_eval(expr_string, context):
    try:
        tree = ast.parse(expr_string.strip(), mode="eval")
        return _SafeEval(context).visit(tree)
    except SyntaxError:
        return ast.literal_eval(expr_string.strip())


def mark_safe2(x):
    if isinstance(x, str):
        return mark_safe(x.replace("<", "[").replace(">", "]"))
    else:
        return x


# Regex anchored at start and end, used with re.fullmatch
r_expr = re.compile(r"^(.*?)\s+as\s+(\w+)$", re.DOTALL)


def _parse_expr_arg(tag_name, arg):
    """
    Parse expr tag argument.
    Use fullmatch instead of search to avoid silently ignoring
    expression fragments containing the keyword 'as'.
    """
    if not arg:
        raise template.TemplateSyntaxError(
            f"{tag_name!r} tag requires at least one argument"
        )
    m = r_expr.fullmatch(arg.strip())
    if m:
        expr_string, var_name = m.groups()
        if not expr_string.strip():
            raise template.TemplateSyntaxError(
                f"{tag_name!r} tag: expression before 'as' cannot be empty"
            )
        return expr_string.strip(), var_name
    return arg.strip(), None


class ExprNode(template.Node):
    def __init__(self, expr_string, var_name=None, safe=True, escape=False):
        self.expr_string = expr_string
        self.var_name = var_name
        self.safe = safe
        self.escape = escape

    def render(self, context):
        try:
            clist = list(context)
            clist.reverse()
            d = {}
            d["_"] = _
            for c in clist:
                d.update(c)
            if self.var_name:
                if self.escape:
                    if self.safe:
                        context[self.var_name] = html.escape(
                            mark_safe2(_safe_eval(self.expr_string, d))
                        )
                    else:
                        context[self.var_name] = html.escape(
                            _safe_eval(self.expr_string, d)
                        )
                else:
                    if self.safe:
                        context[self.var_name] = mark_safe2(
                            _safe_eval(self.expr_string, d)
                        )
                    else:
                        context[self.var_name] = _safe_eval(self.expr_string, d)
                return ""
            else:
                try:
                    val = _safe_eval(self.expr_string, d)
                except Exception:
                    print("ERROR:")
                    print(self.expr_string)
                    print(d)
                    print("------------------------------")
                    val = None
                if val is not None:
                    ret = mark_safe2(str(val)) if self.safe else str(val)
                    if self.escape:
                        return html.escape(ret)
                    else:
                        return ret
                else:
                    return ""
        except Exception:
            print("EXPR ERROR:", self.expr_string)
            raise


def do_expr(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            f"{token.contents.split()[0]!r} tag requires arguments"
        )
    expr_string, var_name = _parse_expr_arg(tag_name, arg)
    return ExprNode(expr_string, var_name, safe=False)


do_expr = register.tag("expr", do_expr)


def do_expr_safe(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            f"{token.contents.split()[0]!r} tag requires arguments"
        )
    expr_string, var_name = _parse_expr_arg(tag_name, arg)
    return ExprNode(expr_string, var_name, safe=True)


do_expr_safe = register.tag("expr_safe", do_expr_safe)


def do_expr_escape(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            f"{token.contents.split()[0]!r} tag requires arguments"
        )
    expr_string, var_name = _parse_expr_arg(tag_name, arg)
    return ExprNode(expr_string, var_name, safe=True, escape=True)


do_expr_escape = register.tag("expr_escape", do_expr_escape)


def build_eval(parser, token):
    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError("eval takes one argument")
    tag, val_expr = bits
    return EvalObject(val_expr)


class GetContext:
    def __init__(self, context):
        self.context = context

    def __getitem__(self, key):
        if key in self.context:
            return self.context.get(key)
        else:
            return None


class EvalObject(template.Node):
    def __init__(self, val_expr):
        self.val_expr = val_expr

    def render(self, context):
        output = _safe_eval(self.val_expr, {"this": GetContext(context)})
        context["eval"] = output
        return ""


register.tag("eval", build_eval)
