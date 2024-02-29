## 抖音/TikTok/快手视频去水印

> 本项目作为[`wechat-gptbot`](https://github.com/iuiaoin/wechat-gptbot)插件，可以去除抖音/TikTok/快手等视频的水印。

### 安装

添加以下配置到插件源配置文件`plugins/source.json`:
```yaml
  "douyin_scraper": {
    "repo": "https://github.com/al-one/wechat-douyin-scraper.git",
    "desc": "抖音/TikTok/快手视频去水印"
  }
```

### 配置

添加以下配置到配置文件`config.json`:
```yaml
  "plugins": [
    {
      "name": "douyin_scraper",
      "command": ["复制打开抖音", "v.douyin", "tiktok.com", "kuaishou.com"],
      "with_link": "{desc}\n高清视频链接:\n{link}", # str或bool，为str时作为回复模板
      "only_link": true,     # 仅发送链接，bool或dict
      "without_at": {        # 无需@机器人也会解析，bool或dict
        "wx_userid": true,     # 私聊
        "xxxx@chatroom": true, # 群聊
        "*": false
      },
      "keep_assets_days": 3             # 清理N天前的视频缓存
      "douyin_cookies": "sessionid=xxx" # 抖音网页版登陆后复制所有Cookie
    }
  ]
```

### 鸣谢

- https://github.com/Evil0ctal/Douyin_TikTok_Download_API
