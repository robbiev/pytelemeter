/* -- THIS FILE IS GENERATE - DO NOT EDIT *//* -*- Mode: C; c-basic-offset: 4 -*- */

#include <Python.h>



#line 3 "src/eggtray/trayicon.override"
#include <Python.h>
#include "pygobject.h"
#include "eggtrayicon.h"
#line 12 "src/eggtray/trayicon.c"


/* ---------- types from other modules ---------- */
static PyTypeObject *_PyGtkPlug_Type;
#define PyGtkPlug_Type (*_PyGtkPlug_Type)


/* ---------- forward type declarations ---------- */
PyTypeObject PyEggTrayIcon_Type;


/* ----------- EggTrayIcon ----------- */

static int
_wrap_egg_tray_icon_new(PyGObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { "name", NULL };
    char *name;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s:EggTrayIcon.__init__", kwlist, &name))
        return -1;
    self->obj = (GObject *)egg_tray_icon_new(name);

    if (!self->obj) {
        PyErr_SetString(PyExc_RuntimeError, "could not create EggTrayIcon object");
        return -1;
    }
    pygobject_register_wrapper((PyObject *)self);
    return 0;
}

static PyObject *
_wrap_egg_tray_icon_cancel_message(PyGObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { "id", NULL };
    int id;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "i:EggTrayIcon.cancel_message", kwlist, &id))
        return NULL;
    egg_tray_icon_cancel_message(EGG_TRAY_ICON(self->obj), id);
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
_wrap_egg_tray_icon_get_orientation(PyGObject *self)
{
    int ret;

    ret = egg_tray_icon_get_orientation(EGG_TRAY_ICON(self->obj));
    return PyInt_FromLong(ret);
}

static PyMethodDef _PyEggTrayIcon_methods[] = {
    { "cancel_message", (PyCFunction)_wrap_egg_tray_icon_cancel_message, METH_VARARGS|METH_KEYWORDS },
    { "get_orientation", (PyCFunction)_wrap_egg_tray_icon_get_orientation, METH_NOARGS },
    { NULL, NULL, 0 }
};

PyTypeObject PyEggTrayIcon_Type = {
    PyObject_HEAD_INIT(NULL)
    0,					/* ob_size */
    "pytrayicon.TrayIcon",			/* tp_name */
    sizeof(PyGObject),	        /* tp_basicsize */
    0,					/* tp_itemsize */
    /* methods */
    (destructor)0,			/* tp_dealloc */
    (printfunc)0,			/* tp_print */
    (getattrfunc)0,	/* tp_getattr */
    (setattrfunc)0,	/* tp_setattr */
    (cmpfunc)0,		/* tp_compare */
    (reprfunc)0,		/* tp_repr */
    (PyNumberMethods*)0,     /* tp_as_number */
    (PySequenceMethods*)0, /* tp_as_sequence */
    (PyMappingMethods*)0,   /* tp_as_mapping */
    (hashfunc)0,		/* tp_hash */
    (ternaryfunc)0,		/* tp_call */
    (reprfunc)0,		/* tp_str */
    (getattrofunc)0,			/* tp_getattro */
    (setattrofunc)0,			/* tp_setattro */
    0,					/* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    NULL, 				/* Documentation string */
    (traverseproc)0,			/* tp_traverse */
    (inquiry)0,			/* tp_clear */
    (richcmpfunc)0,	/* tp_richcompare */
    offsetof(PyGObject, weakreflist),             /* tp_weaklistoffset */
    (getiterfunc)0,		/* tp_iter */
    (iternextfunc)0,	/* tp_iternext */
    _PyEggTrayIcon_methods,			/* tp_methods */
    0,					/* tp_members */
    0,		       	/* tp_getset */
    NULL,				/* tp_base */
    NULL,				/* tp_dict */
    (descrgetfunc)0,	/* tp_descr_get */
    (descrsetfunc)0,	/* tp_descr_set */
    offsetof(PyGObject, inst_dict),                 /* tp_dictoffset */
    (initproc)_wrap_egg_tray_icon_new,		/* tp_init */
};



/* ----------- functions ----------- */

PyMethodDef pytrayicon_functions[] = {
    { NULL, NULL, 0 }
};

/* intialise stuff extension classes */
void
pytrayicon_register_classes(PyObject *d)
{
    PyObject *module;

    if ((module = PyImport_ImportModule("gtk")) != NULL) {
        PyObject *moddict = PyModule_GetDict(module);

        _PyGtkPlug_Type = (PyTypeObject *)PyDict_GetItemString(moddict, "Plug");
        if (_PyGtkPlug_Type == NULL) {
            PyErr_SetString(PyExc_ImportError,
                "cannot import name Plug from gtk");
            return;
        }
    } else {
        PyErr_SetString(PyExc_ImportError,
            "could not import gtk");
        return;
    }


#line 143 "src/eggtray/trayicon.c"
    pygobject_register_class(d, "EggTrayIcon", EGG_TYPE_TRAY_ICON, &PyEggTrayIcon_Type, Py_BuildValue("(O)", &PyGtkPlug_Type));
}
