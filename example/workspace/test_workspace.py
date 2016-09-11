# -*- coding: utf-8 -*-
# Created by apple on 16/8/29.

import package as package

scheme = 'WorkspacePackageTest'
config_name = 'Release'
path = './WorkspacePackageTest'
path_project = '{}/WorkspacePackageTest.xcodeproj'.format(path)
path_workspace = '{}/WorkspacePackageTest.xcworkspace'.format(path)
path_archive = '{}/test.xcarchive'.format(path)
path_ipa = '{}/test.ipa'.format(path)
path_appstore_ipa = '{}/test_appstore.ipa'.format(path)
path_dsym = '{}/test.DSYM'.format(path)
path_info_plist = '{}/WorkspacePackageTest/Info.plist'.format(path)
path_plist = '../AppStore.plist'
keychain_password = '{password}'

# unlock keychain(填上电脑的keychain密码)
package.keychain_unlock(keychain_password)

# list project or workspace info
for l in package.list_info(path_project):
    print(l)

# clean previous build
for l in package.clean(path_workspace, scheme, False):
    print(l)

# pod install
for l in package.pod_install():
    print(l)

# build code
build_code = package.build_code(path_info_plist)
print('build code: ', build_code)

# version code
version_code = package.version_code(path_info_plist)
print('version code: ', version_code)

# archive the project or workspace
for l in package.package_archive(path_workspace, scheme, config_name, path_archive, False):
    print(l)

# export DSYM
package.export_dsym(path_archive, scheme, path_dsym)

# export .ipa
app_path = package.get_app_path(path_archive, scheme)
for l in package.export_ipa(app_path, path_ipa):
    print(l)

# export AppStore ipa
for l in package.export_appstore_ipa(path_archive, scheme, path_appstore_ipa, path_plist):
    print(l)

# upload AppStore(填上自己的apple developer账号和密码)
for l in package.upload_appstore(path_appstore_ipa, '{account}', '{password}'):
    print(l)
