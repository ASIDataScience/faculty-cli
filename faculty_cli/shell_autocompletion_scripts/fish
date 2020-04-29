function __fish_faculty_list_projects
    command faculty project list 2>/dev/null
end

function __fish_faculty_list_all_servers_verbose
    set cmd (commandline -opc)
    command faculty server list $cmd[-1] --all --verbose 2>/dev/null | tail -n +2
end

function __fish_faculty_list_environments
    set cmd (commandline -opc)
    command faculty environment list $cmd[-2] 2>/dev/null
end

function __fish_faculty_list_jobs
    set cmd (commandline -opc)
    command faculty job list $cmd[-1] 2>/dev/null
end

function __fish_faculty_list_runs
    set cmd (commandline -opc)
    command faculty job list-runs $cmd[-2] $cmd[-1] 2>/dev/null
end

function __fish_faculty_list_instance_types
    command faculty server instance-types 2>/dev/null
end

function __fish_faculty_list_instance_types_verbose
    command faculty server instance-types --verbose 2>/dev/null | tail -n +2
end

function __fish_faculty_dirname
    if test -z "$argv[1]" -o $argv[1] = '/project'
        set p '/project/'
    else
        if test (string sub $argv[1] --start -1 = '/')
            set p $argv[1]
        else
            set p (dirname $argv[1])/
        end
    end
    echo $p
end

function __fish_faculty_remote_path_completions
    set cmd (commandline -opc)
    set p (__fish_faculty_dirname (echo (commandline -ct) | sed -e 's/\\\ / /g'))
    faculty file ls $cmd[4] $p
end

function __fish_faculty_local_path_completions
    set p (echo (commandline -ct) | sed -e 's/\\\ / /g')
    __fish_complete_path $p
end

# common options

complete -c faculty -x
complete -c faculty -l help -d 'Display help and exit.'

# list available servers, when server is an option (i.e. --server)
# this assumes the Project is in the fourth position

function __fish_faculty_server_is_option
    set cmd (commandline -opc)
    if [ (count $cmd) -ge 1 ]
        and [ $cmd[-1] = '--server' ]
        return 0
    end
    return 1
end

function __fish_faculty_list_servers_if_option
    set cmd (commandline -opc)
    command faculty server list $cmd[4] --verbose --all 2>/dev/null | tail -n +2
end

complete -c faculty -n "__fish_faculty_server_is_option" -x -a '(string split "\n" (__fish_faculty_list_servers_if_option) | awk -F\'[[:space:]][[:space:]]+\' \'{ print $1 "\t" "Type: " $2 ", Machine Type: " $3 ", CPUs: " $4 ", RAM: " $5 ", Status: " $6 ", Started: " $8}\')'

# list available environments, when environment is an option (i.e. --environment)
# this assumes the Project is in the fourth position

function __fish_faculty_environment_is_option
    set cmd (commandline -opc)
    if [ (count $cmd) -ge 1 ]
        and [ $cmd[-1] = '--environment' ]
        return 0
    end
    return 1
end

function __fish_faculty_list_environments_if_option
    set cmd (commandline -opc)
    command faculty environment list $cmd[4]
end

complete -c faculty -n "__fish_faculty_environment_is_option" -x -a "(__fish_faculty_list_environments_if_option)"

# list available server types, when type is an option (i.e. --type)

function __fish_faculty_type_is_option
    set cmd (commandline -opc)
    if [ (count $cmd) -ge 1 ]
        and [ $cmd[-1] = '--type' ]
        return 0
    end
    return 1
end

complete -c faculty -n "__fish_faculty_type_is_option" -x -a "jupyter jupyterlab rstudio"

# list available machine types, when machine-type is an option (i.e. --machine-type)

function __fish_faculty_machine_type_is_option
    set cmd (commandline -opc)
    if [ (count $cmd) -ge 1 ]
        and [ $cmd[-1] = '--machine-type' ]
        return 0
    end
    return 1
end

