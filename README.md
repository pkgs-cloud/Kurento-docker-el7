### Building Kurento on CentOS 7

1. Install Docker on your system. And clone repository.

2. Build docker image (based on CentOS 7.6 image) and run container

	```
	docker build -t el76-build .
	
	docker run -d \
	  -v $(pwd)/rpmbuild/SPECS:/root/rpmbuild/SPECS \
	  -v $(pwd)/rpmbuild/SRPMS:/root/rpmbuild/SRPMS \
	  -v $(pwd)/rpmbuild/RPMS:/root/rpmbuild/RPMS \
	  -v $(pwd)/rpmbuild/SOURCES:/root/rpmbuild/SOURCES \
	  --name kurento-build-el76 -t el76-build
	```

3. Enter bash within the container

	```
	docker exec -it kurento-build-el76 bash
	```

4. Build Kurento RPMs including all dependencies

	```
	cd && ./build-kurento.sh
	```
	
	Each Kurento and Gstreamer packages are being built from sources pulled from respective [https://github.com/Kurento](https://github.com/Kurento) repository. It uses git commit defined in the respective RPM spec file under `rpmbuild/SPECS`.
	To update a package, modify a line in a spec file. For example:
	
	```
	%define commit b33143e
	```
	
	Also change `Version:` and/or `Release:` tags if necessary.

5. All RPMs will be located under `/root/rpmbuild/RPMS` which is mapped to you local folder outside of the container.

### Installing Kurento on CentOS/RHEL 7

1. Use **minimal** system installation

2. Copy `rpmbuild/RPMS` folder onto your target system under `/root/RPMS`

3. Copy `install-kurento.sh` from this repository into `/root`

4. Run installation script

	```
	cd && chmod +x install-kurento.sh && ./install-kurento.sh
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
