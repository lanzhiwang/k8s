# -*- coding: utf-8 -*-

import os
import collections
import platform
import psutil
import delegator
import string
import pwd
import stat
import iptc

# Linux 用户属性
linuxUser = collections.namedtuple('linuxUser', ['name', 'password', 'uid', 'gid', 'group', 'home', 'shell'])


def getAllFile(path):
    """ 递归获取某路径下的所有文件

    Args:
        path:

    Returns:
        generator
    """
    # if path == None:
    #     return None
    for root, dirs, files in os.walk(path):
        for file in files:
            # 有个bug，系统分隔符无法打印，暂时 hardcode
            yield '{}/{}'.format(root, file)


def getBaseInfo():
    """ 获取系统基本信息

    Args:

    Returns:
        dict
    """
    base_info = {}
    # 获取操作系统及版本信息
    base_info['platform'] = platform.platform()
    # 获取系统版本号
    base_info['version'] = platform.version()
    # 获取系统名称
    base_info['system'] = platform.system()
    # 系统位数(例如：32Bit, 64bit)
    base_info['architecture'] = platform.architecture()
    # 计算机类型，例如：x86, AMD64
    base_info['machine'] = platform.machine()
    # 计算机名称
    base_info['node'] = platform.node()
    # 处理器类型
    base_info['processor'] = platform.processor()
    # 系统发行版
    base_info['linux_distribution'] = platform.linux_distribution()
    # 以上所有信息
    base_info['uname'] = platform.uname()

    return base_info


def getProcessesInfo():
    """ 获取系统的所有进程信息

    Args:

    Returns:
        generator
    """
    pids = psutil.pids()
    # print pids
    for pid in pids:
        processes = {}
        try:
            p = psutil.Process(pid)
            processes['name'] = p.name()  # 进程名称
            processes['exe'] = p.exe()  # 进程exe路径
            processes['cwd'] = p.cwd()  # 进程工作目录
            processes['cmdline'] = p.cmdline()  # 进程启动的命令行
            processes['ppid'] = p.ppid()  # 父进程ID
            processes['parent'] = p.parent()  # 父进程
            processes['children'] = p.children()  # 子进程列表
            processes['status'] = p.status()  # 进程状态
            processes['username'] = p.username()  # 进程用户名
            processes['create_time'] = p.create_time()  # 进程创建时间
            processes['terminal'] = p.terminal()  # 进程终端
            processes['cpu_times'] = p.cpu_times()  # 进程使用的CPU时间
            processes['memory_info'] = p.memory_info()  # 进程使用的内存
            processes['open_files'] = p.open_files()  # 进程打开的文件
            processes['connections'] = p.connections()  # 进程相关网络连接
            processes['num_threads'] = p.num_threads()  # 进程的线程数量
            processes['threads'] = p.threads()  # 所有线程信息
            processes['environ'] = p.environ()  # 进程环境变量

            yield processes
        except psutil.NoSuchProcess as e:
            pass


def getAllModule():
    """ 获取所有加载的模块

    Args:

    Returns:
        list
    """
    result = []
    c = delegator.run('lsmod')
    module_list = c.out.split(os.linesep)
    module_list = module_list[1:len(module_list)-1]
    for temp in module_list:
        module = temp[0:temp.index(' ')].strip()
        result.append(module)
    return result


def getModuleInfo(module_name):
    """ 获取某一模块的信息

    Args:
        module_name: 模块名

    Returns:
        generator
    """
    result = {}
    if module_name is None:
        return None
    c = delegator.run('modinfo ' + module_name)
    if c.err == 1:
        return None
    else:
        mode_info_list = c.out.split(os.linesep)
        mode_info_list = mode_info_list[0:len(mode_info_list)-1]
        for mod_info in mode_info_list:
            key, value = map(string.strip, mod_info.split(':', 1))
            result[key] = value.strip()

        return result


