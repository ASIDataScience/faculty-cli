"""Interact with the Faculty knowledge centre."""

# Copyright 2016-2019 Faculty Science Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from faculty.clients.template import (
    TemplateRetrievalError,
    ResourceValidationError,
    DefaultParametersParsingError,
    ParameterValidationError,
    GenericParsingError,
)

EMPTY_PARAMETERS_YAML = """
# This file describes the parameters used in the interpolation of your
# template. Each parameter has a name, description and type that help users of
# your template choose sensible values.

# parameters:
#   parameter_name:
#     type: <str|bool|filename|number|subdomain>
#     description: <Some text to help the user choose a suitable value>
#     default: <Some sensible default value>
"""


def create_blank_template():
    resource_path = os.path.join(os.getcwd(), "faculty-resources")
    workspace_path = os.path.join(os.getcwd(), "workspace")
    os.mkdir(resource_path)
    os.mkdir(workspace_path)

    def _write_yaml(yaml_content, path):
        with open(os.path.join(os.getcwd(), path), "w") as parameters:
            parameters.write(yaml_content)

    _write_yaml(EMPTY_PARAMETERS_YAML, "parameters.yaml")


def publishing_error_message(error):
    formatters = {
        DefaultParametersParsingError: _simple_error_formatter,
        ResourceValidationError: _resource_validation_error,
        ParameterValidationError: _parameter_validation_error,
        TemplateRetrievalError: _retrieval_error,
        GenericParsingError: _simple_error_formatter,
    }
    formatter = formatters.get(type(error), _default_error_message)
    return formatter(error)


def _default_error_message(*args):
    return "Unknown template error"


def _map_prefix(prefix, errors):
    return [prefix + e for e in errors]


def _one_per_line(error_message_lists):
    messages = [msg for sublist in error_message_lists for msg in sublist]
    return "\n".join(messages)


def _simple_error_formatter(error):
    return error.error


def _parameter_validation_error(errors):
    messages = _map_prefix("Parameter validation failed: ", errors.errors)
    return "\n".join(messages)


def _retrieval_error(error):
    message_lists = [
        _map_prefix(prefix, errors)
        for prefix, errors in [
            ("Error reading app resource definition: ", error.apps),
            ("Error reading API resource definition: ", error.apis),
            (
                "Error reading environment resource definition: ",
                error.environments,
            ),
            ("Error reading app job definition: ", error.jobs),
        ]
    ]
    return _one_per_line(message_lists)


def _resource_validation_error(error):
    apps = error.apps
    apis = error.apis
    envs = error.environments
    jobs = error.jobs
    workspace = error.workspace
    message_lists = [
        _map_prefix(prefix, errors)
        for prefix, errors in [
            ("App subdomain already exists: ", apps.subdomain_conflicts),
            ("App name already exists: ", apps.name_conflicts),
            ("Invalid app working directory: ", apps.invalid_working_dirs),
            ("API subdomain already exists: ", apis.subdomain_conflicts),
            ("API name already exists: ", apis.name_conflicts),
            ("Invalid API working directory: ", apis.invalid_working_dirs),
            ("Environment name already exists: ", envs.name_conflicts),
            ("Invalid environment name: ", envs.invalid_names),
            ("Job name already exists: ", jobs.name_conflicts),
            ("Invalid job name: ", jobs.invalid_names),
            ("Invalid job working directory: ", jobs.invalid_working_dirs),
            ("Workspace file already exists: ", workspace.name_conflicts),
        ]
    ]
    return _one_per_line(message_lists)
