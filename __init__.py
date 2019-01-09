def main():
    import importlib
    import os
    cwd = os.path.dirname(os.path.abspath(__file__))

    files = os.listdir(cwd)

    for i in files:
        if not i.startswith('_') and i.endswith('.py'):
            m = '.' + i[:-3]

            # get a handle on the module
            mdl = importlib.import_module(m, __package__)

            # is there an __all__?  if so respect it
            if "__all__" in mdl.__dict__:
                names = mdl.__dict__["__all__"]
            else:
                # otherwise we import all names that don't begin with _
                names = [x for x in mdl.__dict__ if not x.startswith("_")]

            # now drag them in
            globals().update({k: getattr(mdl, k) for k in names})
            globals().pop(i[:-3])

main()
globals().pop('main')


