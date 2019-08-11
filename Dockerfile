FROM       centos:latest
#FROM      centos:7.6.1810
#FROM      centos:7.5.1804
#FROM      centos:7.3.1611

RUN yum install epel-release -y
RUN yum update -y
#RUN yum install https://get.pkgs.cloud/release.rpm -y
#RUN yum install pkgs.cloud-updates pkgs.cloud-extras -y
RUN yum install mc wget nano patch yum-utils deltarpm which rpm-build rpmdevtools git -y
RUN yum groupinstall "Development Tools" -y
COPY ./.rpmmacros /root/.rpmmacros
COPY ./.bashrc /root/.bashrc