def getIptablesInfo():
    """ 获取iptable信息

    Args:

    Returns:
        dict
    """
    return {
        'nat': iptc.easy.dump_table('nat', ipv6=False),
        'filter': iptc.easy.dump_table('filter', ipv6=False),
        'raw': iptc.easy.dump_table('raw', ipv6=False),
        'mangle': iptc.easy.dump_table('mangle', ipv6=False),
        'security': iptc.easy.dump_table('security', ipv6=False)
    }


def getNetworkInterface():
    """ 获取网络接口信息

    Args:

    Returns:
        dict
    """
    return psutil.net_if_addrs() #


def getNetwordLink():
    """ 获取系统的所有网络连接信息

    Args:

    Returns:
        generator
    """
    for network_link in psutil.net_connections():
        yield network_link


def getPortList():
    """ 获取系统的所有被占用的端口

    Args:

    Returns:
        list
    """
    ports = []
    for network_link in getNetwordLink():
        ports.append(network_link.laddr.port)
    return ports


def getCPUInfo():
    """ 获取 CPU 信息

    Args:

    Returns:
        dict
    """
    return {'logical': psutil.cpu_count(), 'physical': psutil.cpu_count(logical=False)}


def getMemoryInfo():
    """ 获取 memory 信息

    Args:

    Returns:
        dict
    """
    return {'virtual_memory': psutil.virtual_memory(), 'swap_memory': psutil.swap_memory()}


def getDiskInfo():
    """ 获取 disk 信息

    Args:

    Returns:
        dict
    """
    disk_usage = {}
    disk_partitions = psutil.disk_partitions()
    for disk in disk_partitions:
        disk_usage[disk.mountpoint] = psutil.disk_usage(disk.mountpoint)
    disk_io_counters = psutil.disk_io_counters()

    return {'disk_partitions': disk_partitions, 'disk_usage': disk_usage, 'disk_io_counters': disk_io_counters}


def getLoginUserInfo():
    """ 获取系统登录用户信息

    Args:

    Returns:
        list
    """
    return psutil.users()


def getAllUserInfo():
    """ 获取系统的所有用户信息

    Args:

    Returns:
        list
    """
    all_user = []
    c = delegator.run('cat /etc/passwd')
    users = c.out.split(os.linesep)
    for u in users:
        user_l = u.split(':')
        if len(user_l) == 7:
            user = linuxUser._make(user_l)
            all_user.append(user)
    return all_user


def getENV(name=None):
    """ 获取系统的所有环境变量或者某个环境变量

    Args:
        name: 环境变量名称

    Returns:
        返回类型需要一致
    """
    result = None
    if name:
        result = os.getenv(name)
    else:
        result = os.environ
    return result


def getCommandlist(path='PATH'):
    """ 获取某个路径下的所有可执行文件

    Args:
        path: 路径

    Returns:
        generator
    """
    path_s = getENV(path)  # /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin
    path_l = path_s.split(':')
    for path in path_l:
        for file in getAllFile(path):
            if os.access(file, os.X_OK):
                yield file


def getUserInfo(user):
    """ 获取某一用户具体信息

    Args:

    Returns:
        dict
    """
    try:
        # 后面需要修改为自定义结构
        # 是否需要判断用户存在还需要斟酌
        user_info = pwd.getpwnam(user)  # pwd.struct_passwd(pw_name='root', pw_passwd='x', pw_uid=0, pw_gid=0, pw_gecos='root', pw_dir='/root', pw_shell='/bin/bash')
        return user_info
    except KeyError as e:
        return None

def getPathStat(path):
    """ 获取文件或者目录的权限信息

    Args:

    Returns:
        dict
    """
    try:
        # 后面需要修改为自定义结构
        # 是否需要判断路径存在也需要斟酌
        s = os.stat(path)  # posix.stat_result(st_mode=33188, st_ino=137124253, st_dev=64768L, st_nlink=1, st_uid=0, st_gid=0, st_size=7729, st_atime=1562409473, st_mtime=1562409467, st_ctime=1562409467)
        return s
    except OSError as e:
        return None


