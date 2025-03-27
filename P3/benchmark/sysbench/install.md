# install dependencies

```bash
sudo apt install make automake libtool pkg-config libaio-dev autoconf libtool-bin libtool
```

# create install environment

```bash
mkdir install
cd install
```

# download and extract sysbench 0.4.12

```bash
wget https://src.fedoraproject.org/repo/pkgs/sysbench/sysbench-0.4.12.tar.gz/3a6d54fdd3fe002328e4458206392b9d/sysbench-0.4.12.tar.gz
tar -xvf sysbench-0.4.12.tar.gz
cd sysbench-0.4.12
```

# update config.guess and config.sub for ./configure to work

```bash
wget -O config/config.guess 'https://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
wget -O config/config.sub 'https://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub'
```

# build from source

```bash
./autogen.sh
autoupdate
./configure --without-mysql
sudo make LIBTOOL=/usr/bin/libtool
sudo make LIBTOOL=/usr/bin/libtool install
```

# copy generated binary to 

```bash
sudo cp sysbench/sysbench /usr/local/bin/
sudo chmod +x /usr/local/bin/sysbench
sysbench --version
```
