# Copyright 2015 Red Hat, Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


#: The name of the root template in a standard tripleo-heat-template layout.
TEMPLATE_NAME = 'overcloud-without-mergepy.yaml'

#: The name of the type for resource groups.
RESOURCE_GROUP_TYPE = 'OS::Heat::ResourceGroup'

#: The resource name used for package updates
UPDATE_RESOURCE_NAME = 'UpdateDeployment'

#: The default timeout to pass to Heat stacks
STACK_TIMEOUT_DEFAULT = 240

#: The default name to use for a plan container
DEFAULT_CONTAINER_NAME = 'overcloud'

#: The path to the tripleo heat templates installed on the undercloud
DEFAULT_TEMPLATES_PATH = '/usr/share/openstack-tripleo-heat-templates/'

#: The list of passwords used in the tripleo heat templates.
PASSWORD_NAMES = (
    "OVERCLOUD_ADMIN_PASSWORD",
    "OVERCLOUD_ADMIN_TOKEN",
    "OVERCLOUD_AODH_PASSWORD",
    "OVERCLOUD_CEILOMETER_PASSWORD",
    "OVERCLOUD_CEILOMETER_SECRET",
    "OVERCLOUD_CINDER_PASSWORD",
    "OVERCLOUD_DEMO_PASSWORD",
    "OVERCLOUD_GLANCE_PASSWORD",
    "OVERCLOUD_GNOCCHI_PASSWORD",
    "OVERCLOUD_HAPROXY_STATS_PASSWORD",
    "OVERCLOUD_HEAT_PASSWORD",
    "OVERCLOUD_HEAT_STACK_DOMAIN_PASSWORD",
    "OVERCLOUD_NEUTRON_PASSWORD",
    "OVERCLOUD_NOVA_PASSWORD",
    "OVERCLOUD_RABBITMQ_PASSWORD",
    "OVERCLOUD_REDIS_PASSWORD",
    "OVERCLOUD_SAHARA_PASSWORD",
    "OVERCLOUD_SWIFT_HASH",
    "OVERCLOUD_SWIFT_PASSWORD",
    "OVERCLOUD_TROVE_PASSWORD",
    "NEUTRON_METADATA_PROXY_SHARED_SECRET"
)
