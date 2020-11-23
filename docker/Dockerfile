FROM       centos:7

RUN yum install epel-release -y
RUN yum update -y
RUN yum install mc wget nano patch yum-utils deltarpm which rpm-build rpmdevtools git -y
RUN yum groupinstall "Development Tools" -y
COPY ./.rpmmacros /root/.rpmmacros
COPY ./.bashrc /root/.bashrc
