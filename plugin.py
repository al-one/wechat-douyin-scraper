import os
import time
import asyncio
from plugins import register, Plugin, Event, logger, Reply, ReplyType
from .scraper import Scraper

@register
class App(Plugin):
    name = 'douyin_scraper'
    latest_clear = 0

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
        if self.config.get('without_at'):
            self.reply(event)

        self.clear_assets()

    def will_generate_reply(self, event: Event):
        if not self.config.get('without_at'):
            self.reply(event)

    def will_decorate_reply(self, event: Event):
        pass

    def will_send_reply(self, event: Event):
        pass

    def reply(self, event: Event):
        query = event.message.content
        for cmd in self.commands:
            if cmd in query:
                event.reply = self.generate_reply(event)
                event.bypass()
                return

    def generate_reply(self, event: Event) -> Reply:
        query = event.message.content
        result = asyncio.run(self.hybrid_parsing(query)) or {}
        vdata = result.get('video_data') or result
        url = vdata.get('nwm_video_url') or vdata.get('video_url')
        logger.info('Scraper result: %s', url or result)
        if not url:
            if msg := result.get('message'):
                return Reply(ReplyType.TEXT, f'Scraper: {msg}')
            return Reply(ReplyType.TEXT, f'{result}' or '获取视频失败')

        with_link = self.config.get('with_link')
        only_link = self.config.get('only_link')
        if with_link or only_link:
            link = vdata.get('nwm_video_url_HQ') or url
            if with_link not in [True, 1, '1', 'on', 'yes', 'true']:
                if '{link}' not in with_link:
                    with_link = f'{with_link}' + '{link}'
                link = with_link.replace('{link}', link)
                link = link.replace('{desc}', result.get('desc', ''))
            reply = Reply(ReplyType.TEXT, link.strip())
            if only_link:
                return reply
            event.channel.send(reply, event.message)
        return Reply(ReplyType.VIDEO, url)

    async def hybrid_parsing(self, url):
        result = {}
        for n in range(2):
            try:
                return await self.api.hybrid_parsing(url) or {}
            except Exception as exc:
                logger.error('Scraper Exception: %s', exc)
                result = {'message': f'{exc}'}
                await asyncio.sleep(0.1)
        return result

    def clear_assets(self):
        now = time.time()
        if now - self.latest_clear < 300:
            return
        days = self.config.get('keep_assets_days', 0)
        if not days:
            return
        try:
            current_dir = os.path.dirname(os.path.realpath(__file__))
            assets_dir = os.path.dirname(f'{current_dir}/../../assets/.')
            files = os.listdir(assets_dir)
            for file in files:
                path = os.path.join(assets_dir, file)
                if '.gitkeep' in path:
                    continue
                tim = os.path.getmtime(path)
                if time and now - tim > days * 86400:
                    os.remove(path)
                    logger.info('Clear assets file: %s', path)
            self.latest_clear = now
        except Exception as exc:
            logger.warning('Clear assets failed: %s', exc)