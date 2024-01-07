# opencomputer[^oc]-music-service
> 用于将普通含有音轨的文件 (包括但不限于音频 视频) 转化为 Minecraft 模组 OpenComputer 的 DFPWM 波形文件

## 使用方法 (1, 推荐)
1. [手动部署服务器](#部署方法)
2. 后访问服务器链接, 选择并上传支持的文件
3. 等待服务端转换完成
4. 选择下载 或 复制链接 (以粘入 Minecraft[^mc])
> 注意: 本服务器依赖 FFmpeg, 您需要在启动服务器前将 FFmpeg 可执行文件加入环境变量

## 使用方法 (2, 不推荐)
访问官方样例站点 (任选可访问的其一):
1. <http://dfpwm.lovemilk.top:20100>
2. <https://dfpwm.lovemilk.top:2053>

> 官方样例站点仅供测试和预览, 不对可用性保证, 切勿在生产环境使用示例站点 API, 否所造成的一切后果由使用者/团体承担

## 部署方法
1. 安装 FFmpeg 和 Python >= 3.10 并配置入环境变量 (若有请跳过)
2. 使用 git 或 GH CLI 克隆当前存储库 main 分支, 在终端中运行如下指令 (以 git 为例):
   ```sh
   git clone https://github.com/Lovemilk-Inc/opencomputer-music-service.git
   ```
3. 将工作路径切换到克隆的目录, 在默认配置下可以在终端中运行如下指令:
   ```sh
   cd ./opencomputer-music-service
   ```
4. 创建 Python 虚拟环境 (如果有多个 Python 可能需要自行选择相应环境), 一般地可以在终端中运行如下指令: <br>
   ```sh
   python -m venv ./venv
   ```
5. 激活虚拟环境 ~~激活虚拟环境, 转到设置以激活虚拟环境~~
   1. 在 Windows 上, 可以在终端中运行:
      ```sh
      ./venv/Scripts/activate
      ```
      > 如果您的 Powershell 提示无法运行 PS1 脚本, 请参阅 [此处](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_scripts?view=powershell-7.4#how-to-run-a-script)
      以解决, 并重新运行上述脚本
   2. 在 *nix (Unix 和 Unix-like) 可以在终端中运行: 
      ```sh
      source ./venv/bin/activate
      ```
   
6. 安装依赖, 在已激活虚拟环境的终端中运行如下指令:
   ```sh
   pip install -r ./requriuments.txt
   ```
7. 使用 uvicorn 运行服务器, 在已激活虚拟环境并依赖安装成功的终端中运行如下指令:
   ```sh
   uvicorn src.app:app --host=<监听的IP地址, 可以使用 0.0.0.0 监听全部> --port=<服务端口号>
   ```
   推荐指令: 
    ```sh
    uvicorn src.app:app --host=0.0.0.0 --port=20100
    ```
8. 访问 `http://<IP>:<端口>`, 如果你使用推荐指令在当前设备上运行, 您可以直接访问 [此处](http://127.0.0.1:20100)
9. 尽情享受吧!

## 版权声明
[^mc]: Minecraft 是 Mojang Studios 和/或 Microsoft Corporation 旗下的一款沙盒游戏的名称
[^oc]: OpenComputer 是 Minecraft[^mc] 的一个第三方模组
