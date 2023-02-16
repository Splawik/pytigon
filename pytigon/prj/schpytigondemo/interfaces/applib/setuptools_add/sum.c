#define PY_SSIZE_T_CLEAN
#include <Python.h>

PyObject *sum(PyObject *self, PyObject *args)
{
    long a, b;

    if (!PyArg_ParseTuple(args, "ll", &a, &b))
        return NULL;
    return PyLong_FromLong(a + b);
}

static struct PyMethodDef methods[] = {
    {"sum", (PyCFunction)sum, METH_VARARGS},
    {NULL, NULL}};

static struct PyModuleDef zigmodule = {
    PyModuleDef_HEAD_INIT,
    "sum",
    NULL,
    -1,
    methods};

PyMODINIT_FUNC PyInit_c_sum(void)
{
    return PyModule_Create(&zigmodule);
}
