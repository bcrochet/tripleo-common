#   Copyright 2015 Red Hat, Inc.
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


import abc
import logging
import six
import subprocess

from tripleo_common.common.exceptions import ImageBuilderException


@six.add_metaclass(abc.ABCMeta)
class ImageBuilder(object):
    """Base representation of an image building method"""

    @staticmethod
    def get_builder(builder):
        if builder == 'dib':
            return DibImageBuilder()
        raise ImageBuilderException('Unknown image builder type')

    @abc.abstractmethod
    def build_image(self, parsed_args, node_type):
        """Build a disk image"""
        pass


class DibImageBuilder(ImageBuilder):
    """Build images using diskimage-builder"""

    logger = logging.getLogger(__name__ + '.DibImageBuilder')

    def build_image(self, image_path, node_dist, arch, elements,
                    options, packages):
        cmd = ['disk-image-create', '-a', arch, '-o', image_path]

        if packages:
            cmd.append('-p')
            cmd.append(','.join(packages))

        if options:
            cmd.extend(options)

        if node_dist:
            cmd.append(node_dist)

        cmd.extend(elements)

        self.logger.info('Running %s' % cmd)
        subprocess.check_call(cmd)
