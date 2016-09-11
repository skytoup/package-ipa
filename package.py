# -*- coding: utf-8 -*-
# Created by apple on 16/8/29.
import sh
import random
import plistlib
from os.path import expanduser, join, realpath

__path_cwd = realpath('.')
__default_path_keychain = '~/Library/Keychains/login.keychain'
__default_path_xcode = '/Applications/Xcode.app'
__default_path_altool = 'Contents/Applications/Application Loader.app/Contents/Frameworks/ITunesSoftwareService.' \
                        'framework/Versions/A/Support/altool'

__cmd_security = sh.security
__cmd_xcodebuild = sh.xcodebuild
__cmd_xcrun = sh.xcrun
__cmd_cp = sh.cp
__cmd_mv = sh.mv
__cmd_rm = sh.rm
__cmd_altool = sh.Command('{}/{}'.format(__default_path_xcode, __default_path_altool))
__cmd_pod = sh.pod


def option_project_or_workspace(is_project):
    return '-project' if is_project else '-workspace'


def pod_repo_update():
    return __cmd_pod('repo', 'update')


def pod_install():
    return __cmd_pod('install', '--no-repo-update')


def keychain_unlock(password='', path=__default_path_keychain):
    """
    解锁keychain
    :param password: login user 的密码
    :param path: login.keychain的路径, 默认为 ~/Library/Keychains/login.keychain
    :return: sh.Command
    """
    assert password is not None  # password 不为空
    return __cmd_security('unlock-keychain', '-p', "'{}'".format(password), expanduser(path))


def list_info(path, is_project=True):
    """
    列出project or workspace信息
    :param path: project or workspace 的路径
    :param is_project: 是否为project(项目可能是project or workspace)
    :return: sh.Command
    """
    option = option_project_or_workspace(is_project)
    return __cmd_xcodebuild('-list', option, path)


def clean(path, scheme, is_project=True):
    """
    清除package时build产生的文件
    :param path: project or workspace 的路径
    :param scheme: project 的 scheme
    :param is_project: 是否为project(项目可能是project or workspace)
    :return: sh.Command
    """
    option = option_project_or_workspace(is_project)
    return __cmd_xcodebuild('clean', option, path, '-scheme', scheme)


def __get_plist_values(info_plist_path, key):
    """
    读取Plist的value
    :param info_plist_path: Info.plist 的路径
    :param key: 需要获取的key
    :return: key对应的value
    """
    with open(info_plist_path, 'rb') as fp:
        plist = plistlib.load(fp)
        return plist.get(key)


def version_code(info_plist_path):
    """
    读取info plist的version
    :param info_plist_path: Info.plist 的路径
    :return: version code
    """
    return __get_plist_values(info_plist_path, 'CFBundleVersion')


def build_code(info_plist_path):
    """
        读取info plist的build
        :param info_plist_path: Info.plist 的路径
        :return: build code
    """
    return __get_plist_values(info_plist_path, 'CFBundleShortVersionString')


def package_archive(path, scheme, configuration_name, archive_path, is_project=True):
    """
    打包iOS项目成.xcarchive
    :param path: project or workspace 的路径
    :param scheme: project 的 scheme
    :param configuration_name: Release, Debug or othen custom config_name
    :param archive_path: 生成的.xcarchive路径
    :param is_project: 是否为project(项目可能是project or workspace)
    :return: sh.Command
    """
    option = option_project_or_workspace(is_project)
    return __cmd_xcodebuild(option, path, '-scheme', scheme, '-destination', 'generic/platform=iOS', 'archive',
                            '-configuration',
                            configuration_name, 'ONLY_ACTIVE_ARCH=NO', '-archivePath', archive_path)


def get_app_path(archive_path, scheme):
    """
    获取.app的路径
    :param archive_path: .xcarchive 的路径
    :param scheme: project 的 scheme
    :return: sh.Command
    """
    return join(archive_path, 'Products/Applications/{}.app'.format(scheme))


def export_dsym(archive_path, scheme, export_path):
    """
    导出DSYM
    :param archive_path: .xcworkspace 的路径
    :param scheme: project 的 scheme
    :param export_path: 导出的路径
    :return: sh.Command
    """
    dsym_path = join(archive_path, 'DSYMs', '{}.app.DSYM'.format(scheme))
    return __cmd_cp('-r', dsym_path, export_path)


def export_ipa(app_path, ipa_path):
    """
    导出ipa
    :param app_path: .app 路径
    :param ipa_path: 导出的 .ipa 路径
    :return: sh.Command
    """
    export_path = realpath(ipa_path) if ipa_path.find('~') == -1 else expanduser(ipa_path)
    return __cmd_xcrun('-sdk', 'iphoneos', 'PackageApplication', '-v', app_path, '-o', export_path)


def export_appstore_ipa(archive_path, scheme, ipa_path, plist_path):
    """
    导出上传AppStore的ipa
    :param archive_path: .xcworkspace 的路径
    :param scheme: project 的 scheme
    :param ipa_path: 导出的 .ipa 路径
    :param plist_path: .plist 的路径
    :return: sh.Command
    """
    tmp_path = 'tmp_{}'.format(random.randint(100000000, 1000000000))
    tmp_file = '{}/{}.ipa'.format(tmp_path, scheme)
    cmd = __cmd_xcodebuild('-exportArchive', '-archivePath', archive_path, '-exportPath', tmp_path,
                           '-exportOptionsPlist', plist_path)
    if not cmd.exit_code:
        __cmd_mv(tmp_file, ipa_path)
    __cmd_rm('-rf', tmp_path)
    return cmd


def upload_appstore(appstore_ipa_path, developer_account, developer_password, xcode_path=None):
    """
    上传到AppStore
    :param appstore_ipa_path: .ipa 的路径
    :param developer_account: 开发者账号
    :param developer_password: 开发者账号的密码
    :param xcode_path: Xcode的路径
    :return: sh.Command
    """
    if xcode_path:
        altool = sh.Command('{}{}' if xcode_path[-1] == '/' else '{}/{}').format(xcode_path, __default_path_altool)
    else:
        altool = __cmd_altool
    return altool('--upload-app', '-f', appstore_ipa_path, '-u', developer_account, '-p', developer_password, '-t',
                  'ios', '--output', 'xml')
