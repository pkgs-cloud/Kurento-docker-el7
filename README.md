### Building Kurento on CentOS 7

**Kurento 6.16.0**

Kurento depends on several custom libraries and tools such as Boost 1.55 and a customized version of Gstreamer. To avoid possible conflicts with system libraries and tools, some Kurento dependencies are built and installed under `/opt/kms` folder.

`SOURCES` folder contains patches and various configuration files only. Sources for each package will be downloaded from upstream locations automatically.

`SOURCES.snapshot` folder contains a snapshot of all sources downloaded from upstream locations. In case upstream is unavailable, you can copy a missing file from `SOURCES.snapshot` to `SOURCES`.

1. Install Docker on your system. And clone repository.

2. Change current directory to the cloned repository and build Kurento with dependencies.

	```
	cd Kurento-docker-el7
	./build-kurento.sh 6.16.0
	```

3. All RPM packages are saved to `6.16.0/RPMS` folder.

### Installing Kurento on CentOS/RHEL 7

1. Use **minimal** system installation

2. Copy `6.16.0/RPMS` folder onto your target system under `/root/RPMS`

3. Copy `install-kurento.sh` from this repository into `/root`

4. Run installation script

	```
	chmod +x install-kurento.sh && ./install-kurento.sh
	```

### Running Kurento on CentOS/RHEL 7

* To start, stop, restart, enable, disable Kurento Media Server service

	```
	systemctl start|stop|restart|enable|disable kms
	```

* Make sure to allow connections to the port range used by Kurento or disable firewall completely when testing

	```
	systemctl stop firewalld ; systemctl disable firewalld
	```

* Config files are in `/etc/kurento` folder

* The log files are under `/var/log/kurento` folder

* Startup environment variables and arguments are in `/etc/sysconfig/kms` file
