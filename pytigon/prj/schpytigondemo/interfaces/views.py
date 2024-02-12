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

    title1 = "cffi test"
    from interfaces.applib.cffi_add import lib as cffitestlib

    result1 = cffitestlib.add(2, 2)

    title2 = "zig ctypes test"
    import ctypes

    lib = ctypes.CDLL("interfaces/applib/libzig_add.so")
    result2 = lib.add(2, 2)

    title3 = "setuptools test"
    # try:
    import c_sum

    result3 = c_sum.sum(2, 2)
    # except:
    #    print("c_sum demo error")

    title4 = "wasm from zig"
    import interfaces.applib
    from wasmtime import Store, Module, Instance, Func, FuncType

    wasm_path = os.path.join(interfaces.applib.__path__[0], "test_zig.wasm")

    store = Store()
    module = Module.from_file(store.engine, wasm_path)

    instance = Instance(store, module, [])
    sum_func = instance.exports(store)["add"]
    result4 = sum_func(store, 2, 2)

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

    title5 = "llvm test"
    result5 = csum(1, 3)

    return {
        "object_list": (
            (title1, result1),
            (title2, result2),
            (title3, result3),
            (title4, result4),
            (title5, result5),
        )
    }
