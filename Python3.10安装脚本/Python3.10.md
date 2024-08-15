~~~bash
yum -y install libffi-devel zlib-devel bzip2-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc 
cd
wget http://www.openssl.org/source/openssl-1.1.1.tar.gz 
tar -zxvf openssl-1.1.1.tar.gz 
cd openssl-1.1.1
./config --prefix=/usr/local/openssl shared zlib && make && make install
echo "/usr/local/openssl/lib" > /etc/ld.so.conf.d/openssl.conf
mv /usr/bin/openssl /usr/bin/openssl.old
ln -s /usr/local/openssl/bin/openssl /usr/bin/openssl
echo "export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:/usr/local/openssl/lib" >>  /etc/profile 

cd
wget https://www.python.org/ftp/python/3.10.11/Python-3.10.11.tgz
mkdir -p /usr/local/python3.10
tar -zxvf Python-3.10.11.tgz
cd Python-3.10.11
./configure --prefix=/usr/local/python3.10 --with-openssl=/usr/local/openssl && make && make install
echo "export PATH=/usr/local/python3.10/bin:\$PATH" >>  /etc/profile 
source /etc/profile

mkdir ~/.pip
# 创建 pip 地址目录
 
touch ~/.pip/pip.conf
# 创建配置文件
cat > ~/.pip/pip.conf <<q
[global]
trusted-host =  mirrors.aliyun.com
index-url = http://mirrors.aliyun.com/pypi/simple
q
~~~

