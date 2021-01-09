import os
import textwrap
import uuid

from click.testing import CliRunner
import pytest

from faculty_cli.cli import cli
from faculty.clients.account import AccountClient
from faculty.clients.template import (
    TemplateClient,
    GenericParsingError,
    DefaultParametersParsingError,
    ResourceValidationError,
    AppValidationFailure,
    ApiValidationFailure,
    EnvironmentValidationFailure,
    JobValidationFailure,
    WorkspaceValidationFailure,
    ParameterValidationError,
    TemplateRetrievalError,
)
from faculty.clients.notification import NotificationClient
from faculty.clients.project import Project

USER_ID = uuid.uuid4()
SOURCE_PROJECT_ID = uuid.uuid4()
TARGET_PROJECT_ID = uuid.uuid4()

TARGET_PROJECT = Project(
    id=TARGET_PROJECT_ID, name="target-project", owner_id=USER_ID
)

CUSTOM_SOURCE_DIRS = [
    ("source/dir", "/project/source/dir", "/source/dir"),
    ("", "/project", "/"),
    ("", "/project/path", "/path"),
    (".", "/project", "/"),
    (".", "/project/path", "/path"),
    ("/project", "/project", "/"),
    ("/project/", "/project", "/"),
    ("/project/path", "/project/path", "/path"),
]

PUBLISHING_ERRORS = [
    (GenericParsingError("generic parsing error"), "generic parsing error\n"),
    (
        DefaultParametersParsingError("param parsing error"),
        "param parsing error\n",
    ),
    (
        ResourceValidationError(
            apps=AppValidationFailure(
                subdomain_conflicts=["app-subdomain-1"],
                name_conflicts=["test-app-name-1", "test-app-name-2"],
                invalid_working_dirs=["invalid/app/dir"],
            ),
            apis=ApiValidationFailure(
                subdomain_conflicts=["api-subdomain-1"],
                name_conflicts=["test-api-name"],
                invalid_working_dirs=["invalid/API/dir"],
            ),
            environments=EnvironmentValidationFailure(
                name_conflicts=["test-env-name"], invalid_names=["invalid#env"]
            ),
            jobs=JobValidationFailure(
                name_conflicts=["test-job-name"],
                invalid_working_dirs=[],
                invalid_names=["invalid#job"],
            ),
            workspace=WorkspaceValidationFailure(
                name_conflicts=["test-file-path"]
            ),
        ),
        textwrap.dedent(
            """\
                App subdomain already exists: app-subdomain-1
                App name already exists: test-app-name-1
                App name already exists: test-app-name-2
                Invalid app working directory: invalid/app/dir
                API subdomain already exists: api-subdomain-1
                API name already exists: test-api-name
                Invalid API working directory: invalid/API/dir
                Environment name already exists: test-env-name
                Invalid environment name: invalid#env
                Job name already exists: test-job-name
                Invalid job name: invalid#job
                Workspace file already exists: test-file-path
            """
        ),
    ),
    (
        ParameterValidationError(
            errors=["test param 1 error", "test param 2 error"]
        ),
        textwrap.dedent(
            """\
            Parameter validation failed: test param 1 error
            Parameter validation failed: test param 2 error
        """
        ),
    ),
    (
        TemplateRetrievalError(
            apps=["app error"],
            apis=["API error"],
            environments=["env error"],
            jobs=["job error"],
        ),
        textwrap.dedent(
            """\
            Error reading app resource definition: app error
            Error reading API resource definition: API error
            Error reading environment resource definition: env error
            Error reading app job definition: job error
        """
        ),
    ),
]


def test_init():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["template", "init"])
        assert result.exit_code == 0
        assert os.path.isfile("parameters.yaml")
        assert os.path.isdir("faculty-resources")
        assert os.path.isdir("workspace")


def test_publish_new_template_missing_project_id(mocker):
    mocker.patch.object(
        AccountClient, "authenticated_user_id", return_value=USER_ID
    )

    runner = CliRunner(mix_stderr=False, env={"FACULTY_PROJECT_ID": None})
    result = runner.invoke(cli, ["template", "publish", "new", "name"])

    assert result.exit_code >= 1
    assert (
        result.stderr
        == "This command is meant to be used from inside a Faculty server.\n"
    )


