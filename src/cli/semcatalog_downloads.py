"""
semcatalog.urls

    Copyright (c) 2015, The Regents of the University of California,
    through Lawrence Berkeley National Laboratory (subject to receipt
    of any required approvals from the U.S. Dept. of Energy).
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:
    (1) Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer. (2) Redistributions
    in binary form must reproduce the above copyright notice, this list of
    conditions and the following disclaimer in the documentation and/or other
    materials provided with the distribution. (3) Neither the name of the
    University of California, Lawrence Berkeley National Laboratory, U.S.
    Dept. of Energy nor the names of its contributors may be used to endorse or
    promote products derived from this software without specific prior written
    permission.
    
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
    ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
    LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
    SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
    INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
    CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.
    
    You are under no obligation whatsoever to provide any bug fixes, patches,
    or upgrades to the features, functionality or performance of the source
    code ("Enhancements") to anyone; however, if you choose to make your
    Enhancements available either publicly, or directly to Lawrence Berkeley
    National Laboratory, without imposing a separate written license agreement
    for such Enhancements, then you hereby grant the following license:
    a non-exclusive, royalty-free perpetual license to install, use, modify,
    prepare derivative works, incorporate into other computer software,
    distribute, and sublicense such enhancements or derivative works thereof,
    in binary and source code form.

URLs for the SEMC Software Catalog

@author: Gilberto Pastorello
@contact: gzpastorello@lbl.gov
@date: 2015-03-30
"""
import sys
import argparse
import requests # TODO: test import
import json

# TODO: get_list of software
# TODO: get_list of API commands
# TODO: delete download_count entry
# TODO: add version to sw
# TODO: download counts only ----------
# TODO: API for updates to other fields
#       -- google analytics as download count method
#       -- statcounter.com (more site access, counter) (Hari)
# TODO: You-Wei can help with testing
# TODO: add continuous integration / testing (travis/github, bamboo/bitbucket) -- Shreyas will help
# TODO: reports (to tech transfer) what info: (check with Tech Transfer on formats Dan, Hari) -- look into forms



BASE_URL = 'http://localhost:8000/catalog/{s}/{c}/'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', metavar="COMMAND", help="Main command to be executed", choices=['get_count', 'add_count', 'set_password'], type=str, nargs=1)
    parser.add_argument('softwareid', metavar="SOFTWAREID", help="Software ID", type=str, nargs=1)
    args = parser.parse_args()

    request_url =  BASE_URL.format(s=args.softwareid[0], c=args.command[0])

    if args.command[0] == 'get_count':
        r = requests.get(request_url)
        info = json.loads(r.text)
        print(info['download count'])
    elif args.command[0] == 'add_count':
        print('NOT IMPLEMENTED')
    elif args.command[0] == 'set_password':
        print('NOT IMPLEMENTED')
    else:
        sys.exit("ERROR: unknown command '{c}'".format(c=args.command[0]))

    sys.exit(0)
