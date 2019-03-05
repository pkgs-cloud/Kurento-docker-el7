FROM      centos:7.6.1810
#FROM      centos:7.5.1804

RUN yum install epel-release -y
RUN yum update -y
RUN yum install https://get.pkgs.cloud/release.rpm -y
RUN yum install pkgs.cloud-updates pkgs.cloud-extras -y
RUN yum install mc wget nano patch yum-utils which aspell-en -y
RUN yum groupinstall "Development Tools" -y
COPY ./.rpmmacros /root/.rpmmacros
COPY ./.bashrc /root/.bashrc

