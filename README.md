# PackageIPA(打包IPA)
使用python脚本, 轻松定制自动化iOS项目打包IPA, 还可以上传到appstore😁。

# 主要功能
1. ✔︎打包项目(.xcodeproj, .xcworkspace), 生成.xcarchive
2. ✔︎生成.ipa
3. ✔︎导出.DSYM
4. ✔︎上传ipa到appstore

# 运行环境
MacOS python3(python2没有试过)

# 依赖库
sh: <https://github.com/amoffat/sh>

	pip install sh

# 使用
请参考example

# 注意事项
1. 打包时使用不同的证书说明(证书请在项目里面进行设置):

		①使用发布证书打包, 可以上传到appstore, 用于TestFlight和发布
		②使用开发证书打包, 可以上传到蒲公英、fir等网站进行内测, 也可以上传到appstore
		
2. 需要先把apple打包需要的各种证书安装到keychain

# 相关文章
- [iOS自动化打包上传的踩坑记​](http://skytoup.wicp.net/2016/05/31/iOS%E8%87%AA%E5%8A%A8%E5%8C%96%E6%89%93%E5%8C%85%E4%B8%8A%E4%BC%A0%E7%9A%84%E8%B8%A9%E5%9D%91%E8%AE%B0/)

## 联系方式
* QQ：875766917，请备注
* Mail：875766917@qq.com

# 开源协议: [Apach2.0](LICENSE)