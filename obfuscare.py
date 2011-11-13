#!/usr/bin/env python2.7

# ------------------------------------------------------------------------------
# obfuscare.py
# www.nomuus.com
# -------------------------------------------------------[ Revision History ]----
# username/YYYY-MM-DD/version    /
# -------------------------------
# nomuus/2011-11-12/0.0.500.1
#     - Public beta release.
# nomuus/2011-10-10/0.0.467.3
#     - Added additional meta-data.
#     - Minor formatting adjustments.
# nomuus/2011-01-03/0.0.187.2
#     - Updated output formatting.
#     - Added argument parsing.
# nomuus/2010-07-01/0.0.0.1
#     - Initial development release.

import sys
from base64 import b64encode
from nomcom import _file_exists
from os.path import basename
from random import shuffle, randint
from re import sub
from time import strftime, localtime

###########################################################################

__version__ = "0.0.500.1"
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
__description__ = 'Provides basic text obfuscation.'


HEADER_MAPPING = """ __  __                   _             
|  \/  | __ _ _ __  _ __ (_)_ __   __ _ 
| |\/| |/ _` | '_ \| '_ \| | '_ \ / _` |
| |  | | (_| | |_) | |_) | | | | | (_| |
|_|  |_|\__,_| .__/| .__/|_|_| |_|\__, |
             |_|   |_|            |___/ """

HEADER_OBFUSCATION = """  ___  _      __                      _   _             
 / _ \| |__  / _|_   _ ___  ___  __ _| |_(_) ___  _ __  
| | | | '_ \| |_| | | / __|/ __|/ _` | __| |/ _ \| '_ \ 
| |_| | |_) |  _| |_| \__ \ (__| (_| | |_| | (_) | | | |
 \___/|_.__/|_|  \__,_|___/\___|\__,_|\__|_|\___/|_| |_|"""

HEADER_INDICES = """ ___           _ _               
|_ _|_ __   __| (_) ___  ___ ___ 
 | || '_ \ / _` | |/ __|/ _ | __|
 | || | | | (_| | | (__|  __|__ \ 
|___|_| |_|\__,_|_|\___|\___|___/"""

ARG_NUM_MAPPINGS = ["-n", "--num-mappings"]
ARG_OBFUSCATE_TEXT = ["-k", "--key-file", "--code-book"]
INDICE_SEP = " "
FILLER = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890./<>?;':\"[]{}\\|`~!@#$%^&*()-_=+ \r\n\t"
B_CASE_SENSITIVE = True
stdout = sys.stdout
stderr = sys.stderr

###########################################################################

def repl(m):
    inner_word = list(m.group(0))
    shuffle(inner_word)
    return "".join(inner_word)

###########################################################################

def obfuscate(text):
    """Obfuscates input text with other text.
    
    Generates a pseudorandom buffer of text and shuffles characters from
    the original text into the buffer.  This is essentially a codebook
    generator.
    
    Args:
        text: String containing original plaintext.
        
    Returns:
        This returns a pseudorandom buffer / codebook.
        
        If not a string, then a blank string, "", is returned.
    """
    
    if not isinstance(file, basestring):
        return ""
    
    filler = FILLER
    tmp_text = ""
    tmp_text2 = filler
    i = 0
    len_f = len(filler)
    len_t = len(text)
    
    # ""random"" mapping.
    while i < len_t:
        len_t2 = len(tmp_text2)
        tmp_text = (tmp_text + (filler[randint(0, len_f - 1)] * randint(2, 6)) +
                    text[i] + filler[randint(0, len_f - 1)] + tmp_text2[randint(0, len_t2 - 1)] +
                    text[randint(0, len_t - 1)] + text[i] * randint(2, 4))
        tmp_text2 = tmp_text
        i = i + 1
    return sub(r".*", repl, tmp_text)

###########################################################################
    
def get_obfuscated_indices(c, obfuscated, b_case_sensitive=False):
    i = 0
    list1 = []
    b_add = False
    # TODO: Consider making a generator
    while i < len(obfuscated):
        if b_case_sensitive:
            if c == obfuscated[i]:
                b_add = True
            else:
                b_add = False
        else:
            if c.lower() == obfuscated[i].lower():
                b_add = True
            else:
                b_add = False
                
        if b_add:
            if not c in list1:
                list1.append(i)
        i = i + 1
    return list1

