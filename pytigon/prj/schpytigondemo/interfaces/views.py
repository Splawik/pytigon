from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django import forms
from django.template.loader import render_to_string
from django.template import Context, Template
from django.template import RequestContext
from django.conf import settings
from django.views.generic import TemplateView

from pytigon_lib.schviews.form_fun import form_with_perms
from pytigon_lib.schviews.viewtools import (
    dict_to_template,
    dict_to_odf,
    dict_to_pdf,
    dict_to_json,
    dict_to_xml,
    dict_to_ooxml,
    dict_to_txt,
    dict_to_hdoc,
)
from pytigon_lib.schviews.viewtools import render_to_response
from pytigon_lib.schdjangoext.tools import make_href
from pytigon_lib.schdjangoext import formfields as ext_form_fields
from pytigon_lib.schviews import actions

from django.utils.translation import gettext_lazy as _

from . import models
import os
import sys
import datetime
from django.utils import timezone

from pytigon_lib.schtools import nim_ext
from django.conf import settings
import os

ext_path = os.path.join(settings.DATA_PATH, settings.PRJ_NAME, "prjlib")

lib = nim_ext.load_nim_lib(os.path.join(ext_path, "schpytigondemo_test_nim"), "ext")


def make_csum_fun():
    from pytigon_lib.schtools.llvm_exec import compile_str_to_module, get_function
    from ctypes import CFUNCTYPE, c_int

    fun_str = """
    define dso_local i32 @cadd(i32 %0, i32 %1) #0 {
      %3 = alloca i32, align 4
      %4 = alloca i32, align 4
      store i32 %0, i32* %3, align 4
      store i32 %1, i32* %4, align 4
      %5 = load i32, i32* %3, align 4
      %6 = load i32, i32* %4, align 4
      %7 = add nsw i32 %5, %6
      ret i32 %7
    }
    """

    compile_str_to_module(fun_str)
    func_ptr = get_function("cadd")
    cfunc = CFUNCTYPE(c_int, c_int, c_int)(func_ptr)
    return cfunc


csum = make_csum_fun()


@dict_to_template("interfaces/v_test_interfaces.html")
def test_interfaces(request, **argv):
    title1 = "wasm from zig"
    import interfaces.applib
    from wasmtime import Store, Module, Instance, Func, FuncType

    wasm_path = os.path.join(interfaces.applib.__path__[0], "test_zig.wasm")

    store = Store()
    module = Module.from_file(store.engine, wasm_path)

    instance = Instance(store, module, [])
    sum_func = instance.exports(store)["add"]
    result1 = sum_func(store, 2, 2)

    # from wasmer import engine, wasi, Store, Module, ImportObject, Instance
    # from wasmer_compiler_cranelift import Compiler
    # import interfaces.applib
    # with open(os.path.join(interfaces.applib.__path__[0], "test_zig.wasm"), "rb") as f:
    #    wasm_bytes = f.read()
    #    store = Store(engine.Universal(Compiler))
    #    module = Module(store, wasm_bytes)
    #    wasi_env = (
    #        wasi.StateBuilder("wasi_test_program")
    #        .argument("--test")
    #        .environment("COLOR", "true")
    #        .environment("APP_SHOULD_LOG", "false")
    #        .map_directory("the_host_current_dir", ".")
    #        .finalize()
    #    )
    #    module = Module(store, wasm_bytes)
    #    instance = Instance(module)
    #    sum = instance.exports.add
    #    result4 = sum(2, 2)

    title2 = "json_test"
    result2 = nim_ext.ext.json_test(x=100, y=300, value="Hello world!")

    title3 = "int_test"
    result3 = nim_ext.ext.int_test(10)

    title4 = "float_test"
    result4 = nim_ext.ext.float_test(100.0)

    title5 = "string_test"
    result5 = nim_ext.ext.string_test(b"Hello")
    title6 = "string_test_from_utf"
    result6 = nim_ext.ext.string_test_str("Hello")

    title7 = "void_test"
    result7 = nim_ext.ext.void_test()

    title8 = "string_int_test"
    result8 = nim_ext.ext.string_int_test("string int test")

    title9 = "json_test2"
    result9 = nim_ext.ext.json_test2()

    import nimext

    title10 = "nimext test"
    result10 = nimext.greet("world") + " from nimext"

    title11 = "llvm assembly"
    result11 = csum(2, 2)

    return {
        "object_list": (
            (title1, result1),
            (title2, result2),
            (title3, result3),
            (title4, result4),
            (title5, result5),
            (title6, result6),
            (title7, result7),
            (title8, result8),
            (title9, result9),
            (title10, result10),
            (title11, result11),
        )
    }
