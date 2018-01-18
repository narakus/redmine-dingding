# redmine-dingding

通过redmine的webhook插件，将消息发送至钉钉中

redmine webhook安装：https://github.com/suer/redmine_webhook


需要修改几个参数，corpid，corpsecret，是从钉钉企业管理员那里可以得到，agentid是自建应用id

服务启动：nohup python robot.py runserver -h 0.0.0.0 -p 3333 > work.log 2>&1 &