complete -c faculty -n "__fish_faculty_machine_type_is_option" -x -a '(string split "\n" (__fish_faculty_list_instance_types_verbose) | awk -F\' \' \'{ print $1 "\t" "CPUs: " $2 ", Ram: " $3 " GB, GPUs: " $5 ", Cost: $" $(NF-2) " / hr" }\')'

# environment

complete -c faculty -n "__fish_is_first_token" -a environment -d "Manipulate Faculty server environments."

complete -c faculty -n "__fish_seen_subcommand_from environment; and __fish_is_token_n 3" -x -a apply -d "Apply an environment to the server."
complete -c faculty -n "__fish_seen_subcommand_from environment; and __fish_seen_subcommand_from apply; and __fish_is_token_n 4" -x -a "(__fish_faculty_list_projects)"
complete -c faculty -n "__fish_seen_subcommand_from environment; and __fish_seen_subcommand_from apply; and __fish_is_token_n 5" -x -a '(string split "\n" (__fish_faculty_list_servers_if_option) | awk -F\'[[:space:]][[:space:]]+\' \'{ print $1 "\t" "Type: " $2 ", Machine Type: " $3 ", CPUs: " $4 ", RAM: " $5 ", Status: " $6 ", Started: " $8}\')'
complete -c faculty -n "__fish_seen_subcommand_from environment; and __fish_seen_subcommand_from apply; and __fish_is_token_n 6" -x -a "(__fish_faculty_list_environments)"

complete -c faculty -n "__fish_seen_subcommand_from environment; and __fish_is_token_n 3" -x -a list -d "List your environments."
complete -c faculty -n "__fish_seen_subcommand_from environment; and __fish_seen_subcommand_from list; and __fish_is_token_n 4" -x -a "(__fish_faculty_list_projects)"
complete -c faculty -n "__fish_seen_subcommand_from environment; and __fish_seen_subcommand_from list" -s v -l verbose -d "Print extra information about environments."

complete -c faculty -n "__fish_seen_subcommand_from environment; and __fish_is_token_n 3" -x -a logs -d "Stream the logs for a server environment application."
complete -c faculty -n "__fish_seen_subcommand_from environment; and __fish_seen_subcommand_from logs; and __fish_is_token_n 4" -x -a "(__fish_faculty_list_projects)"
complete -c faculty -n "__fish_seen_subcommand_from environment; and __fish_seen_subcommand_from logs; and __fish_is_token_n 5" -x -a '(string split "\n" (__fish_faculty_list_servers_if_option) | awk -F\'[[:space:]][[:space:]]+\' \'{ print $1 "\t" "Type: " $2 ", Machine Type: " $3 ", CPUs: " $4 ", RAM: " $5 ", Status: " $6 ", Started: " $8}\')'
complete -c faculty -n "__fish_seen_subcommand_from environment; and __fish_seen_subcommand_from logs" -s s -l step -d "Display only the logs for this step."

complete -c faculty -n "__fish_seen_subcommand_from environment; and __fish_is_token_n 3" -x -a status -d "Get the execution status for an environment."
complete -c faculty -n "__fish_seen_subcommand_from environment; and __fish_seen_subcommand_from status; and __fish_is_token_n 4" -x -a "(__fish_faculty_list_projects)"
complete -c faculty -n "__fish_seen_subcommand_from environment; and __fish_seen_subcommand_from status; and __fish_is_token_n 5" -x -a '(string split "\n" (__fish_faculty_list_servers_if_option) | awk -F\'[[:space:]][[:space:]]+\' \'{ print $1 "\t" "Type: " $2 ", Machine Type: " $3 ", CPUs: " $4 ", RAM: " $5 ", Status: " $6 ", Started: " $8}\')'

# file

complete -c faculty -n "__fish_is_first_token" -a file -d "Manipulate files in a Faculty project."

complete -c faculty -n "__fish_seen_subcommand_from file; and __fish_is_token_n 3" -x -a get -d "Copy a file from the Faculty workspace to the local machine."
complete -c faculty -n "__fish_seen_subcommand_from file; and __fish_seen_subcommand_from get; and __fish_is_token_n 4" -x -a "(__fish_faculty_list_projects)"
complete -c faculty -n "__fish_seen_subcommand_from file; and __fish_seen_subcommand_from get; and __fish_is_token_n 5" -a '(__fish_faculty_remote_path_completions)'
complete -c faculty -n "__fish_seen_subcommand_from file; and __fish_seen_subcommand_from get; and __fish_is_token_n 6" -a '(__fish_faculty_local_path_completions)'

