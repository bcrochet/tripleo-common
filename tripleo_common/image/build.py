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


import logging
import os
import re

from tripleo_common.image.base import BaseImageManager
from tripleo_common.image.image_builder import ImageBuilder


# YAML FILE FORMAT
# disk_images:
#   -
#      imagename: overcloud-compute
#      builder: dib
#      arch: amd64
#      type: qcow2
#      elements:
#        - overcloud-compute
#      packages:
#        - vim
#      options:
class ImageBuildManager(BaseImageManager):
    logger = logging.getLogger(__name__ + '.ImageBuildManager')

    def __init__(self, config_files, node_dist=None, output_directory='.',
                 skip=False, verbose=False, debug=False):
        super(ImageBuildManager, self).__init__(config_files, verbose, debug)
        self.node_dist = node_dist
        self.output_directory = re.sub('[/]$', '', output_directory)
        self.skip = skip

    def build(self):
        self.logger.info('Using config files: %s' % self.config_files)

        disk_images = self.load_config_files()

        for image in disk_images:
            arch = image.get('arch', 'amd64')
            img_type = image.get('type', 'qcow2')
            imagename = image.get('imagename')
            builder = image.get('builder', 'dib')
            self.logger.info('imagename: %s' % imagename)
            image_path = '%s/%s.%s' % (
                self.output_directory, imagename, img_type)
            if self.skip:
                self.logger.info('looking for image at path: %s' % image_path)
                if os.path.exists(image_path):
                    self.logger.warn('Image file exists for image name: %s' %
                                     imagename)
                    self.logger.warn('Skipping image build')
                    continue
            elements = image.get('elements', [])
            options = image.get('options', [])
            packages = image.get('packages', [])

            builder = ImageBuilder.get_builder(builder)
            builder.build_image(image_path, self.node_dist, arch, elements,
                                options, packages)
