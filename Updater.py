#!/usr/bin/env python
# Written by: DGC

"""
This is a module for checking if there is a new version of the software.
"""

# python imports
import threading
import urllib2
import xml.dom.minidom

# local imports
import Version

#==============================================================================
class Updater(object):

    def __init__(self):
        self.finished = False
        self.thread = threading.Thread(target=self.check_update)
        self.thread.start()

    def check_update(self):
        self.finished = False
        self.update_available = new_version_available()
        self.finished = True

#==============================================================================
def new_version_available():
    """
    Checks this version and checks the download site for a new version.
    """
    return current_version() < available_version()

#==============================================================================
def current_version():
    """
    Returns the version of the software being run.
    """
    # in future this will work out the os and return the appropriate one
    return Version.WINDOWS_VERSION

#==============================================================================
def get_version_from_xml(xml_string):
    """
    This takes a string of xml of the form
    <Versions>
      <Windows>1</Windows>
    </Versions>
    and returns the (float) value of the Windows node.
    """
    version_xml = xml.dom.minidom.parseString(xml_string)
    version =  version_xml.getElementsByTagName("Windows")[0].firstChild
    return float(version.nodeValue)

#==============================================================================
def get_version_xml():
    """
    Returns a string containing the xml from Version.xml

    Will raise a urllib2.HTTPError if the file not found.
    """
    url = "https://bitbucket.org/davidcorne/markdown-editor-downloads/raw/tip/Version.xml"
    return urllib2.urlopen(url).read()

#==============================================================================
def available_version():
    """
    Returns the internal version number which is available to download.
    """
    try:
        response = get_version_xml()
    except urllib2.HTTPError:
        return 0
    return get_version_from_xml(response)

#==============================================================================
if (__name__ == "__main__"):
    pass