complete -c faculty -n "__fish_seen_subcommand_from file; and __fish_is_token_n 3" -x -a put -d "Copy a local file to the Faculty workspace."
complete -c faculty -n "__fish_seen_subcommand_from file; and __fish_seen_subcommand_from put; and __fish_is_token_n 4" -x -a "(__fish_faculty_list_projects)"
complete -c faculty -n "__fish_seen_subcommand_from file; and __fish_seen_subcommand_from put; and __fish_is_token_n 5" -a '(__fish_faculty_local_path_completions)'
complete -c faculty -n "__fish_seen_subcommand_from file; and __fish_seen_subcommand_from put; and __fish_is_token_n 6" -a '(__fish_faculty_remote_path_completions)'

complete -c faculty -n "__fish_seen_subcommand_from file; and __fish_is_token_n 3" -x -a sync-down -d "Sync remote files down from project with rsync."
complete -c faculty -n "__fish_seen_subcommand_from file; and __fish_seen_subcommand_from sync-down; and __fish_is_token_n 4" -x -a "(__fish_faculty_list_projects)"
complete -c faculty -n "__fish_seen_subcommand_from file; and __fish_seen_subcommand_from sync-down; and __fish_is_token_n 5" -a '(__fish_faculty_remote_path_completions)'
complete -c faculty -n "__fish_seen_subcommand_from file; and __fish_seen_subcommand_from sync-down; and __fish_is_token_n 6" -a '(__fish_faculty_local_path_completions)'

complete -c faculty -n "__fish_seen_subcommand_from file; and __fish_is_token_n 3" -x -a sync-up -d "Sync local files up to a project with rsync."
complete -c faculty -n "__fish_seen_subcommand_from file; and __fish_seen_subcommand_from sync-up; and __fish_is_token_n 4" -x -a "(__fish_faculty_list_projects)"
complete -c faculty -n "__fish_seen_subcommand_from file; and __fish_seen_subcommand_from sync-up; and __fish_is_token_n 5" -a '(__fish_faculty_local_path_completions)'
complete -c faculty -n "__fish_seen_subcommand_from file; and __fish_seen_subcommand_from sync-up; and __fish_is_token_n 6" -a '(__fish_faculty_remote_path_completions)'

complete -c faculty -n "__fish_seen_subcommand_from file; and __fish_is_token_n 3" -x -a ls -d "List files and directories on the Faculty workspace."
complete -c faculty -n "__fish_seen_subcommand_from file; and __fish_seen_subcommand_from ls; and __fish_is_token_n 4" -x -a "(__fish_faculty_list_projects)"
complete -c faculty -n "__fish_seen_subcommand_from file; and __fish_seen_subcommand_from ls; and __fish_is_token_n 5" -a '(__fish_faculty_remote_path_completions)'

complete -c faculty -n "__fish_seen_subcommand_from file; and __fish_is_token_n 4" -x -a "(__fish_faculty_list_projects)"
complete -c faculty -n "__fish_seen_subcommand_from file" -l server -d "Name or ID of server to use."

# login

complete -c faculty -n "__fish_is_first_token" -a login -d "Write Faculty credentials to file."

# project

complete -c faculty -n "__fish_is_first_token" -a project -d "Manipulate Faculty projects."
complete -c faculty -n "__fish_seen_subcommand_from project; and __fish_is_token_n 3" -x -a list -d "List accessible Faculty projects."
complete -c faculty -n "__fish_seen_subcommand_from project; and __fish_seen_subcommand_from list" -s v -l verbose -d "Print extra information about projects."

# completion

complete -c faculty -n "__fish_is_first_token" -a completion -d "Generate auto-completion scripts for faculty_cli."
complete -c faculty -n "__fish_seen_subcommand_from completion; and __fish_is_token_n 3" -x -a bash
complete -c faculty -n "__fish_seen_subcommand_from completion; and __fish_is_token_n 3" -x -a zsh
complete -c faculty -n "__fish_seen_subcommand_from completion; and __fish_is_token_n 3" -x -a fish

