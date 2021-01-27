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
Palo Alto Networks DAG APp

Quick CNC App to load the DAG skillets as a standalone application

This software is provided without support, warranty, or guarantee.
Use at your own risk.
"""
import os
from pathlib import Path

from django.conf import settings
from skilletlib import SkilletLoader

from pan_cnc.lib import cnc_utils
from pan_cnc.views import ProvisionSnippetView


class DAGProvisionView(ProvisionSnippetView):
    def get_snippet(self):
        return self.snippet

    def load_skillet_by_name(self, skillet_name) -> (dict, None):
        """
        Loads application specific skillet

        :param skillet_name:
        :return:
        """

        all_skillets = cnc_utils.get_long_term_cached_value(self.app_dir, 'all_snippets')
        if not all_skillets:
            all_skillets = list()
            application_skillets_dir = Path(os.path.join(settings.SRC_PATH, self.app_dir, 'snippets'))
            skillet_loader = SkilletLoader()
            app_skillets = skillet_loader.load_all_skillets_from_dir(application_skillets_dir)
            for s in app_skillets:
                all_skillets.append(s.skillet_dict)

            cnc_utils.set_long_term_cached_value(self.app_dir, 'all_snippets', all_skillets, -1)

        for skillet in all_skillets:
            if skillet['name'] == skillet_name:
                return skillet

        return None

    def get_context_data(self, **kwargs):

        user_ip = self.request.META.get('REMOTE_ADDR')
        self.save_value_to_workflow('dag_ip_address', user_ip)

        return super().get_context_data(**kwargs)
