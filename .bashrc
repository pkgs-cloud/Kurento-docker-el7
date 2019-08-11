# .bashrc

# User specific aliases and functions

alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

alias rpmbb='rpmbuild -bb --define="dist .el7"'
alias rpmbs='rpmbuild -bs --define="dist .el7"'
alias yumi='yum install -y'
alias yumr='yum reinstall -y'
alias yume='yum erase -y'
alias yumd='yum downgrade -y'
alias yumbd='yum-builddep -y'
alias rpmsrc='spectool -R -g'
