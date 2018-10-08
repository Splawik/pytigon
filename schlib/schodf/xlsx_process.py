from openpyxl import load_workbook, Workbook

def transform_xlsx(stream_in, stream_out, transform_list):
    tables = {}
    first_ws = False
    if stream_in:
        wb = load_workbook(stream_in)
    else:
        wb = Workbook()
        first_ws = True
    
    ws_name_prev = None
    ws = None
    

    def set_sheet(name):
        nonlocal ws_name_prev, wb, ws
        if name != ws_name_prev:
            if not ws_name_prev and first_ws:
                ws = wb.active
                ws.title = name
            try:
                ws = wb[name]
            except:
                ws = wb.create_sheet(name) 
            ws_name_prev = name

    for _pos in transform_list:
        pos = list(_pos)
        key = pos[0]
        
        if type(key)=='str' and '=>' in key:
            x = key.split('=>')
            ws_name = x[0] if x[0] else 'data'
            set_sheet(ws_name)            
            ws.append(pos[1:])
            
        elif type(key)=='str' and '/' in key:
            x = key.split('/')
            ws_name = x[0] if x[0] else 'data'
            set_sheet(ws_name)            
            if ':' in x[1]:
                xx = x[1].split(':')
            else:
                xx = ( x[1], pos[1], )
            
            ws[xx[0]] = xx[1]   
            
        else:
            ws_name = 'data'
            set_sheet(ws_name)
            ws.append(pos)
            
    wb.save(stream_out)
