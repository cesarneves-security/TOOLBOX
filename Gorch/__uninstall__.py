import os
choice = "y"
run = os.system
if str(choice)=='Y' or str(choice)=='y':
    run('rm -r /usr/share/Gorch ')
    run('rm /usr/bin/Gorch ')
    print('[!] FERRAMENTA REMOVIDA COM SUCESSO!')

