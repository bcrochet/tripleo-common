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

import mock

from tripleo_common.image.build import ImageBuildManager
from tripleo_common.image.image_builder import ImageBuilder
from tripleo_common.tests import base
from tripleo_common.tests.image import fakes


class TestImageBuildManager(base.TestCase):
    def setUp(self):
        super(TestImageBuildManager, self).setUp()

    @mock.patch.object(ImageBuilder, 'get_builder')
    @mock.patch('tripleo_common.image.base.BaseImageManager.load_config_files',
                autospec=True)
    def test_build(self, mock_load_config_files, mock_get_builder):
        mock_load_config_files.return_value = fakes.create_disk_images().get(
            'disk_images')

        mock_builder = mock.Mock()
        mock_get_builder.return_value = mock_builder

        build_manager = ImageBuildManager(['config/file'])
        build_manager.build()

        assert mock_load_config_files.called
        assert mock_load_config_files.call_count == 1

        mock_builder.build_image.assert_called_with(
            './overcloud.qcow2', None, 'amd64', ['image_element'], [], [])
