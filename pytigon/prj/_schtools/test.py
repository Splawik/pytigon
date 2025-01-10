import os


def gen_file_list(prj_path):
    object_list = os.walk(prj_path)

    l = []
    for root, dirs, files in object_list:
        if ".git" not in root and "__pycache__" not in root:
            for file_name in files:
                if file_name.endswith(".pyc") or file_name.endswith(".pyo"):
                    continue
                l.append(os.path.join(root, file_name))
    return l


def gen_list_for_delete(l_new, l_old):
    l = []
    for item in l_old:
        if item not in l_new:
            l.append(item)
    return l


def gen_list_for_new(l_new, l_old):
    l = []
    for item in l_new:
        if item not in l_old:
            l.append(item)
    return l


def gen_list_for_update(l_new, l_old):
    l = []
    for item in l_new:
        if item in l_old:
            l.append(item)
    return l


l = gen_file_list("/home/sch/prj/pytigon/pytigon/prj/_schtools/")

for item in l:
    print(item)
