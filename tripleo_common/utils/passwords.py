#   Copyright 2016 Red Hat, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import logging
import os
import os.path
import passlib.utils as passutils

from tripleo_common import constants
from tripleo_common import exception

_MIN_PASSWORD_SIZE = 25


def generate_overcloud_passwords(output_file="tripleo-overcloud-passwords",
                                 create_password_file=False):
    """Create the passwords needed for the overcloud

    This will create the set of passwords required by the overcloud, store
    them in the output file path and return a dictionary of passwords. If the
    file already exists the existing passwords will be returned instead,
    """

    log = logging.getLogger(__name__ + ".generate_overcloud_passwords")

    log.debug("Using password file: {0}".format(os.path.abspath(output_file)))

    passwords = {}
    if os.path.isfile(output_file):
        with open(output_file) as f:
            passwords = dict(line.split('=') for line in f.read().splitlines())
    elif not create_password_file:
        raise exception.PasswordFileNotFound(
            "The password file could not be found!")

    for name in constants.PASSWORD_NAMES:
        if not passwords.get(name):
            passwords[name] = passutils.generate_password(
                size=_MIN_PASSWORD_SIZE)

    with open(output_file, 'w') as f:
        for name, password in passwords.items():
            f.write("{0}={1}\n".format(name, password))

    return passwords