# server

complete -c faculty -n "__fish_is_first_token" -a server -d "Manipulate Faculty servers."

complete -c faculty -n "__fish_seen_subcommand_from server; and __fish_is_token_n 3" -x -a list -d "List your Faculty servers."
complete -c faculty -n "__fish_seen_subcommand_from server; and __fish_seen_subcommand_from list; and __fish_is_token_n 4" -x -a "(__fish_faculty_list_projects)"
complete -c faculty -n "__fish_seen_subcommand_from server; and __fish_seen_subcommand_from list" -s v -l verbose -d "Print extra information about servers."
complete -c faculty -n "__fish_seen_subcommand_from server; and __fish_seen_subcommand_from list" -s a -l all -d "Show all servers, not just running ones."

complete -c faculty -n "__fish_seen_subcommand_from server; and __fish_is_token_n 3" -x -a new -d "Create a new Faculty server."
complete -c faculty -n "__fish_seen_subcommand_from server; and __fish_seen_subcommand_from new; and __fish_is_token_n 4" -x -a "(__fish_faculty_list_projects)"
complete -c faculty -n "__fish_seen_subcommand_from server; and __fish_seen_subcommand_from new; and not __fish_seen_subcommand_from --cores; and not __fish_seen_subcommand_from --machine-type" -l cores -d "Number of CPU cores  [default: 1]."
complete -c faculty -n "__fish_seen_subcommand_from server; and __fish_seen_subcommand_from new; and not __fish_seen_subcommand_from --memory; and not __fish_seen_subcommand_from --machine-type" -l memory -d "Server memory in GB  [default: 4]."
complete -c faculty -n "__fish_seen_subcommand_from server; and __fish_seen_subcommand_from new; and not __fish_seen_subcommand_from --type" -l type -d "Server type  [default: jupyter]."
complete -c faculty -n "__fish_seen_subcommand_from server; and __fish_seen_subcommand_from new; and not __fish_seen_subcommand_from --machine-type; and not __fish_seen_subcommand_from --cores; and not __fish_seen_subcommand_from --memory" -l machine-type -d "Machine type for a dedicated instance."
complete -c faculty -n "__fish_seen_subcommand_from server; and __fish_seen_subcommand_from new; and not __fish_seen_subcommand_from --version" -l version -d "Server image version [advanced]."
complete -c faculty -n "__fish_seen_subcommand_from server; and __fish_seen_subcommand_from new; and not __fish_seen_subcommand_from --name" -l name -d "Name to assign to the server."
complete -c faculty -n "__fish_seen_subcommand_from server; and __fish_seen_subcommand_from new; and not __fish_seen_subcommand_from --environment" -l environment -d "Environments to apply to the server."
complete -c faculty -n "__fish_seen_subcommand_from server; and __fish_seen_subcommand_from new; and not __fish_seen_subcommand_from --wait" -l wait -d "Wait until the server is running before exiting."

complete -c faculty -n "__fish_seen_subcommand_from server; and __fish_is_token_n 3" -x -a open -d "Open a Faculty server in your browser."
complete -c faculty -n "__fish_seen_subcommand_from server; and __fish_seen_subcommand_from open; and __fish_is_token_n 4" -x -a "(__fish_faculty_list_projects)"
complete -c faculty -n "__fish_seen_subcommand_from server; and __fish_seen_subcommand_from open" -l server -d "Name or ID of server to use."

complete -c faculty -n "__fish_seen_subcommand_from server; and __fish_is_token_n 3" -x -a terminate -d "Terminate a Faculty server."
complete -c faculty -n "__fish_seen_subcommand_from server; and __fish_seen_subcommand_from terminate; and __fish_is_token_n 4" -x -a "(__fish_faculty_list_projects)"
complete -c faculty -n "__fish_seen_subcommand_from server; and __fish_seen_subcommand_from terminate; and __fish_is_token_n 5" -x -a '(string split "\n" (__fish_faculty_list_all_servers_verbose) | awk -F\'[[:space:]][[:space:]]+\' \'{ print $1 "\t" "Type: " $2 ", Machine Type: " $3 ", CPUs: " $4 ", RAM: " $5 ", Status: " $6 ", Started: " $8}\')'