def test_publish_new_template_success(mocker):
    mocker.patch.object(
        AccountClient, "authenticated_user_id", return_value=USER_ID
    )
    mocker.patch("os.path.abspath", return_value="/project/src/")
    mock_notifications = mocker.Mock()
    notifications_mock = mocker.patch.object(
        NotificationClient,
        "publish_template_notifications",
        return_value=mock_notifications,
    )
    publish_new_mock = mocker.patch.object(TemplateClient, "publish_new")

    runner = CliRunner(
        mix_stderr=False, env={"FACULTY_PROJECT_ID": str(SOURCE_PROJECT_ID)}
    )
    result = runner.invoke(cli, ["template", "publish", "new", "name"])
    assert result.exit_code == 0
    assert result.stdout == "Successfully published template `name`.\n"

    notifications_mock.assert_called_once_with(USER_ID, SOURCE_PROJECT_ID)
    publish_new_mock.assert_called_once_with(
        SOURCE_PROJECT_ID, "name", "/src/"
    )
    mock_notifications.wait_for_completion.assert_called_once_with()


@pytest.mark.parametrize(
    "input_src_dir, mock_abs_src_dir, expected_src_dir", CUSTOM_SOURCE_DIRS
)
def test_publish_new_template_custom_source_dir(
    mocker, input_src_dir, mock_abs_src_dir, expected_src_dir
):
    mocker.patch.object(
        AccountClient, "authenticated_user_id", return_value=USER_ID
    )
    mocker.patch("os.path.abspath", return_value=mock_abs_src_dir)
    mock_notifications = mocker.Mock()
    notifications_mock = mocker.patch.object(
        NotificationClient,
        "publish_template_notifications",
        return_value=mock_notifications,
    )
    publish_new_mock = mocker.patch.object(TemplateClient, "publish_new")

    runner = CliRunner(
        mix_stderr=False, env={"FACULTY_PROJECT_ID": str(SOURCE_PROJECT_ID)}
    )
    result = runner.invoke(
        cli, ["template", "publish", "new", "name", input_src_dir]
    )
    assert result.exit_code == 0
    assert result.stdout == "Successfully published template `name`.\n"

    notifications_mock.assert_called_once_with(USER_ID, SOURCE_PROJECT_ID)
    publish_new_mock.assert_called_once_with(
        SOURCE_PROJECT_ID, "name", expected_src_dir
    )
    mock_notifications.wait_for_completion.assert_called_once_with()


def test_publish_new_template_outside_project(mocker):
    mocker.patch.object(
        AccountClient, "authenticated_user_id", return_value=USER_ID
    )
    mocker.patch("os.path.abspath", return_value="/outside/project")
    runner = CliRunner(
        mix_stderr=False, env={"FACULTY_PROJECT_ID": str(SOURCE_PROJECT_ID)}
    )
    result = runner.invoke(
        cli, ["template", "publish", "new", "name", "/outside/project"]
    )
    assert result.exit_code >= 1
    assert result.stderr == (
        "Source directory must be under /project. "
        "This command is meant to be used from inside a Faculty server.\n"
    )


@pytest.mark.parametrize("mock_exception, expected_message", PUBLISHING_ERRORS)
def test_publish_new_template_validation_errors(
    mocker, mock_exception, expected_message
):
    mocker.patch.object(
        AccountClient, "authenticated_user_id", return_value=USER_ID
    )
    mocker.patch("os.path.abspath", return_value="/project/src/")
    mock_notifications = mocker.Mock()
    notifications_mock = mocker.patch.object(
        NotificationClient,
        "publish_template_notifications",
        return_value=mock_notifications,
    )
    publish_new_mock = mocker.patch.object(
        TemplateClient, "publish_new", side_effect=mock_exception
    )

    runner = CliRunner(
        mix_stderr=False, env={"FACULTY_PROJECT_ID": str(SOURCE_PROJECT_ID)}
    )
    result = runner.invoke(cli, ["template", "publish", "new", "name"])
    assert result.exit_code == 64
    assert result.stderr == expected_message

    notifications_mock.assert_called_once_with(USER_ID, SOURCE_PROJECT_ID)
    publish_new_mock.assert_called_once_with(
        SOURCE_PROJECT_ID, "name", "/src/"
    )


def test_add_to_project_from_directory_missing_project_id(mocker):
    mocker.patch.object(
        AccountClient, "authenticated_user_id", return_value=USER_ID
    )
    mocker.patch(
        "faculty_cli.cli._list_projects", return_value=[TARGET_PROJECT]
    )
    runner = CliRunner(mix_stderr=False, env={"FACULTY_PROJECT_ID": None})
    result = runner.invoke(
        cli, ["template", "add-to-project-from-directory", "target-project"]
    )

    assert result.exit_code >= 1
    assert (
        result.stderr
        == "This command is meant to be used from inside a Faculty server.\n"
    )


