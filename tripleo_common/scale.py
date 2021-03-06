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

import collections
import logging
import os

from heatclient.common import template_utils

LOG = logging.getLogger(__name__)
TEMPLATE_NAME = 'overcloud-without-mergepy.yaml'


class ScaleManager(object):
    def __init__(self, heatclient, stack_id, tht_dir=None,
                 environment_files=None):
        self.heatclient = heatclient
        self.stack_id = stack_id
        self.tht_dir = tht_dir
        self.environment_files = environment_files

    def scaledown(self, instances):
        resources = self.heatclient.resources.list(self.stack_id,
                                                   nested_depth=5)
        resources_by_role = collections.defaultdict(list)
        instance_list = list(instances)
        for res in resources:
            try:
                instance_list.remove(res.physical_resource_id)
            except ValueError:
                continue

            stack_name, stack_id = next(
                x['href'] for x in res.links if
                x['rel'] == 'stack').rsplit('/', 2)[1:]
            # get resource to remove from resource group (it's parent resource
            # of nova server)
            role_resource = next(x for x in resources if
                                 x.physical_resource_id == stack_id)
            # Get the role name which is the resource_type in Heat.
            role = role_resource.resource_type
            resources_by_role[role].append(role_resource)

        resources_by_role = dict(resources_by_role)

        if instance_list:
            raise ValueError(
                "Couldn't find following instances in stack %s: %s" %
                (self.stack_id, ','.join(instance_list)))

        # decrease count for each role (or resource group) and set removal
        # policy for each resource group
        stack_params = self._get_removal_params_from_heat(resources_by_role)

        self._update_stack(parameters=stack_params)

    def _update_stack(self, parameters={}):

        tpl_files, template = template_utils.get_template_contents(
            template_file=os.path.join(self.tht_dir, TEMPLATE_NAME))
        env_paths = []
        if self.environment_files:
            env_paths.extend(self.environment_files)
        env_files, env = (
            template_utils.process_multiple_environments_and_files(
                env_paths=env_paths))
        fields = {
            'existing': True,
            'stack_id': self.stack_id,
            'template': template,
            'files': dict(list(tpl_files.items()) +
                          list(env_files.items())),
            'environment': env,
            'parameters': parameters
        }

        LOG.debug('stack update params: %s', fields)
        self.heatclient.stacks.update(**fields)

    def _get_removal_params_from_heat(self, resources_by_role):
        stack_params = {}
        stack = self.heatclient.stacks.get(self.stack_id)
        for role, role_resources in resources_by_role.items():
            param_name = "{0}Count".format(role)
            old_count = next(v for k, v in stack.parameters.items() if
                             k == param_name)
            count = max(int(old_count) - len(role_resources), 0)
            stack_params[param_name] = str(count)
            # add instance resource names into removal_policies
            # so heat knows which instances should be removed
            removal_param = "{0}RemovalPolicies".format(role)
            stack_params[removal_param] = [{
                'resource_list': [r.resource_name for r in role_resources]
            }]

        return stack_params
