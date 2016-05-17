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

from uuid import uuid4

import mock
import os.path
import tempfile
from unittest import TestCase

from tripleo_common import constants
from tripleo_common import exception
from tripleo_common.utils import passwords as utils


class TestPasswordsUtil(TestCase):

    @mock.patch("os.path.isfile", return_value=False)
    @mock.patch("passlib.utils.generate_password",
                return_value="PASSWORD")
    def test_generate_passwords(self, generate_password_mock, isfile_mock):

        mock_open = mock.mock_open()

        with mock.patch('six.moves.builtins.open', mock_open):
            passwords = utils.generate_overcloud_passwords(
                create_password_file=True)
        mock_calls = [
            mock.call('NEUTRON_METADATA_PROXY_SHARED_SECRET=PASSWORD\n'),
            mock.call('OVERCLOUD_ADMIN_PASSWORD=PASSWORD\n'),
            mock.call('OVERCLOUD_ADMIN_TOKEN=PASSWORD\n'),
            mock.call('OVERCLOUD_AODH_PASSWORD=PASSWORD\n'),
            mock.call('OVERCLOUD_CEILOMETER_PASSWORD=PASSWORD\n'),
            mock.call('OVERCLOUD_CEILOMETER_SECRET=PASSWORD\n'),
            mock.call('OVERCLOUD_CINDER_PASSWORD=PASSWORD\n'),
            mock.call('OVERCLOUD_DEMO_PASSWORD=PASSWORD\n'),
            mock.call('OVERCLOUD_GLANCE_PASSWORD=PASSWORD\n'),
            mock.call('OVERCLOUD_GNOCCHI_PASSWORD=PASSWORD\n'),
            mock.call('OVERCLOUD_HAPROXY_STATS_PASSWORD=PASSWORD\n'),
            mock.call('OVERCLOUD_HEAT_PASSWORD=PASSWORD\n'),
            mock.call('OVERCLOUD_HEAT_STACK_DOMAIN_PASSWORD=PASSWORD\n'),
            mock.call('OVERCLOUD_NEUTRON_PASSWORD=PASSWORD\n'),
            mock.call('OVERCLOUD_NOVA_PASSWORD=PASSWORD\n'),
            mock.call('OVERCLOUD_RABBITMQ_PASSWORD=PASSWORD\n'),
            mock.call('OVERCLOUD_REDIS_PASSWORD=PASSWORD\n'),
            mock.call('OVERCLOUD_SAHARA_PASSWORD=PASSWORD\n'),
            mock.call('OVERCLOUD_SWIFT_HASH=PASSWORD\n'),
            mock.call('OVERCLOUD_SWIFT_PASSWORD=PASSWORD\n'),
            mock.call('OVERCLOUD_TROVE_PASSWORD=PASSWORD\n'),
        ]
        self.assertEqual(sorted(mock_open().write.mock_calls), mock_calls)
        self.assertEqual(generate_password_mock.call_count, len(mock_calls))

        self.assertEqual(len(passwords), len(mock_calls))

    def test_generate_passwords_update(self):

        mock_open = mock.mock_open()

        with mock.patch('six.moves.builtins.open', mock_open):
            with self.assertRaises(exception.PasswordFileNotFound):
                utils.generate_overcloud_passwords()

    @mock.patch("os.path.isfile", return_value=True)
    @mock.patch("passlib.utils.generate_password",
                return_value="PASSWORD")
    def test_load_passwords(self, generate_password_mock, isfile_mock):
        PASSWORDS = [
            'OVERCLOUD_ADMIN_PASSWORD=PASSWORD\n',
            'OVERCLOUD_ADMIN_TOKEN=PASSWORD\n',
            'OVERCLOUD_AODH_PASSWORD=PASSWORD\n',
            'OVERCLOUD_CEILOMETER_PASSWORD=PASSWORD\n',
            'OVERCLOUD_CEILOMETER_SECRET=PASSWORD\n',
            'OVERCLOUD_CINDER_PASSWORD=PASSWORD\n',
            'OVERCLOUD_DEMO_PASSWORD=PASSWORD\n',
            'OVERCLOUD_GLANCE_PASSWORD=PASSWORD\n',
            'OVERCLOUD_GNOCCHI_PASSWORD=PASSWORD\n',
            'OVERCLOUD_HAPROXY_STATS_PASSWORD=PASSWORD\n',
            'OVERCLOUD_HEAT_PASSWORD=PASSWORD\n',
            'OVERCLOUD_HEAT_STACK_DOMAIN_PASSWORD=PASSWORD\n',
            'OVERCLOUD_NEUTRON_PASSWORD=PASSWORD\n',
            'OVERCLOUD_NOVA_PASSWORD=PASSWORD\n',
            'OVERCLOUD_RABBITMQ_PASSWORD=PASSWORD\n',
            'OVERCLOUD_REDIS_PASSWORD=PASSWORD\n',
            'OVERCLOUD_SAHARA_PASSWORD=PASSWORD\n',
            'OVERCLOUD_SWIFT_HASH=PASSWORD\n',
            'OVERCLOUD_SWIFT_PASSWORD=PASSWORD\n',
            'OVERCLOUD_TROVE_PASSWORD=PASSWORD\n',
            'NEUTRON_METADATA_PROXY_SHARED_SECRET=PASSWORD\n',
        ]

        mock_open = mock.mock_open(read_data=''.join(PASSWORDS))
        mock_open.return_value.__iter__ = lambda self: self
        mock_open.return_value.__next__ = lambda self: self.readline()

        with mock.patch('six.moves.builtins.open', mock_open):
            passwords = utils.generate_overcloud_passwords()

        generate_password_mock.assert_not_called()
        self.assertEqual(len(passwords), len(PASSWORDS))
        for name in constants.PASSWORD_NAMES:
            self.assertEqual('PASSWORD', passwords[name])
