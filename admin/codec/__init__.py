import sys


def getCodec (codec):
    #+++ here i should i an exception handler
    codec_module = __import__ ( codec , globals () , locals () , ["main"] , -1)
    reload (codec_module)
    
    obj = codec_module.main.codec ()
    return obj 


