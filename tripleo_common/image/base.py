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
import yaml


class BaseImageManager(object):
    logger = logging.getLogger(__name__ + '.BaseImageManager')

    def __init__(self, config_files, verbose=False, debug=False):
        self.config_files = config_files
        self._configure_logger(verbose, debug)

    def _configure_logger(self, verbose=False, debug=False):
        LOG_FORMAT = '[%(asctime)s] [%(levelname)s] %(message)s'
        DATE_FORMAT = '%Y/%m/%d %I:%M:%S %p'
        log_level = logging.WARN

        if debug:
            log_level = logging.DEBUG
        elif verbose:
            log_level = logging.INFO

        logging.basicConfig(format=LOG_FORMAT, datefmt=DATE_FORMAT,
                            level=log_level)

    def load_config_files(self):
        for config_file in self.config_files:
            if os.path.isfile(config_file):
                with open(config_file) as cf:
                    disk_images = yaml.load(cf.read()).get("disk_images")
                    self.logger.debug(
                        'disk_images JSON: %s' % str(disk_images))
            else:
                self.logger.error('No config file exists at: %s' % config_file)
                raise IOError('No config file exists at: %s' % config_file)

        return disk_images