###########################################################################

def build_text_obfuscation_map(text, obfuscated_text, b_case_sensitive=False):
    i = 0
    text_obfusc_list = []
    tmp_list = []
    text_list = []
    not_found_list = []
    b_error = False
    # TODO: Consider making a generator
    while i < len(text):
        t = text[i]
        
        if i == 0:
            b_first = True
        else:
            b_first = False
        
        if b_first:
            text_list.append(t)
            tmp_list = get_obfuscated_indices(t, obfuscated_text, b_case_sensitive)
            if tmp_list:
                text_obfusc_list.append([t, tmp_list])
                del tmp_list
            else:
                #sys.stderr.write("Error, char %s does not exist in obfuscated list.\n" % t)
                not_found_list.append(t)
                b_error = True
                #break
        else:
            if not t in text_list:
                text_list.append(t)
                tmp_list = get_obfuscated_indices(t, obfuscated_text, b_case_sensitive)
                if tmp_list:
                    text_obfusc_list.append([t, tmp_list])
                    del tmp_list
                else:
                    #sys.stderr.write("Error, char does not exist in obfuscated list.\n")
                    not_found_list.append(t)
                    b_error = True
                    #break
        i = i + 1
    
    if b_error:
        return ["error", not_found_list]
    else:
        return text_obfusc_list

###########################################################################

def usage():
    f = basename(sys.argv[0])
    stdout.write("Obfuscare %s - Provides basic text obfuscation.\n" % __version__)
    copyright = __copyright__.split('\n')[0].rstrip("\r\n")
    stdout.write("%s\n\n" % copyright)
    stdout.write("%s file.txt [options]\n\n" % f)
    stdout.write("Options\n")
    stdout.write("-n, --num-mappings    Number of mappings to generate.\n")
    stdout.write("                      Defaults to 1 if omitted.\n")
    stdout.write("-k, --key-file,       Key obfuscation file; indices mapped to this file.\n")
    stdout.write("    --code-book       Defaults to random obfuscation plus original text.\n")
    stdout.write("\n")
    stdout.write("Examples\n")
    stdout.write("%s myfile.txt > myfile_output.txt\n" % f)
    stdout.write("%s myfile.txt -n 5 > myfile_output.txt\n" % f)
    stdout.write("%s myfile.txt -n 2 -k bill_of_rights.txt > myfile_output.txt\n" % f)
    stdout.write("%s myfile.txt -k bible.txt > myfile_output.txt\n" % f)

###########################################################################

def banner():
    stdout.write("Generated with Obfuscare %s\n" % __version__)
    stdout.write("%s\n" % __copyright__)
    stdout.write("www.nomuus.com\n\n\n")
    stdout.write("YYYYmmddHHMMSS - %s\n" % strftime("%Y%m%d%H%M%S", localtime()))

###########################################################################

def arg_parser(args):
    kwargs = {"file": _file_exists(args[1]),
              "mappings": "",
              "keyfile": ""}
    if not kwargs["file"]:
        stderr.write("Input file does not exist.\n")
        sys.exit(2)
    del args[0:2]
    
    arg_num = ""
    arg_ob = ""
    arg_len = len(args)
    if arg_len > 2 or arg_len < 7:
        for arg in args:
            if arg_num and arg_ob:
                break
            
            if ARG_NUM_MAPPINGS.count(arg) > 1:
                usage()
                sys.exit(-1)
            if ARG_OBFUSCATE_TEXT.count(arg) > 1:
                usage()
                sys.exit(-1)
            
            arg_index = args.index(arg)
            if arg in ARG_NUM_MAPPINGS:
                if not arg_num:
                    if arg_index < arg_len - 1:
                        arg_num = args[arg_index + 1]
                    else:
                        stderr.write("Mappings argument is invalid.\n")
                        sys.exit(3)
                else:
                    stderr.write("Too many mappings specified.\n")
                    sys.exit(-1)
            elif arg in ARG_OBFUSCATE_TEXT:
                if not arg_ob:
                    if arg_index < arg_len - 1:
                        arg_ob = args[arg_index + 1]
                    else:
                        stderr.write("Obfuscation file argument invalid.\n")
                        sys.exit(3)
                else:
                    stderr.write("Too many obfuscation files specified.\n")
                    sys.exit(-1)
            else:
                if arg_num:
                    if arg_index - args.index(arg_num) == 0:
                        continue
                if arg_ob:
                    if arg_index - args.index(arg_ob) == 0:
                        continue
                usage()
                stderr.write("Specified arguments are invalid.\n")
                sys.exit(-1)
    else:
        usage()
        stderr.write("Specified arguments are invalid.\n")
        sys.exit(3)
    
    # Optional number of mappings.
    if arg_num:
        if not arg_num.isdigit():
            stderr.write("Mappings argument is invalid.\n")
            sys.exit(3)
        else:
            kwargs["mappings"] = int(arg_num)
    else:
        kwargs["mappings"] = 1
    
    # Optional key obfuscation file.
    if arg_ob:
        kwargs["keyfile"] = _file_exists(arg_ob)
        if not kwargs["keyfile"]:
            sys.stderr.write("Key obfuscation file does not exist.\n")
            sys.exit(2)
            
    return kwargs

