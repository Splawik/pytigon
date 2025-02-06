from .editor import init_control as init_control_edit
from .grid import init_control as init_control_grid

def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    app.register_ctrl_process_fun('ctrlstyledtext', init_control_edit)
    app.register_ctrl_process_fun('ctrlgrid', init_control_grid)
    app.register_ctrl_process_fun('ctrltable', init_control_grid)
