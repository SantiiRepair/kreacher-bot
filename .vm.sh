#!/bin/bash

sudo apt-get update && sudo apt-get upgrade -y

if ! command -v redis-cli >/dev/null 2>&1; then
    sudo apt-get install -y lsb-release curl gpg
    curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
    sudo apt-get update && sudo apt-get install redis -y
fi

if ! command -v git >/dev/null 2>&1; then
    sudo apt-get install git-all -y
fi

CHROME_PATH=$(which google-chrome 2>&1)

if ! [ -x $CHROME_PATH ]; then
    wget -O /tmp/google-chrome-stable_current_amd64.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo dpkg -i /tmp/google-chrome-stable_current_amd64.deb; sudo apt-get -fy install
    rm -rf /tmp/google-chrome-stable_current_amd64.deb
fi

if ! command -V python >/dev/null 2>&1; then
    if [ ! -r ~/.pyenv/ ]; then
        git clone https://github.com/pyenv/pyenv.git ~/.pyenv
        git clone https://github.com/pyenv/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
        cat << EOF >> ~/.bashrc
        export PYENV_ROOT="$HOME/.pyenv"
        export PATH="$PYENV_ROOT/bin:$PATH"
        if command -v pyenv 1>/dev/null 2>&1; then
            eval "$(pyenv init -)"
            eval "$(pyenv virtualenv-init -)" # Enable auto-activation of virtualenvs.
        fi
EOF
        source ~/.bashrc
        exec "$SHELL"
    fi

    pyenv install 3.11.6
    pyenv global 3.11.6
fi

if command -V python >/dev/null 2>&1; then
    installed=$(python --version | cut -d " " -f2)
    incompatible="3.12"
    if [[ $installed == $incompatible || $installed > $incompatible ]]; then
        if [ ! -r ~/.pyenv/ ]; then
            git clone https://github.com/pyenv/pyenv.git ~/.pyenv
            git clone https://github.com/pyenv/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
            cat << EOF >> ~/.bashrc
            export PYENV_ROOT="$HOME/.pyenv"
            export PATH="$PYENV_ROOT/bin:$PATH"
            if command -v pyenv 1>/dev/null 2>&1; then
                eval "$(pyenv init -)"
                eval "$(pyenv virtualenv-init -)" # Enable auto-activation of virtualenvs.
            fi
EOF
            source ~/.bashrc
            exec "$SHELL"
        fi

        pyenv install 3.11.6
        pyenv global 3.11.6
    fi
fi

make install