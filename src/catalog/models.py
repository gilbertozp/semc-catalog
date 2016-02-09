"""
catalog

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

Models for SEMC Software Catalog

@author: Gilberto Pastorello
@contact: gzpastorello@lbl.gov
@date: 2015-03-28
"""
import os
import sys

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from datetime import datetime


class Contact(models.Model):
    """
    Contact information for a software package
    """
    name = models.CharField(max_length=255, null=True, blank=True, help_text="contact's full name")
    email = models.EmailField(null=True, blank=True, help_text="contact's email address")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return u"{t}".format(t=(self.name if self.name else "(no name)"))


class Software(models.Model):
    """
    Software package record
    """
    name = models.CharField(max_length=255, null=True, blank=True, help_text='software name')
    slug = models.CharField(max_length=255, editable=False, null=True, blank=True, help_text='software name')
    description = models.TextField(null=True, blank=True, help_text='software description')
    url = models.URLField(null=True, blank=True, help_text='software main URL')
    url_src = models.URLField(null=True, blank=True, help_text='software source code URL')
    url_issue = models.URLField(null=True, blank=True, help_text='software issue tracking URL')
    department = models.TextField(null=True, blank=True, help_text='LBNL Department')
    password = models.TextField(null=True, blank=True, help_text='Software password for to allow changes')
    contacts = models.ManyToManyField(Contact, null=True)

    # general access info
    created_on = models.DateTimeField(editable=False, help_text='timestamp of creation')
    updated_on = models.DateTimeField(editable=False, help_text='timestamp of most recent update')

    def save(self, *args, **kwargs):
        """
        Update timestamps on save
        """
        self.slug = slugify(self.name)
        if not self.id:
            self.created_on = timezone.now()
        self.updated_on = timezone.now()
        return super(Software, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return u"{t}".format(t=(self.name if self.name else "(no name)"))

    def all_contacts(self):
        """
        Returns comma-separated list of contacts and email addresses
        """
        return ', '.join(["{n} <{e}>".format(n=i.name, e=i.email) for i in self.contacts.all()])

    def downloads_recent(self):
        """
        Returns most recent download count and timestamp
        """
        download_counts = self.downloadcount_set.order_by('-valid_on')
        if download_counts:
            return download_counts[0]
        else:
            return None

    def downloads_timestamp(self, timestamp):
        """
        Returns most recent download count and timestamp
        """
        ts = datetime.strptime(timestamp, '%Y%m%dT%H%M%S')
        download_counts = self.downloadcount_set.get('valid_on={t}'.format(t=ts))
        if download_counts:
            return download_counts[0]
        else:
            return None

    @property
    def contact_list(self):
        """
        Returns string with comma separated contact list name <email>,
        """
        result = ''
        for c in self.contacts.all():
            result += "{n} <{e}>, ".format(n=c.name, e=c.email)
        if result:
            result = result[:-2]
        return result


class DownloadCount(models.Model):
    """
    Download count records for software packages
    """
    software = models.ForeignKey(Software)
    valid_on = models.DateTimeField(default=timezone.now(), help_text='timestamp of when count is valid')
    count = models.IntegerField(help_text='number of downloads at this time')

    # general access info
    created_on = models.DateTimeField(editable=False, help_text='timestamp of creation')
    updated_on = models.DateTimeField(editable=False, help_text='timestamp of most recent update')

    def save(self, *args, **kwargs):
        """
        Update timestamps on save
        """
        if not self.id:
            self.created_on = timezone.now()
        self.updated_on = timezone.now()
        return super(DownloadCount, self).save(*args, **kwargs)

    class Meta:
        ordering = ['software', '-valid_on']

    def __str__(self):
        return u"{n}_{t}".format(n=self.software.name, t=self.valid_on.strftime("%Y%m%d"))

