import os,sys

#以root用户登录


#判断当前用户
if os.getuid() != 0:
    print("请以root用户执行脚本")
    sys.exit(1)
#else:
#    cmd = 'sudo su && huawei@123'
#    if os.system(cmd) != 0:
#        print('登录失败！')
#        sys.exit(1)
#获取源码包


#选择版本号
def_ver = '1.15.5'
version = input('请输入要下载的版本号（默认为{}）：'.format(def_ver))
if version == '':
    version = def_ver
print('当前安装的版本号为{}'.format(version))
url = 'http://nginx.org/download/nginx-{}.tar.gz'.format(version)

#选择安装路径
def_path = '/usr/local/nginx'
path = input('请输入要安装的路径（默认为{}：）'.format(def_path))
if path == '':
    path = def_path
print('当前选择的安装路径为{}'.format(path))

#删除同名文件
if os.path.exists('nginx-{}'.format(version)):
    os.system('rm -rf nginx-{}'.format(version))
    #os.remove('nginx-{}'.format(version))

#下载
cmd = 'wget {}'.format(url)
res = os.system(cmd)
if res != 0:
    print('下载失败')
    sys.exit(1)
#解压
cmd = 'tar -zxf nginx-{}.tar.gz'.format(version)
if os.system(cmd) != 0:
    print('解压失败')
    sys.exit(1)

#安装依赖包
cmd = 'apt install -y gcc make libpcre3-dev zlib1g-dev openssl libssl-dev'
if os.system(cmd) != 0:
    print('安装依赖失败！')
    sys.exit(1)

#配置
cmd = 'cd nginx-{} && ./configure --prefix=/usr/local/nginx --with-http_ssl_module'.format(version)
if os.system(cmd) != 0:
    print('配置失败！')
    sys.exit(1)

#编译
cmd = 'cd nginx-{} && make && make install'.format(version)
if os.system(cmd) != 0:
    print('编译失败！')
    sys.exit(1)

print('安装成功！')