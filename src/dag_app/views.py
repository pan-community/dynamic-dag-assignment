# Copyright (c) 2018, Palo Alto Networks
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Author: Nathan Embery nembery@paloaltonetworks.com

"""
Palo Alto Networks Panhandler

panhandler is a tool to find, download, and use CCF enabled repositories

Please see http://panhandler.readthedocs.io for more information

This software is provided without support, warranty, or guarantee.
Use at your own risk.
"""
import os
from pathlib import Path
from typing import Any

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from skilletlib import SkilletLoader

from pan_cnc.lib import cnc_utils
from pan_cnc.views import CNCBaseFormView
from pan_cnc.views import ProvisionSnippetView


class DAGAppFormView(CNCBaseFormView):
    required_session_vars = list()

    def get_snippet(self):
        return self.snippet

    def load_skillet_by_name(self, skillet_name) -> (dict, None):
        """
        Loads application specific skillet
        :param skillet_name:
        :return:
        """

        application_skillets_dir = Path(os.path.join(settings.SRC_PATH, self.app_dir, 'snippets'))
        skillet_loader = SkilletLoader()
        app_skillets = skillet_loader.load_all_skillets_from_dir(application_skillets_dir)
        cnc_utils.set_long_term_cached_value(self.app_dir, 'all_snippets', app_skillets, -1)
        for skillet in app_skillets:
            if skillet.name == skillet_name:
                return skillet.skillet_dict

        return None

    def get(self, request, *args, **kwargs) -> Any:
        """
        Quick check to ensure the required variables are indeed in the session and bail out if not

        :param request: request object
        :param args: supplied args
        :param kwargs: supplied kwargs
        :return: super().get Any
        """

        for v in self.required_session_vars:
            if v not in self.request.session:
                messages.add_message(self.request, messages.ERROR, f'Process Error')
                return HttpResponseRedirect(self.request.session.get('last_page', '/'))

        return super().get(request, *args, **kwargs)


class DAGProvisionView(ProvisionSnippetView):
    def get_snippet(self):
        return self.snippet

    def load_skillet_by_name(self, skillet_name) -> (dict, None):
        """
        Loads application specific skillet
        :param skillet_name:
        :return:
        """

        application_skillets_dir = Path(os.path.join(settings.SRC_PATH, self.app_dir, 'snippets'))
        skillet_loader = SkilletLoader()
        app_skillets = skillet_loader.load_all_skillets_from_dir(application_skillets_dir)
        all_skillet_dicts = list()
        for s in app_skillets:
            all_skillet_dicts.append(s.skillet_dict)

        cnc_utils.set_long_term_cached_value(self.app_dir, 'all_snippets', all_skillet_dicts, -1)

        for skillet in app_skillets:
            if skillet.name == skillet_name:
                return skillet.skillet_dict

        return None
