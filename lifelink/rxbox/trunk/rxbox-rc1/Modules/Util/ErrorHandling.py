import traceback

def ERROR(comment=''):
    return '%s\n%s'%(comment,traceback.format_exc())
