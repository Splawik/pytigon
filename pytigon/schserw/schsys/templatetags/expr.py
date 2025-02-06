import re
import html

from django import template
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

register = template.Library()


def mark_safe2(x):
    """Replace '<' and '>' with '[' and ']' to make the string safe."""
    if isinstance(x, str):
        return mark_safe(x.replace("<", "[").replace(">", "]"))
    else:
        return x


class ExprNode(template.Node):
    """Node for evaluating expressions in Django templates."""

    def __init__(self, expr_string, var_name=None, safe=True, escape=False):
        self.expr_string = expr_string
        self.var_name = var_name
        self.safe = safe
        self.escape = escape

    def render(self, context):
        """Render the expression and handle errors."""
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
                            mark_safe2(eval(self.expr_string, d))
                        )
                    else:
                        context[self.var_name] = html.escape(eval(self.expr_string, d))
                else:
                    if self.safe:
                        context[self.var_name] = mark_safe2(eval(self.expr_string, d))
                    else:
                        context[self.var_name] = eval(self.expr_string, d)
                return ""
            else:
                try:
                    val = eval(self.expr_string, d)
                except:
                    print("ERROR:")
                    print(self.expr_string)
                    print(d)
                    print("------------------------------")
                    val = None
                if val != None:
                    if self.safe:
                        ret = mark_safe2(str(val))
                    else:
                        ret = str(val)
                    if self.escape:
                        return html.escape(ret)
                    else:
                        return ret
                else:
                    return ""
        except:
            print("EXPR ERROR:", self.expr_string)
            raise


r_expr = re.compile(r"(.*?)\s+as\s+(\w+)", re.DOTALL)


def do_expr(parser, token):
    """Handle the 'expr' template tag."""
    try:
        (tag_name, arg) = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires arguments" % token.contents[0]
        )
    m = r_expr.search(arg)
    if m:
        (expr_string, var_name) = m.groups()
    else:
        if not arg:
            raise template.TemplateSyntaxError(
                "%r tag at least require one argument" % tag_name
            )
        (expr_string, var_name) = (arg, None)
    return ExprNode(expr_string, var_name, False)


do_expr = register.tag("expr", do_expr)


def do_expr_safe(parser, token):
    """Handle the 'expr_safe' template tag."""
    try:
        (tag_name, arg) = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires arguments" % token.contents[0]
        )
    m = r_expr.search(arg)
    if m:
        (expr_string, var_name) = m.groups()
    else:
        if not arg:
            raise template.TemplateSyntaxError(
                "%r tag at least require one argument" % tag_name
            )
        (expr_string, var_name) = (arg, None)
    return ExprNode(expr_string, var_name, True)


do_expr_safe = register.tag("expr_safe", do_expr_safe)


def do_expr_escape(parser, token):
    """Handle the 'expr_escape' template tag."""
    try:
        (tag_name, arg) = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires arguments" % token.contents[0]
        )
    m = r_expr.search(arg)
    if m:
        (expr_string, var_name) = m.groups()
    else:
        if not arg:
            raise template.TemplateSyntaxError(
                "%r tag at least require one argument" % tag_name
            )
        (expr_string, var_name) = (arg, None)
    return ExprNode(expr_string, var_name, True, True)


do_expr_escape = register.tag("expr_escape", do_expr_escape)


def build_eval(parser, token):
    """Handle the 'eval' template tag."""
    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError("eval takes one argument")
    (tag, val_expr) = bits
    return EvalObject(val_expr)


class GetContext:
    """Helper class to get context variables."""

    def __init__(self, context):
        self.context = context

    def __getitem__(self, key):
        if key in self.context:
            return self.context.get(key)
        else:
            return None


class EvalObject(template.Node):
    """Node for evaluating expressions in the context."""

    def __init__(self, val_expr):
        self.val_expr = val_expr

    def render(self, context):
        """Render the evaluated expression."""
        output = eval(self.val_expr, {"this": GetContext(context)})
        context["eval"] = output
        return ""


register.tag("eval", build_eval)
