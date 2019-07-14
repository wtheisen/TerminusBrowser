from inspect import currentframe
def INITDEBUG():
    with open('debug.log', 'a+') as f:
        f.write('Beginning new run\n\n')

def DEBUG(data):
    cF = currentframe()

    with open('debug.log', 'a+') as f:
        f.write(f'{str(cF.f_back.f_lineno)}:\n' + repr(data) + '\n')