complete -c faculty -n "__fish_seen_subcommand_from server; and __fish_is_token_n 3" -x -a instance-types -d "List the types of servers available on dedicated infrastructure."
complete -c faculty -n "__fish_seen_subcommand_from server; and __fish_seen_subcommand_from instance-types" -s v -l verbose -d "Print extra information about instance types."

# shell

complete -c faculty -n "__fish_is_first_token" -a shell -d "Open a shell on an Faculty server."
complete -c faculty -n "__fish_seen_subcommand_from shell; and __fish_is_token_n 3" -x -a "(__fish_faculty_list_projects)"
complete -c faculty -n "__fish_seen_subcommand_from shell; and __fish_is_token_n 4" -x -a '(string split "\n" (__fish_faculty_list_all_servers_verbose) | awk -F\'[[:space:]][[:space:]]+\' \'{ print $1 "\t" "Type: " $2 ", Machine Type: " $3 ", CPUs: " $4 ", RAM: " $5 ", Status: " $6 ", Started: " $8}\')'

# version

complete -c faculty -n "__fish_is_first_token" -a version -d "Print the faculty version number."

# job

complete -c faculty -n "__fish_is_first_token" -a job -d "Manipulate Faculty jobs."

complete -c faculty -n "__fish_seen_subcommand_from job; and __fish_is_token_n 3" -x -a list -d "List the jobs in a project."
complete -c faculty -n "__fish_seen_subcommand_from job; and __fish_seen_subcommand_from list; and __fish_is_token_n 4" -x -a "(__fish_faculty_list_projects)"
complete -c faculty -n "__fish_seen_subcommand_from job; and __fish_seen_subcommand_from list" -s v -l verbose -d "Print extra information about jobs."

complete -c faculty -n "__fish_seen_subcommand_from job; and __fish_is_token_n 3" -x -a list-runs -d "List the runs of a job."
complete -c faculty -n "__fish_seen_subcommand_from job; and __fish_seen_subcommand_from list-runs; and __fish_is_token_n 4" -x -a "(__fish_faculty_list_projects)"
complete -c faculty -n "__fish_seen_subcommand_from job; and __fish_seen_subcommand_from list-runs; and __fish_is_token_n 5" -x -a "(__fish_faculty_list_jobs)"
complete -c faculty -n "__fish_seen_subcommand_from job; and __fish_seen_subcommand_from list-runs" -s v -l verbose -d "Print extra information about runs."

complete -c faculty -n "__fish_seen_subcommand_from job; and __fish_is_token_n 3" -x -a logs -d "Print the logs for a run."
complete -c faculty -n "__fish_seen_subcommand_from job; and __fish_seen_subcommand_from logs; and __fish_is_token_n 4" -x -a "(__fish_faculty_list_projects)"
complete -c faculty -n "__fish_seen_subcommand_from job; and __fish_seen_subcommand_from logs; and __fish_is_token_n 5" -x -a "(__fish_faculty_list_jobs)"
complete -c faculty -n "__fish_seen_subcommand_from job; and __fish_seen_subcommand_from logs; and __fish_is_token_n 6" -x -a "(__fish_faculty_list_runs)"

complete -c faculty -n "__fish_seen_subcommand_from job; and __fish_is_token_n 3" -x -a run -d "Run a job."
complete -c faculty -n "__fish_seen_subcommand_from job; and __fish_seen_subcommand_from run; and __fish_is_token_n 4" -x -a "(__fish_faculty_list_projects)"
complete -c faculty -n "__fish_seen_subcommand_from job; and __fish_seen_subcommand_from run; and __fish_is_token_n 5" -x -a "(__fish_faculty_list_jobs)"
complete -c faculty -n "__fish_seen_subcommand_from job; and __fish_seen_subcommand_from run" -l num-subruns -d "Number of sub runs."