###########################################################################
    
def main(argv):    
    if len(argv) < 2 or len(argv) > 6:
        usage()
        sys.exit(1)
    
    # Argument Parser
    kwargs = arg_parser(argv)
    
    # Required input plain-text file.
    with open(kwargs["file"], 'r') as f:
        text = f.read()
    if not text:
        stderr.write("The specified input file does not contain data.\n")
        sys.exit(4)
    
    # Optional key obfuscation file.
    if kwargs["keyfile"]:
        with open(kwargs["keyfile"], 'r') as f:
            obfuscated_text = f.read()        
        if not obfuscated_text:
            stderr.write("The specified key obfuscation file does not contain valid data.\n")
            sys.exit(4)
    else:
        obfuscated_text = obfuscate(text)

    # Build a mapping of indices to the key file (codebook).
    text_obfuscate_map = build_text_obfuscation_map(text, obfuscated_text,
                                                    B_CASE_SENSITIVE)
    
    # Validate the mapping; if chars are missing then inform the user.
    if not text_obfuscate_map or len(text_obfuscate_map) < 1:
        stderr.write("The obfuscation mapping could not be built.\n")
        sys.exit(4)    
    if len(text_obfuscate_map) > 1:
        if text_obfuscate_map[0] == "error":
            stderr.write("Key obfuscation file text is missing characters.\n"
                         "Add missing characters or choose different text.\n\n")
            tmp = '\'' +"', '".join(text_obfuscate_map[1]) + '\''
            tmp = tmp.replace('\n', "\\n").replace('\r', "\\r").replace('\t', "\\t")
            stderr.write("Missing: %s\n" % tmp)
            sys.exit(5)
    
    # Begin displaying codebook and mappings to stdout.
    banner()
    div = "-=" * 50 + '\n' + "=-" * 50
    stdout.write("%s (Key File: Base64 Encoded)\n%s\n%s\n\n" % (HEADER_OBFUSCATION, div, b64encode(obfuscated_text)))
    stdout.write("%s (Char: Indices)\n%s\n" % (HEADER_MAPPING, div))
    
    for alist in text_obfuscate_map:
        tmp = '\'' + alist[0].replace('\n', "\\n").replace('\r', "\\r").replace('\t', "\\t") + '\''
        stdout.write("%s: %s\n" % (tmp.ljust(4), ', '.join(map(str, alist[1]))))

    n = 1
    while n <= kwargs["mappings"]:
        stdout.write("\n")
        stdout.write("%s (%d / %d)\n%s\n" % (HEADER_INDICES, n, kwargs["mappings"], div))
        
        varlist = ""
        i = 0
        len_text = len(text)
        len_obmap = len(text_obfuscate_map)
        while i < len_text:
            j = 0
            while j < len_obmap:
                if text[i] == text_obfuscate_map[j][0]:
                    ri = randint(0, len(text_obfuscate_map[j][1]) - 1)
                    random_index = text_obfuscate_map[j][1][ri]
                    j = len_obmap - 1
                j = j + 1
            varlist = varlist + INDICE_SEP + str(random_index)
            i = i + 1
        varlist = varlist.strip(INDICE_SEP)
        
        stdout.write("%s\n" % str(varlist))
        
        n = n + 1

###########################################################################

if __name__ == '__main__':
    main(sys.argv)