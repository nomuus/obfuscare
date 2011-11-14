# ------------------------------------------------------------------------------
# dobfuscare.py
# www.nomuus.com
# -------------------------------------------------------[ Revision History ]----
# username/YYYY-MM-DD/version    /
# -------------------------------
# nomuus/2011-11-12/0.0.501.2
#     - Removed example generation code.
# nomuus/2011-11-12/0.0.501.1
#     - Public beta release.
# nomuus/2010-07-01/0.0.0.1
#     - Initial development release.

###########################################################################

import sys
from base64 import b64decode
from nomcom import file_exists
from os.path import basename
from re import compile, search

###########################################################################

__version__ = "0.0.501.2"
__status__ = "BETA"
__author__ = "nomuus"
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
__email__ = "mu*nre*txemusu*da"[::-1].replace('*', '') + "!@#$%^&*()"[1] + "nomuus" + "+..com"[2:]
__company__ = 'www.nomuus.com'
__description__ = 'Decoder for obfuscated files.'


stderr = sys.stderr
stdout = sys.stdout
BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
RE_NOTBASE64 = compile("[^" + BASE64_CHARS + "]+")

###########################################################################

def usage():
    f = basename(sys.argv[0])
    stdout.write("Dobfuscare %s - Decoder for obfuscated files.\n" % __version__)
    copyright = __copyright__.split('\n')[0].rstrip("\r\n")
    stdout.write("%s\n\n" % copyright)
    stdout.write("%s obfuscatedfile indicefile\n\n" % f)
    stdout.write("Examples\n%s example_obfuscated.txt example_indices.txt\n" % f)
    stdout.write("%s example_obfuscated-base64.txt example_indices.txt\n" % f)
    
###########################################################################

def main(argv):
    arg_len = len(argv)
    
    if arg_len != 3:
        usage()
        sys.exit(-1)
        
    obfile = file_exists(argv[1])
    idfile = file_exists(argv[2])
    
    if not obfile:
        stderr.write("%s does not exist.\n" % argv[1])
        sys.exit(1)
    if not idfile:
        stderr.write("%s does not exist.\n" % argv[2])
        sys.exit(1)
    
    with open(obfile, 'r') as f:
        tmp = f.read()
    if tmp.count('\n') > 1 and tmp.count(' ') > 0 and search(RE_NOTBASE64, tmp):
        # Most likely not base64
        obdata = tmp
    else:
        obdata = b64decode(tmp)

    if not obdata:
        stderr.write("Error parsing %s.\n" % obfile)
        sys.exit(-2)
        
    with open(idfile, 'r') as f:
        iddata = [x.strip("\r\n") for x in f.readline().split(" ")]

    if not isinstance(iddata, list):
        stderr.write("Error parsing %s.\n" % idfile)
        sys.exit(2)
        
    obdata_len = len(obdata)
    for id in iddata:
        if not id.isdigit():
            stderr.write("%s is not a valid index number.\n" % id)
            sys.exit(3)
        x = int(id)
        if x >= 0 and x < obdata_len:
            stdout.write("%s" % obdata[x])
        else:
            print obdata_len
            stderr.write("%s index does not exist in ofuscated file %s.\n" % (id, obfile))
            sys.exit(-3)

###########################################################################

if __name__ == "__main__":
    main(sys.argv)