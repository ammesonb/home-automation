#!/bin/bash
export TERM=xterm-256color
tmux -S /tmp/automation_dev new-session -d -s automation_dev \; send-keys "vi automation.py" Enter \; rename-window auto
tmux -S /tmp/automation_dev new-window -t automation_dev -n recog \; send-keys "vi recognition.py" Enter \;
tmux -S /tmp/automation_dev new-window -t automation_dev -n shared \; send-keys "vi shared.py" Enter \;
tmux -S /tmp/automation_dev new-window -t automation_dev -n act \; send-keys "vi actions.py" Enter \;
tmux -S /tmp/automation_dev new-window -t automation_dev -n ev \; send-keys "vi triggers.py" Enter \;
tmux -S /tmp/automation_dev new-window -t automation_dev -n psql \; send-keys "psql automation" Enter \;
tmux -S /tmp/automation_dev new-window -t automation_dev -n py \;
tmux -S /tmp/automation_dev new-window -t automation_dev -n todo \; send-keys "reset; grep -iHn todo * 2>&1 | grep -i todo" Enter
tmux -S /tmp/automation_dev new-window -t automation_dev -n git \; send-keys "git pull" Enter