def test_add_to_project_from_directory(mocker):
    mocker.patch.object(
        AccountClient, "authenticated_user_id", return_value=USER_ID
    )
    mocker.patch(
        "faculty_cli.cli._list_projects", return_value=[TARGET_PROJECT]
    )
    mocker.patch("os.path.abspath", return_value="/project/src/")
    mock_notifications = mocker.Mock()
    notifications_mock = mocker.patch.object(
        NotificationClient,
        "add_to_project_from_dir_notifications",
        return_value=mock_notifications,
    )
    add_to_project_from_directory_mock = mocker.patch.object(
        TemplateClient, "add_to_project_from_directory"
    )

    runner = CliRunner(
        mix_stderr=False, env={"FACULTY_PROJECT_ID": str(SOURCE_PROJECT_ID)}
    )
    result = runner.invoke(
        cli,
        [
            "template",
            "add-to-project-from-directory",
            "target-project",
            "-p",
            "param1",
            "1",
        ],
    )

    assert result.exit_code == 0
    assert (
        result.stdout
        == "Successfully applied template to project target-project.\n"
    )

    notifications_mock.assert_called_once_with(USER_ID, TARGET_PROJECT_ID)
    add_to_project_from_directory_mock.assert_called_once_with(
        SOURCE_PROJECT_ID, "/src/", TARGET_PROJECT_ID, "/", {"param1": "1"}
    )
    mock_notifications.wait_for_completion.assert_called_once_with()


@pytest.mark.parametrize(
    "input_src_dir, mock_abs_src_dir, expected_src_dir", CUSTOM_SOURCE_DIRS
)
def test_add_to_project_from_directory_custom_source_dir(
    mocker, input_src_dir, mock_abs_src_dir, expected_src_dir
):
    mocker.patch.object(
        AccountClient, "authenticated_user_id", return_value=USER_ID
    )
    mocker.patch(
        "faculty_cli.cli._list_projects", return_value=[TARGET_PROJECT]
    )
    mocker.patch("os.path.abspath", return_value=mock_abs_src_dir)
    mock_notifications = mocker.Mock()
    notifications_mock = mocker.patch.object(
        NotificationClient,
        "add_to_project_from_dir_notifications",
        return_value=mock_notifications,
    )
    add_to_project_from_directory_mock = mocker.patch.object(
        TemplateClient, "add_to_project_from_directory"
    )

    runner = CliRunner(
        mix_stderr=False, env={"FACULTY_PROJECT_ID": str(SOURCE_PROJECT_ID)}
    )
    result = runner.invoke(
        cli,
        [
            "template",
            "add-to-project-from-directory",
            "target-project",
            "-p",
            "param1",
            "1",
        ],
    )

    assert result.exit_code == 0
    assert (
        result.stdout
        == "Successfully applied template to project target-project.\n"
    )

    notifications_mock.assert_called_once_with(USER_ID, TARGET_PROJECT_ID)
    add_to_project_from_directory_mock.assert_called_once_with(
        SOURCE_PROJECT_ID,
        expected_src_dir,
        TARGET_PROJECT_ID,
        "/",
        {"param1": "1"},
    )
    mock_notifications.wait_for_completion.assert_called_once_with()


@pytest.mark.parametrize("mock_exception, expected_message", PUBLISHING_ERRORS)
def test_add_to_project_from_directory_validation_errors(
    mocker, mock_exception, expected_message
):
    mocker.patch.object(
        AccountClient, "authenticated_user_id", return_value=USER_ID
    )
    mocker.patch(
        "faculty_cli.cli._list_projects", return_value=[TARGET_PROJECT]
    )
    mocker.patch("os.path.abspath", return_value="/project/src/")
    mock_notifications = mocker.Mock()
    notifications_mock = mocker.patch.object(
        NotificationClient,
        "add_to_project_from_dir_notifications",
        return_value=mock_notifications,
    )
    add_to_project_from_directory_mock = mocker.patch.object(
        TemplateClient,
        "add_to_project_from_directory",
        side_effect=mock_exception,
    )

    runner = CliRunner(
        mix_stderr=False, env={"FACULTY_PROJECT_ID": str(SOURCE_PROJECT_ID)}
    )
    result = runner.invoke(
        cli,
        [
            "template",
            "add-to-project-from-directory",
            "target-project",
            "-p",
            "param1",
            "1",
        ],
    )

    assert result.exit_code == 64
    assert result.stderr == expected_message

    notifications_mock.assert_called_once_with(USER_ID, TARGET_PROJECT_ID)
    add_to_project_from_directory_mock.assert_called_once_with(
        SOURCE_PROJECT_ID, "/src/", TARGET_PROJECT_ID, "/", {"param1": "1"}
    )
