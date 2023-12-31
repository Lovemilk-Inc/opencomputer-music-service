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
1. 安装 FFmpeg 和 Python >= 3.10 并配置入环境变量 (若有请跳过)
2. 使用 git 或 GH CLI 克隆当前存储库 main 分支, 在终端中运行如下指令 (以 git 为例): <br>
`git clone https://github.com/zhuhansan666/opencomputer-music-service`
3. 将工作路径切换到克隆的目录, 在默认配置下可以在终端中运行如下指令: <br>
`cd ./opencomputer-music-service`
4. 创建 Python 虚拟环境 (如果有多个 Python 可能需要自行选择相应环境), 一般的可以在终端中运行如下指令: <br>
`python -m venv ./venv`
5. 激活虚拟环境 ~~激活虚拟环境, 转到设置以激活虚拟环境~~ <br>
   1. 在 Windows 上, 可以在终端中运行: `./venv/Scripts/activate`
   2. 在 *nix (Unix 和 Unix-like) 可以在终端中运行: `source ./venv/bin/activate`
6. 安装依赖, 在已激活虚拟环境的终端中运行如下指令: <br>
`pip install -r ./requriuments.txt`
7. 使用 uvicorn 运行服务器, 在已激活虚拟环境并依赖安装成功的终端中运行如下指令: <br>
`uvicorn src.app:app --host=<监听的IP地址, 可以使用 0.0.0.0 监听全部> --port=<服务端口号>` <br>
推荐指令: `uvicorn src.app:app --host=0.0.0.0 --port=20100`
8. 访问 `http://<IP>:<端口>`, 如果你使用推荐指令在当前设备上运行, 您可以直接访问 [此处](http://127.0.0.1:20100)
9. 尽情享受吧!

## 版权声明
[^mc]: Minecraft 是 Mojang Studios 和/或 Microsoft Corporation 旗下的一款沙盒游戏的名称
[^oc]: OpenComputer 是 Minecraft 的一个第三方模组
