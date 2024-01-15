import asyncio
from plugins import register, Plugin, Event, logger, Reply, ReplyType
from douyin_tiktok_scraper.scraper import Scraper

@register
class App(Plugin):
    name = 'douyin_scraper'

    def __init__(self, config: dict):
        super().__init__(config)
        self.api = Scraper()

    def help(self, **kwargs):
        return '抖音/TikTok/快手视频去水印'

    @property
    def commands(self):
        cmds = self.config.get('command', '去水印')
        if not isinstance(cmds, list):
            cmds = [cmds]
        return cmds

    def did_receive_message(self, event: Event):
        pass

    def will_generate_reply(self, event: Event):
        query = event.context.query
        for cmd in self.commands:
            if cmd in query:
                event.reply = self.reply(event)
                event.bypass()
                return

    def will_decorate_reply(self, event: Event):
        pass

    def will_send_reply(self, event: Event):
        pass

    def reply(self, event: Event) -> Reply:
        query = event.context.query
        result = asyncio.run(self.api.hybrid_parsing(query)) or {}
        logger.info('Scraper: %s', [query, result])
        vdata = result.get('video_data') or {}
        url = vdata.get('nwm_video_url_HQ') or vdata.get('nwm_video_url')
        if url:
            return Reply(ReplyType.VIDEO, url)
        if msg := result.get('message'):
            return Reply(ReplyType.TEXT, msg)
        return Reply(ReplyType.TEXT, f'{result}' or '获取失败')
