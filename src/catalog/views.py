"""
catalog.views

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

Views for the SEMC Software Catalog

@author: Gilberto Pastorello
@contact: gzpastorello@lbl.gov
@date: 2015-03-28
"""
import csv
import json

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, Http404
from django.utils import timezone

from catalog.models import Software

def list_commands(request):
    """
    Returns list of commands available
    """
    hostname = request.get_host()

    command_list = {'command_list': [
        {'command': 'list_commands', 'url': hostname + '/' + "list_commands", },
        {'command': 'list_software', 'url': hostname + '/' + "list_software", },
        {'command': 'software_details', 'url': hostname + '/' + "catalog/SOFTWAREID/software_details", },
        {'command': 'get_count', 'url': hostname + '/' + "catalog/SOFTWAREID/get_count", },
        {'command': 'add_count', 'url': hostname + '/' + "catalog/SOFTWAREID/add_count", },
        {'command': 'del_count', 'url': hostname + '/' + "catalog/SOFTWAREID/del_count", },
        {'command': 'set_password', 'url': hostname + '/' + "catalog/SOFTWAREID/set_password", },
    ]}
    return JsonResponse(command_list)

def list_software(request):
    """
    Returns list of software available in catalog
    """
    hostname = request.get_host()

    software = Software.objects.all()

    software_list = {'software_list': [{'software id': s.slug,
                                        'software name': s.name,
                                        'description': s.description,
                                        'web URL': hostname + '/catalog/' + s.slug,
                                        'source URL': s.url_src,
                                        'issue tracking URL': s.url_issue,
                                        'LBNL department': s.department,
                                        'contacts': [c.name + ' <' + c.email + '>' for c in s.contacts.all()],
                                        "download counts":[{'count':e.count, 'timestamp':e.valid_on.strftime("%Y%m%dT%H%M%S")} for e in s.downloadcount_set.all()],
                                        } for s in software]}
    return JsonResponse(software_list)

def index(request):
    """
    Main page with list of softwares in catalog
    """
    software_list = Software.objects.all()
    return render(request, 'index.html', {'software_list': software_list})


def software_details(request, slug, rformat='html'):
    """
    Details page for a given software package
    
    :param slug: slug from software name
    :type slug: str
    """
    software = get_object_or_404(Software, slug=slug)
    if rformat.lower() == 'html':
        return render(request, 'details.html', {'software': software})
    elif rformat.lower() == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="software_catalog_{n}.csv"'.format(n=software.slug)

        writer = csv.writer(response)
        writer.writerow(["Software Name", "Software ID", "LBNL Department", "Web URL", "Source URL", "Issue Tracking URL", "Contacts", "Download Count", "Download Count Timestamp"])
        for dlcount in software.downloadcount_set.all():
            writer.writerow([software.name, software.slug, software.department, software.url, software.url_src, software.url_issue, software.contact_list, dlcount.count, dlcount.valid_on.strftime("%Y%m%dT%H%M%S")])

        return response
    elif rformat.lower() == 'json':
        software_data = {software.slug: {
            "software name": software.name,
            "software id": software.slug,
            "description": software.description,
            "LBNL department": software.department,
            "web URL": software.url,
            "source URL": software.url_src,
            "issue tracking URL": software.url_issue,
            "contacts": [{'Name':c.name, 'Email':c.email} for c in software.contacts.all()],
            "download counts":[{'count':e.count, 'timestamp':e.valid_on.strftime("%Y%m%dT%H%M%S")} for e in software.downloadcount_set.all()],
        }, }
        return JsonResponse(software_data)
    else:
        raise Http404


def software_get_download_count(request, slug, timestamp=None):
    """
    Returns most recent download count for software and timestamp when valid
    
    :param slug: slug from software name
    :type slug: str
    """
    print(timestamp)
    if request.method == 'GET':
        software = get_object_or_404(Software, slug=slug)
        if timestamp is None:
            download_count = software.downloads_recent()
        else:
            download_count = software.downloads_timestamp(timestamp)

        if download_count:
            count = download_count.count
            timestamp = download_count.valid_on.strftime("%Y%m%dT%H%M%S")
        else:
            count = 'no downloads'
            timestamp = ''
        response_str = '{"software name": "%s",\n"software id": "%s",\n"download count": %d,\n"download count timestamp": "%s"}\n' % (software.name, software.slug, count, timestamp)
        return HttpResponse(response_str, content_type="application/json")
    elif request.method == 'POST':
        HttpResponse('{}', content_type="application/json")



def software_add_download_count(request, slug, password, timestamp=timezone.now().strftime("%Y%m%dT%H%M%S")):
    """
    Adds download count for software with timestamp when valid (default now)
    
    :param slug: slug from software name
    :type slug: str
    :param password: default secret password for updates to software
    :type password: str
    :param timestamp: timestamp of download counts
    :type timestamp: str
    """
    return

def software_del_download_count(request, slug, password, timestamp=None):
    """
    Removes download count for software with timestamp when valid (default most recent)
    
    :param slug: slug from software name
    :type slug: str
    :param password: default secret password for updates to software
    :type password: str
    :param timestamp: timestamp of download counts to be removed
    :type timestamp: str
    """
    return


def software_set_password(request, slug, old_password, new_password):
    """
    Updates default password for changes to software with new password 
    
    :param slug: slug from software name
    :type slug: str
    :param old_password: current secret password for updates to software
    :type old_password: str
    :param new_password: new secret password for updates to software
    :type new_password: str
    """
    return

