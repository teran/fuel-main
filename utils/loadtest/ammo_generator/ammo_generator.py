#    Copyright 2014 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json
from optparse import OptionParser
import os
from random import randint
import sys

from django.conf import settings
from django.template import Template, Context

settings.configure(TEMPLATE_DEBUG=True)


class ammo_generator():
    def generate_random_mac(self):
        mac = [randint(0x00, 0x7f) for _ in xrange(6)]

        return ':'.join(map(lambda x: "%02x" % x, mac)).lower()

    def generate_random_ip(self):
        octet = lambda: str(randint(0, 255))

        return ".".join(["10", octet(), octet(), octet()])


def generate_ammo(handler, icount=3):
    interfaces = []
    for i in range(1, icount):
        it = {
            "current_speed": None,
            "max_speed": 1000,
            "mac": ammo_generator().generate_random_mac(),
            "state": "down",
            "name": "eth%s" % i
        }
        interfaces.append(json.dumps(it))

    t = Template(
        open(
            '%s/templates/%s.json' % (os.path.dirname(__file__), handler), 'r'
        ).read())
    print t.render(
        Context({
            'interfaces': interfaces,
            'test_var': 'LOL it works'
        })
    )

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-a', '--handler', dest='handler', type='string',
                      help='Handler to generate ammos for')
    parser.add_option('-c', '--count', dest='count', type='int',
                      help='Amount of ammos to generate')

    (options, args) = parser.parse_args()


    generate_ammo(options.handler)
