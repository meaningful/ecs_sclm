# ecs_sclm
the code in my ecs server
这是从我们的ecs服务器上的代码仓库， 团队使用本仓库作为代码管理 ， 请各位按照下面的方式生成自己的ssh密钥， 然后私下发给我添加到本代码仓库中： 

一、生成ssh密钥对

当然上传之前肯定要自己先生成ssh key了，windows的用户可以下载xshell之类的工具来生成，我这边linux就直接输命令了

ssh-keygen -t rsa # 一直回车下去，不输入密码

二、查看公钥

密钥对生成完成后存放于当前用户 ~/.ssh 目录中，查看 id_rsa.pub 

