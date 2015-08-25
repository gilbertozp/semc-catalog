"""
catalog.populate

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

Populate entries for SEMC Software Catalog from given source

@author: Gilberto Pastorello
@contact: gzpastorello@lbl.gov
@date: 2015-03-28
"""
import os
import sys
import csv
import io
import re

from django.utils import timezone

from catalog.models import Contact, Software, DownloadCount
from semcatalog.settings import BASE_DIR


PASSWORD = 'CRD-SEMC_VerySecretPassword1234'

def populate_from_csv(source_filename=os.path.join( os.path.join(BASE_DIR, os.pardir), 'data', 'catalog_v0.1_gspreadsheets_export_2015-03-30.csv')):
    """
    Populates DB from csv (export from google spreadsheets catalog)

    :param source_filename: source CSV filename 
    :type source_filename: str
    """

    print("Processing:", source_filename)
    lines = []
    with io.open(source_filename, 'r', encoding="utf8") as f:
        for line in csv.reader(f):
            lines.append([i.encode('utf8').decode("utf8") for i in line])

    for line in lines[1:]:
        if ((not line[0]) or (line[0].strip().lower() == 'no url')):
            continue
        name, description, url, contact, department, email1, email2 = line
        if url and (not url.startswith('http')):
            url = 'http://' + url
        contacts = [c.strip() for c in re.split(',|/|;', contact)]
        emails = [email1, email2]
        contacts += [''] * max(len(contacts), len(emails))
        emails += [''] * max(len(contacts), len(emails))
        contact_infos = [ (a, b) for (a, b) in list(zip(contacts, emails)) if (a or b) ]
        contact_list = []
        for cname, cemail in contact_infos:
            try:
                c = Contact.objects.get(name=cname)
                if cemail and not c.email:
                    c.email = cemail
                    c.save()
            except Contact.DoesNotExist:
                c = Contact(name=cname, email=cemail)
                c.save()
            contact_list.append(c)
        url_src = (url if ('bitbucket.org' in url or 'github.com' in url) else None)
        s = Software(name=name, description=description, department=department, url=url, url_src=url_src, password=PASSWORD)
        s.save()
        for c in contact_list:
            s.contacts.add(c)
        s.save()
        d = DownloadCount(software=s, valid_on=timezone.now(), count=10)
        d.save()

if __name__ == '__main__':
    populate_from_csv()