def is_readable(path, user):
    """ 判断用户对文件或者目录是否可读

    Args:

    Returns:
        bool
    """
    uid = gid = mode = None
    user_info = getUserInfo(user)
    if user_info is not None:
        uid = user_info.pw_uid
        gid = user_info.pw_gid
    s = getPathStat(path)
    if s is not None:
        mode = s[stat.ST_MODE]  # 自定义结构后需要修改
    if (uid is None) or (gid is None) or (s is None):
        return False
    else:
        return (
            ((s[stat.ST_UID] == uid) and (mode & stat.S_IRUSR > 0)) or
            ((s[stat.ST_GID] == gid) and (mode & stat.S_IRGRP > 0)) or
            (mode & stat.S_IROTH > 0)
        )


def is_writable(path, user):
    """ 判断用户对文件或者目录是否可写

    Args:

    Returns:
        bool
    """
    uid = gid = mode = None
    user_info = getUserInfo(user)
    if user_info is not None:
        uid = user_info.pw_uid
        gid = user_info.pw_gid
    s = getPathStat(path)
    if s is not None:
        mode = s[stat.ST_MODE]  # 自定义结构后需要修改
    if (uid is None) or (gid is None) or (s is None):
        return False
    else:
        return (
            ((s[stat.ST_UID] == uid) and (mode & stat.S_IWUSR > 0)) or
            ((s[stat.ST_GID] == gid) and (mode & stat.S_IWGRP > 0)) or
            (mode & stat.S_IWOTH > 0)
        )


def is_executable(path, user):
    """ 判断用户对文件是否执行

    Args:

    Returns:
        bool
    """
    uid = gid = mode = None
    user_info = getUserInfo(user)
    if user_info is not None:
        uid = user_info.pw_uid
        gid = user_info.pw_gid
    s = getPathStat(path)
    if s is not None:
        mode = s[stat.ST_MODE]  # 自定义结构后需要修改
    if (uid is None) or (gid is None) or (s is None):
        return False
    else:
        return (
            ((s[stat.ST_UID] == uid) and (mode & stat.S_IXUSR > 0)) or
            ((s[stat.ST_GID] == gid) and (mode & stat.S_IXGRP > 0)) or
            (mode & stat.S_IXOTH > 0)
        )


"""
def getPackageTool():
    package_tool = (None, None)
    # 初步判断系统自带的包管理工具
    linux_distribution = getBaseInfo()['linux_distribution']  # ('CentOS Linux', '7.5.1804', 'Core')
    if 'centos' in linux_distribution[0].lower():
        for command in getCommandlist():
            # package_tool[0] = lambda 'rpm' in command if command else None
            # package_tool[1] = lambda 'yum' in command if command else None
            if 'rpm' in command:
                package_tool[0] = command
            if 'yum' in command:
                package_tool[1] = command
    if 'ubuntu' in linux_distribution[0].lower():
        for command in getCommandlist():
            # package_tool[0] = lambda 'dpkg' in command if command else None
            # package_tool[1] = lambda 'apt' in command if command else None
            if 'dpkg' in command:
                package_tool[0] = command
            if 'apt' in command:
                package_tool[1] = command
"""


def getPackageTool():
    """ 获取系统的包管理工具

    Args:

    Returns:
        list
    """
    package_tool = [None, None]
    # 初步判断系统自带的包管理工具
    for command in getCommandlist():
        if command.endswith('rpm'):
            package_tool[0] = command
        if command.endswith('yum'):
            package_tool[1] = command

        if command.endswith('dpkg'):
            package_tool[0] = command
        if command.endswith('apt'):
            package_tool[1] = command
    return package_tool


def getSoftwareByPackageOnCentos():
    pass


def getSoftwareByPackageOnUbuntu():
    pass


def getSoftwareByPackage(software=None):
    """ 获取系统已经安装的软件列表

    Args:

    Returns:
        list
    """
    c = None
    result = []
    package_tool = getPackageTool()
    linux_distribution = getBaseInfo()['linux_distribution']  # ('CentOS Linux', '7.5.1804', 'Core')
    if 'centos' in linux_distribution[0].lower():
        if package_tool[0] is not None:
            if software is not None:
                c = delegator.run(package_tool[0] + ' -qa').pipe('grep -v grep').pipe('grep ' + software)
            else:
                c = delegator.run(package_tool[0] + ' -qa')

    if 'ubuntu' in linux_distribution[0].lower():
        if package_tool[0] is not None:
            if software is not None:
                c = delegator.run(package_tool[0] + ' -L').pipe('grep -v grep').pipe('grep ' + software)
            else:
                c = delegator.run(package_tool[0] + ' -L')
    if c is not None and c.out is not None:
        result = c.out.split(os.linesep)
    return result


