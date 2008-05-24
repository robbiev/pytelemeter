"""
    pytelemeter parsers for Scarlet.be
"""

def parsers():
    parsers=[]
    try:
        import web
        parsers.append(web.ScarletWebParser())
    except:
        pass # wtf?
    return parsers
