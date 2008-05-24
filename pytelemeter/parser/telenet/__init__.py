"""
    pytelemeter parsers for Telenet
"""

def parsers():
    parsers=[]
    try:
        import telemeter4tools
        parsers.append(telemeter4tools.Telemeter4ToolsParser())
    except:
        pass # SOAPpy is probably not installed, silent skip it
    #try:
    #    import flashxml
    #    parsers.append(flashxml.FlashXMLParser())
    #except:
    #    pass # Probably, neither cookielib nor ClientCookie is available
    return parsers
