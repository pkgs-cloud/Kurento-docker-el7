### Building Kurento on CentOS 7

**Kurento 6.11.0**

Kurento depends on several custom libraries and tools such as Boost 1.55 and a customized version of Gstreamer. To avoid possible conflicts with system libraries and tools, some Kurento dependencies are built and installed under `/opt/kms` folder.

`SOURCES` folder contains patches and various configuration files only. Sources for each package will be downloaded from upstream locations automatically.

`SOURCES.snapshot` folder contains a snapshot of all sources downloaded from upstream locations. In case upstream is unavailable, you can copy a missing file from `SOURCES.snapshot` to `SOURCES`.

1. Install Docker on your system. And clone repository.

2. Build docker image (based on CentOS 7 Latest)

	```
	docker build -t rpm-build .
	```
	
3. Select Kurento version

	```
	cd 6.11.0
	```
	
4. Build Kurento dependencies

	```
	docker run -d \
	  -v $(pwd)/SPECS:/root/rpmbuild/SPECS \
	  -v $(pwd)/RPMS:/root/rpmbuild/RPMS \
	  -v $(pwd)/SOURCES:/root/rpmbuild/SOURCES \
	  -v $(pwd)/scripts:/root/scripts \
	  --name kurento-build-deps -t rpm-build
	  
	docker exec -it kurento-build-deps /root/scripts/build-deps.sh
	```
	
5. Build Kurento packages

	```
	docker run -d \
	  -v $(pwd)/SPECS:/root/rpmbuild/SPECS \
	  -v $(pwd)/RPMS:/root/rpmbuild/RPMS \
	  -v $(pwd)/SOURCES:/root/rpmbuild/SOURCES \
	  -v $(pwd)/scripts:/root/scripts \
	  --name kurento-build -t rpm-build
	  
	docker exec -it kurento-build /root/scripts/build.sh
	```
	
	Each Kurento and Gstreamer packages are being built from sources pulled from respective [https://github.com/Kurento](https://github.com/Kurento) repository. It uses git commit defined in the respective RPM spec file under `SPECS`.
	To update a package, modify a line in a spec file. For example:
	
	```
	%define commit b33143e
	```
	
	Also change `Version:` and/or `Release:` tags if necessary.

6. Optionally, delete Docker containers after successful build

	```
	docker stop kurento-build-deps kurento-build
	docker rm kurento-build-deps kurento-build
	```

5. All RPM packages are located in `RPMS` folder.

### Installing Kurento on CentOS/RHEL 7

1. Use **minimal** system installation

2. Copy `RPMS` folder onto your target system under `/root/RPMS`

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
