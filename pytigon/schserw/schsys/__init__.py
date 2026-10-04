Name = "schsys"
Title = "System tools"
ModuleName = "System"
ModuleTitle = "System"
Perms = True
Index = "index"
Urls = ()

# Import for its side effect: registers the security system checks. Django does
# not auto-import app ``checks`` modules, and Pytigon builds its AppConfigs
# dynamically, so the import happens here.
from . import checks  # noqa: E402,F401  (must follow nothing; side effect only)

