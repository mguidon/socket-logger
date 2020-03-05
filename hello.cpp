#include <Python.h>
#include <iostream>

static PyObject *
print_stdout(PyObject *self, PyObject *args)
{
    const char *what;

    if (!PyArg_ParseTuple(args, "s", &what))
    {
        return NULL;
    }
    
    std::cout << "c++ stdout says: " << what << std::endl;

    Py_RETURN_NONE;
}

static PyObject *
print_stderr(PyObject *self, PyObject *args)
{
    const char *what;

    if (!PyArg_ParseTuple(args, "s", &what))
    {
        return NULL;
    }
    
    std::cerr << "c++ stderr says: " << what << std::endl;

    Py_RETURN_NONE;
}

static PyMethodDef HelloMethods[] = {
    {"stdout", print_stdout, METH_VARARGS, "Write to stdout"},
    {"stderr", print_stderr, METH_VARARGS, "Write to stderr"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef hello =
{
    PyModuleDef_HEAD_INIT,
    "hello",     /* name of module */
    "",          /* module documentation, may be NULL */
    -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    HelloMethods
};

PyMODINIT_FUNC PyInit_hello(void)
{
    return PyModule_Create(&hello);
}