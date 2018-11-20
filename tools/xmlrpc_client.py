import xmlrpc.client
with xmlrpc.client.ServerProxy('http://localhost:7080/') as proxy:
    print('next tasks:')
    x = proxy.show_tasks()
    for pos in x:
        print(f"{pos[1][:16].replace('T', ' ')}: {pos[0]}({pos[2]},{pos[3]})")
    print('current tasks:')
    x = proxy.show_current_tasks()
    for pos in x:
        print(pos)
