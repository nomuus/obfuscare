"""nomuus common python function file

Created by nomuus <"".join(["adus@um.ex", "te@rn.um"]).replace(".", "").replace("@", "") + "@" + "nomuus.com">
"""

__version__ = "1.0"

__copyright__ = """Copyright (c) 2010-2011, nomuus. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.

    * Neither the name of the copyright holder nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

###########################################################################

from os.path import isdir, isfile
from os import getcwd, sep

###########################################################################

def _file_exists(file):
    """Determines if a fiile exists.

    Determines if a file exists in either the specified path or
    within the current working directory.
    
    Args:
        file: path to a file, either absolute path or relative
              to the current working directory.
        
    Returns:
        If exists, returns the absolute file path or the relative
        file path to the current working directory.
        
        If the file is not found or the file specified is not
        a basestring then a blank string, "", is returned.
    """
    if not isinstance(file, basestring):
        return ""
    if isfile(file):
        return file
    elif isfile(getcwd() + sep + file):
        return osfile(getcwd() + sep + file)
    else:
        return ""

###########################################################################

def _dir_exists(directory):
    """Determines if a directory exists.

    Determines if a directory exists in either the specified path or
    within the current working directory.
    
    Args:
        directory: path to a directory, either absolute path or relative
                   to the current working directory.
        
    Returns:
        If exists, returns the absolute path or relative path to the
        current working directory.
        
        If the directory is not found or the directory specified is not
        a basestring then a blank string, "", is returned.
    """
    if not isinstance(directory, basestring):
        return ""
    if isdir(directory):
        return directory
    elif isdir(getcwd() + sep + directory):
        return isdir(getcwd() + sep + directory)
    else:
        return ""
        
###########################################################################
## Wrapper functions

def dir_exists(dir):
    return _dir_exists(dir)

def directory_exists(dir):
    return _dir_exists(dir)

def file_exists(file):
    return _file_exists(file)

###########################################################################