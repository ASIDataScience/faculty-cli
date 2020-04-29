# faculty-cli

`faculty` is the command line interface to the [Faculty platform](https://faculty.ai/products-services/platform/).

## Enabling shell auto-completion

`faculty` provides auto-completion support for Bash, Zsh and Fish. 

## Bash

The completion script depends on `bash-completion`. To test if you have 
`bash-completion` already installed, run `type _init_completion`.

### Install `bash-completion`

#### Linux

`bash-completion` is provided by many package managers. You can install it 
with, e.g. `apt-get install bash-completion`. Reload your shell and run 
`type _init_completion`. If the command succeeds, you’re already set, otherwise 
add the following to your `~/.bashrc` file:

```
source /usr/share/bash-completion/bash_completion
```

#### macOS

`bash-completion` is not well supported by Bash 3.2, the default shell for 
macOS. Therefore, we recommend upgrading the default shell to a newer version
of Bash, which is currently Bash 5.0. 

You can then install `bash-completion v2` (for Bash 4.1+) with Homebrew:

```
brew install bash-completion@2
```

As stated in the output of this command, add the following to your `~/.bashrc` 
file:

```
export BASH_COMPLETION_COMPAT_DIR="/usr/local/etc/bash_completion.d"
[[ -r "/usr/local/etc/profile.d/bash_completion.sh" ]] && . "/usr/local/etc/profile.d/bash_completion.sh"
```

Reload your shell and verify that `bash-completion` is correctly installed 
with `type _init_completion`.


### Enable auto-completion

The `faculty` completion script for Bash can be generated with the command 
`faculty completion bash`. Sourcing the completion script in your shell enables 
auto-completion. To ensure the `faculty` completion scripts gets
sourced in all your shell sessions, add the following to your `~/.bashrc` file:

```
source <(faculty completion bash)
```

After reloading your shell, `faculty` auto-completion should be working.

## Zsh

The faculty completion script for Zsh can be generated with the command 
`faculty completion zsh`. Sourcing the completion script in your shell enables 
auto-completion. To do so in all your shell sessions, add the following to your 
`~/.zshrc` file:

```
source <(faculty completion zsh)
```

After reloading your shell, `faculty` auto-completion should be working.

If you get an error like `command not found: compdef`, then add the following 
to the beginning of your `~/.zshrc` file:

```
autoload -Uz compinit && compinit
```

## Fish

The faculty completion script for Fish can be generated with the command 
`faculty completion fish`. Sourcing the completion script in your shell enables 
auto-completion. To do so in all your shell sessions, add the following to your 
`~/.config/fish/config.fish` file:

```
faculty completion fish | source
```