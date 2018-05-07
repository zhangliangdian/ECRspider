:: 如果配置过mongod.cfg，则用如下方式运行MongoDB
mongod.exe --config "F:\MongoDB\mongod.cfg" --install
net start MongoDB

:: 如果未配置，用如下命令运行MongoDB；mongod.exe要先添加到path环境变量
:: mongod.exe --dbpath=F:\MongoDB\data\db

python ECRspiderGUI.py

net stop MongoDB

pause
