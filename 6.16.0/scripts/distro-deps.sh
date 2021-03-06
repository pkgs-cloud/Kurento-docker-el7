source <(cat /etc/os-release | grep ID)
DISTRO=${ID}${VERSION_ID}

if [ "$DISTRO" == "centos7" ]; then
  yumi centos-release-scl
  yumi devtoolset-7-gcc*
  #scl enable devtoolset-7 bash

  for filepath in `find /opt/rh/devtoolset-7/root/usr/bin/ -executable -type f`; do
    file=`basename $filepath`
    if [ -f /usr/bin/$file ] && [ ! -f /usr/bin/$file.orig ]; then
      mv /usr/bin/$file /usr/bin/$file.orig
      ln -s $filepath /usr/bin/$file
    fi
  done

  rm -f /etc/yum.repos.d/CentOS-SCLo-scl-rh.repo
fi

echo Building for $DISTRO
