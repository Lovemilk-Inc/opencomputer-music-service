# opencomputer[^oc]-music-service
> 用于将普通含有音轨的文件 (包括但不限于音频 视频) 转化为 Minecraft 模组 OpenComputer 的 DFPWM 波形文件

## 使用方法 (1, 推荐)
1. [手动部署服务器](#部署方法)
2. 后访问服务器链接, 选择并上传支持的文件
3. 等待服务端转换完成
4. 选择下载 或 复制链接 (以粘入 Minecraft[^mc])
> 注意: 本服务器依赖 FFmpeg, 您需要在启动服务器前将 FFmpeg 可执行文件加入环境变量

## 使用方法 (2)
访问官方样例站点: <http://dfpwm.lovemilk.top:20100>
> 官方样例站点仅供测试和预览, 不对可用性保证, 切勿在生产环境使用示例站点 API

## 部署方法
1. 安装 FFmpeg 并配置入环境变量 (若有请跳过)
2. `clone` 后使用 uvicorn 运行 `src.app:app`
3. 尽情享受吧!

## 版权声明
[^mc]: Minecraft 是 Mojang Studios 和/或 Microsoft Corporation 旗下的一款沙盒游戏的名称
[^oc]: OpenComputer 是 Minecraft 的一个第三方模组
