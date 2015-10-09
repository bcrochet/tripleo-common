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

from tripleo_common import utils
from tripleo_common.image.base import BaseImageManager
from tripleo_common.image.image_builder import ImageBuilder


# YAML FILE FORMAT
# disk_images:
#   -
#      imagename: overcloud-compute
#      builder: dib
#      arch: amd64
#      type: qcow2
#      destination: /some/path (or glance)
#      elements:
#        - overcloud-compute
#      packages:
#        - vim
#      options:
class ImageLoadManager(BaseImageManager):
    logger = logging.getLogger(__name__ + '.ImageBuildManager')

    def __init__(self, config_files, input_directory='.',
                 heat_env_output_file=None, remove_duplicates=False,
                 imageclient=None, verbose=False, debug=False):
        super(ImageBuildManager, self).__init__(config_files, node_dist,
                                                verbose, debug)
        self.input_directory = re.sub('[/]$', '', input_directory)
        self.heat_env_output_file = heat_env_output_file
        self.remove_duplicates = remove_duplicates
        self.imageclient = imageclient

    def _read_image_file_pointer(self, image_path):
        return open(image_path, 'rb')

    def _upload_image(self, *args, **kwargs):
        image = self.app.client_manager.image.images.create(*args, **kwargs)
        self.logger.info('Image "%s" was uploaded.' % image.name)
        return image

    def _remove_image(self, name):
        kwargs = {'name': name}
        images = self.imageclient.images.findall(**kwargs)
        for image in images:
            self.logger.debug("Removing image %s (%s) from image service" %
                              (image.name, image.id))
            self.imageclient.images.delete(image.id)

    def _load_image(self, image_name, image_path,
                    image_format, remove_duplicates):
        image_directory = os.path.dirname(image_path)
        ramdisk = "%s/%s.initrd" % (image_directory, image_name)
        kernel = "%s/%s.vmlinuz" % (image_directory, image_name)

        kwargs = {'name': image_name}
        try:
            current_image = self.imageclient.images.find(**kwargs)
            new_checksum = utils.file_checksum(image_path)
            if new_checksum == current_image.checksum:
                self.logger.info("%s checksum matches image service checksum, "
                                 "not creating duplicate image." % image_path)
                return
        except:
            pass

        if remove_duplicates:
            self._remove_image("%s-vmlinuz" % image_name)
            self._remove_image("%s-initrd" % image_name)
            self._remove_image("%s" % image_name)


        kernel = self._upload_image(
            name="%s-vmlinuz" % image_name,
            is_public=True,
            disk_format='aki',
            container_format='aki',
            data=self._read_image_file_pointer(kernel)
        )
        ramdisk = self._upload_image(
            name="%s-initrd" % image_name,
            is_public=True,
            disk_format="ari",
            container_format="ari",
            data=self._read_image_file_pointer(ramdisk)
        )
        self._upload_image(
            name=image_name,
            is_public=True,
            disk_format=image_format,
            container_format="bare",
            properties={'kernel_id': kernel.id,
                        'ramdisk_id': ramdisk.id},
            data=self._read_image_file_pointer(image_path)
        )

    def load(self):
        self.logger.info('Using config files: %s' % self.config_files)

        disk_images = self.load_config_files()

        heat_parameters = {'parameters': {}}

        for image in disk_images:
            img_type = image.get('type', 'qcow2')
            image_name = image.get('imagename')
            image_path = '%s/%s.%s' % (
                self.input_directory, image_name, img_type)
            if os.path.isfile(image_path):
                logger.info('image path: %s' % image_path)
                try:
                    self._load(image_name, image_path,
                               img_type, self.remove_duplicates)
                except:
                    pass
                if image.get('heat_parameters'):
                    for name in image.get('heat_parameters'):
                        heat_parameters['parameters'][name] = stdout.strip()

            else:
                logger.warn('No image file exists for image name: %s' %
                            image_path)
                continue

        if self.heat_env_output_file:
            with open(self.heat_env_output_file, 'w') as of:
                of.write(yaml.dump(heat_parameters))