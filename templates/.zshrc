export ZSH=/home/romanpeters/.oh-my-zsh
ZSH_THEME="robbyrussell"

# DISABLE_AUTO_UPDATE="true"
export UPDATE_ZSH_DAYS=100
ENABLE_CORRECTION="true"
COMPLETION_WAITING_DOTS="true"
HIST_STAMPS="dd.mm.yyyy"

plugins=(
  git
  extract 
  git
  nmap
  rsync
  zsh-autosuggestions
  docker
)

source $ZSH/oh-my-zsh.sh

# User configuration

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

export LC_ALL=C.UTF-8
export LANG=C.UTF-8


alias srm="trash"
alias rm='echo "rm is disabled, use srm or /bin/rm instead."'
alias enter="source .venv/bin/activate || source venv/bin/activate"
alias permission="stat -c '%a %n' "
alias ha-check="docker run -it --rm -v /opt/homeassistant/config:/config -v /etc/localtime:/etc/localtime:ro homeassistant/amd64-homeassistant hass -c /config --script check_config"
alias ha-restart="docker restart homeassistant | lolcat"
alias ha-refresh="docker run -it --rm -v /opt/homeassistant/config:/config -v /etc/localtime:/etc/localtime:ro homeassistant/amd64-homeassistant hass -c /config --script check_config && docker restart homeassistant | lolcat"

# Show hostname
export PROMPT='${ret_status} %m %{$fg[cyan]%}%c%{$reset_color%} $(git_prompt_info)'
