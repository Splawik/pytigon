import otkernel.applib.public_api as pub
import otkernel.applib.private_api as prv

from otkernel.applib.core_api import API

API.register_api("pub", pub)
API.register_api("prv", prv)
