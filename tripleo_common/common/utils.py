# Copyright 2015 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import os


def file_checksum(filepath):
    """Calculate md5 checksum on file

    :param filepath: Full path to file (e.g. /home/stack/image.qcow2)
    :type  filepath: string

    """
    if not os.path.isfile(filepath):
        raise ValueError("The given file {0} is not a regular "
                         "file".format(filepath))
    checksum = hashlib.md5()
    with open(filepath, 'rb') as f:
        while True:
            fragment = f.read(65536)
            if not fragment:
                break
            checksum.update(fragment)
    return checksum.hexdigest()
