### Building Kurento and FreeSWITCH for CentOS 7 and Amazon Linux 2

**Kurento 6.16.0, FreeSWITCH 1.10.5**

Kurento depends on several custom libraries and tools such as Boost 1.55 and a customized version of GStreamer. To avoid possible conflicts with system libraries and tools, some Kurento dependencies are built and installed under `/opt/kms` folder.

`SOURCES` folder contains patches and various configuration files only. Sources for each package will be downloaded from upstream locations automatically.

`SOURCES.snapshot` folder contains a snapshot of all sources downloaded from upstream locations. In case upstream is unavailable, you can copy a missing file from `SOURCES.snapshot` to `SOURCES`.

1. Install Docker on your system. And clone this repository.

2. Change current directory to the cloned repository and build Kurento with dependencies.

	```
	cd Kurento-docker-el7

	# CentOS/EL 7
	./build-kurento.sh 6.16.0 el7

	# Amazon Linux 2
	./build-kurento.sh 6.16.0 amzn2
	```

3. FreeSWITCH can be built after Kurento build is ready for the OS distribution selected in previous step.
FreeSWITCH shares some dependencies with Kurento, such as FFmpeg and Opus.

	```
	# CentOS/EL 7
	./build-freeswitch.sh 6.16.0 el7

	# Amazon Linux 2
	./build-freeswitch.sh 6.16.0 amzn2
	```

4. All RPM packages for Kurento and FreeSWITCH are saved to `6.16.0/RPMS.el7` and `6.16.0/RPMS.amzn2` folders for each OS distribution respectively.

### Installing Kurento (and FreeSWITCH) on CentOS/RHEL 7 and Amazon Linux 2

1. Use **minimal** system installation

2. For EL7 copy `6.16.0/RPMS.el7` folder onto your target system as `/root/RPMS`. For Amazon Linux 2 use `6.16.0/RPMS.amzn2` folder

3. Copy `install-kurento.sh` from this repository into `/root`

4. Run installation script

	```
	chmod +x install-kurento.sh && ./install-kurento.sh
	```

### Running Kurento and FreeSWITCH on CentOS/RHEL 7 and Amazon Linux 2

* To start, stop, restart, enable, disable Kurento Media Server service

	```
	systemctl start kms
	systemctl stop kms
	systemctl restart kms
	systemctl enable kms
	systemctl disable kms
	```

* FreeSWITCH service can be managed similarly

	```
	systemctl start freeswitch
	systemctl stop freeswitch
	systemctl restart freeswitch
	systemctl enable freeswitch
	systemctl disable freeswitch
	```

* Make sure to allow connections to the port range used by Kurento and FreeSWITCH or disable firewall completely for testing purposes

	```
	systemctl stop firewalld ; systemctl disable firewalld
	```

* Config files are in `/etc/kurento`, `/etc/freeswitch` folders

* The log files are under `/var/log/kurento`, `/var/log/freeswitch` folders

* Startup environment variables and arguments can be changed by editing `/etc/sysconfig/kms`, `/etc/sysconfig/freeswitch` files
