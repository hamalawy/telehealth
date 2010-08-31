import traceback

def ERROR(errortype="***System Error***"):
    print errortype
    print traceback.format_exc()