def getSoftwareinfo(software):
    """ 获取某种软件的具体信息

    Args:

    Returns:
        dict
    """
    if software is None:
        return None
    c = None
    result = {}
    package_tool = getPackageTool()
    linux_distribution = getBaseInfo()['linux_distribution']  # ('CentOS Linux', '7.5.1804', 'Core')
    soft_list = getSoftwareByPackage(software)
    # print soft_list
    if len(soft_list):
        for soft in soft_list:
            if 'centos' in linux_distribution[0].lower():
                if package_tool[0] is not None:
                    c = delegator.run(package_tool[0] + ' -qi ' + soft)
                    print c.out

            if 'ubuntu' in linux_distribution[0].lower():
                if package_tool[0] is not None:
                    c = delegator.run(package_tool[0] + ' -l')

            if c is not None and c.out is not None:
                result[soft] = c.out

    return result



if __name__ == '__main__':
    print '------------ 获取系统基本信息 ------------'
    print getBaseInfo()
    print '\n\n'

    print '------------ 获取系统的所有进程信息 ------------'
    for processes in getProcessesInfo():
        print processes
    print '\n\n'

    print '------------ 获取所有加载的模块 ------------'
    print getAllModule()
    print '\n\n'

    print '------------ 获取某一模块的信息(以 veth 模块为例) ------------'
    print getModuleInfo('veth')
    print '\n\n'

    print '------------ 获取 iptable 信息 ------------'
    print getIptablesInfo()
    print '\n\n'

    print '------------ 获取网络接口信息 ------------'
    print getNetworkInterface()
    print '\n\n'

    print '------------ 获取系统的所有网络连接信息 ------------'
    for link in getNetwordLink():
        print link
    print '\n\n'

    print '------------ 获取系统的所有被占用的端口 ------------'
    print getPortList()
    print '\n\n'

    print '------------ 获取 CPU 信息 ------------'
    print getCPUInfo()
    print '\n\n'

    print '------------ 获取 memory 信息 ------------'
    print getMemoryInfo()
    print '\n\n'

    print '------------ 获取 disk 信息 ------------'
    print getDiskInfo()
    print '\n\n'

    print '------------ 获取系统登录用户信息 ------------'
    print getLoginUserInfo()
    print '\n\n'

    print '------------ 获取系统的所有用户信息 ------------'
    print getAllUserInfo()
    print '\n\n'

    print '------------ 获取某一用户具体信息 ------------'
    print getUserInfo('root')
    print '\n\n'

    print '------------ 获取系统的所有环境变量或者某个环境变量 ------------'
    print getENV()
    print '\n\n'

    print '------------ 获取某个路径下的所有可执行文件 ------------'
    for command in getCommandlist('PATH'):
        print command
    print '\n\n'

    print '------------ 获取文件或者目录的权限信息 ------------'
    print getPathStat('/root/work/mysql')
    print '\n\n'

    print '------------ 判断用户对文件或者目录是否可读 ------------'
    print is_readable('/root/work/mysql', 'root')
    print '\n\n'

    print '------------ 判断用户对文件或者目录是否可写 ------------'
    print is_writable('/root/work/mysql', 'root')
    print '\n\n'

    print '------------ 判断用户对文件是否执行 ------------'
    print is_executable('/usr/bin/yum', 'root')
    print '\n\n'

    print '------------ 获取系统的包管理工具 ------------'
    print getPackageTool()
    print '\n\n'

    print '------------ 获取系统已经安装的软件列表 ------------'
    print getSoftwareByPackage()
    print '\n\n'

    print '------------ 获取某种软件的具体信息 ------------'
    print getSoftwareinfo('vim')
    print '\n\n'
