import os
import json
from django.conf import settings

from dulwich import porcelain
from dulwich.repo import Repo
from dulwich import index

from schwiki.models import WikiConf, Page

from pytigon_lib.schtools.wiki import wiki_from_str


class WikiGit:
    def __init__(self, wikiconf_item):
        self.git_repository = wikiconf_item.git_repository
        if self.git_repository and "=>" in self.git_repository:
            x = self.git_repository.split("=>")
            self.git_repository = x[0]
            self.module = x[1]
        else:
            self.module = "main"
        self.wikiconf_item = wikiconf_item
        git_base_path = os.path.join(
            settings.DATA_PATH, settings.PRJ_NAME, "git_repositories"
        )
        if not os.path.exists(git_base_path):
            os.makedirs(git_base_path)
        self.git_subject_path = os.path.join(git_base_path, wikiconf_item.subject)
        if not os.path.exists(self.git_subject_path):
            os.makedirs(self.git_subject_path)
        self.git_path = os.path.join(self.git_subject_path, ".git")

    def _pull(self):
        if os.path.exists(self.git_path):
            repo = Repo(self.git_subject_path)
            try:
                print(self.git_repository)
                remote_refs = porcelain.fetch(repo, self.git_repository)
                repo[b"HEAD"] = remote_refs.refs[b"refs/heads/master"]
                index_file = repo.index_path()
                tree = repo[b"HEAD"].tree
                index.build_index_from_tree(
                    repo.path, index_file, repo.object_store, tree
                )
            except Exception as e:
                print("git pull error: ", str(e))
        else:
            try:
                print(self.git_repository)
                porcelain.clone(self.git_repository, self.git_subject_path)
            except Exception as e:
                print("git clone error: ", str(e))

    def _push(self):
        repo = Repo(self.git_subject_path)
        paths = []
        for root, dirs, files in os.walk(self.git_subject_path):
            if not ".git" in root.replace("\\", "/").split("/"):
                for file in files:
                    paths.append(os.path.join(root, file))
        porcelain.add(repo, paths)
        try:
            porcelain.commit(repo, "Automatic sychnronization with schportal")
            porcelain.push(repo, self.git_repository, b"master")
        except Exception as e:
            print("git push error: ", str(e))

    def wiki_pull(self, erase_previous_data=False, subfolders_in_main_menu=False):
        self._pull()

        if erase_previous_data:
            Page.objects.filter(subject=self.wikiconf_item.subject).delete()
            print("Data from subject: %s deleted!" % self.wikiconf_item.subject)
        else:
            Page.objects.filter(subject=self.wikiconf_item.subject).update(latest=True)

        conf = {}
        config_path = os.path.join(self.git_subject_path, "conf.json")
        if os.path.exists(config_path):
            with open(config_path, "rt") as f:
                conf = json.loads(f.read())

        l = len(self.git_subject_path)
        for root, dirs, files in os.walk(self.git_subject_path):
            if not ".git" in root.replace("\\", "/").split("/"):
                file_path = root[l + 1 :]
                for file in files:
                    if file == "config.json":
                        continue

                    if (
                        file[2] == "."
                        and file[0] >= "0"
                        and file[0] <= "9"
                        and file[1] >= "0"
                        and file[1] <= "9"
                    ):
                        menu_position = int(file[:2])
                        description = (
                            file.split(".", 1)[1]
                            .strip()
                            .replace(".imd", "")
                            .replace(".md", "")
                        )
                    else:
                        menu_position = None
                        description = file.replace(".imd", "").replace(".md", "")

                    name = wiki_from_str(description)
                    old_page = Page.objects.filter(
                        subject=self.wikiconf_item.subject, published=True, name=name
                    ).first()
                    if old_page:
                        old_page.published = False
                        try:
                            old_page.save()
                        except Exception as e:
                            print("old page save error: ", str(e))
                        obj = old_page
                        obj.pk = None
                    else:
                        obj = Page()
                    obj.subject = self.wikiconf_item.subject
                    obj.name = name
                    obj.description = description
                    n = 0
                    if menu_position and file_path:
                        if "." in file_path:
                            x = file_path.split("/")
                            y = []
                            base = 1000000
                            for item in x:
                                if len(item) > 3 and item[2] == ".":
                                    n += int(item[:2]) * base
                                    y.append(item[3:].strip())
                                else:
                                    y.append(item)
                                base /= 100
                        else:
                            y = file_path.split("/")
                        if subfolders_in_main_menu:
                            if len(y)>1:
                                obj.menu = y[0] + "/" + y[1]
                            else:
                                obj.menu = y[0]
                        else:
                            obj.menu = self.module + "/" + y[0]

                    if menu_position:
                        obj.menu_position = menu_position + n

                    obj.prj_name = settings.PRJ_NAME

                    with open(os.path.join(root, file), "rt") as f:
                        obj.content_src = f.read()
                    if file_path:
                        obj.json_path = file_path + "/" + file
                    else:
                        obj.json_path = file

                    obj.published = True
                    obj.latest = True

                    if name in conf:
                        for key, value in conf[name].items():
                            if key == "json_data":
                                for key2, value2 in value.items():
                                    setattr(obj, "json_" + key2, value2)
                            else:
                                setattr(obj, key, value)
                    try:
                        obj.save()
                    except Exception as e:
                        print("obj save error: ", str(e))

    def wiki_push(self):
        if not os.path.exists(self.git_path):
            self._pull()
        conf = {}
        objects_list = Page.objects.filter(
            subject=self.wikiconf_item.subject, published=True
        )
        for obj in objects_list:
            if obj.content_src:
                if obj.menu_position:
                    name = "%02d. " % (obj.menu_position % 100)
                else:
                    name = ""
                if obj.description:
                    name += obj.description
                else:
                    name += obj.name
                if obj.menu:
                    menu_path = obj.menu.split("/")
                    if len(menu_path) > 1:
                        menu_path = menu_path[1:]
                else:
                    menu_path = []

                file_name = obj.json_path

                if file_name:
                    if "/" in file_name:
                        file_path = os.path.join(
                            self.git_subject_path, file_name.rsplit("/", 1)[0]
                        )
                    else:
                        file_path = self.git_subject_path
                    file_name = os.path.join(self.git_subject_path, file_name)
                else:
                    if obj.menu_position > 1000000:
                        menu_path[0] = "%02d" % (obj.menu_position // 1000000)
                    file_path = os.path.join(self.git_subject_path, *menu_path)
                    file_name = os.path.join(file_path, name)

                if not os.path.exists(file_path):
                    os.makedirs(file_path)

                with open(file_name, "wt") as f:
                    f.write(obj.content_src)

                obj_conf = {}
                obj_conf["base_template"] = obj.base_template
                obj_conf["rights_group"] = obj.rights_group
                obj_conf["menu_icon"] = obj.menu_icon
                obj_conf["menu_icon_size"] = obj.menu_icon_size
                obj_conf["operator"] = obj.operator
                if obj.json_data:
                    obj_conf["json_data"] = obj.json_data
                else:
                    obj_conf["json_data"] = {}
                obj_conf["json_data"].pop("path", None)
                if obj.operator:
                    obj_conf["json_data"]["operator"] = obj.operator
                conf[obj.name] = obj_conf
        with open(os.path.join(self.git_subject_path, "conf.json"), "wt") as f:
            f.write(json.dumps(conf))

        self._push()
