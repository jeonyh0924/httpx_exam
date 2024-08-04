import asyncio
import httpx
import os
import logging

from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings

from core.models import LogTable

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'django command 에서 async로 httpx 요청 하는 데모 코드 작성 해주세요.'

    def handle(self, *args, **options):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.crawling())

    async def crawling(self):
        url_list_path = os.path.join(settings.BASE_DIR, 'url_list.txt')
        if not os.path.exists(url_list_path):
            logger.info(f"해당 파일이 존재하지 않습니다. 파일 경로 : {url_list_path}")
            return

        with open(url_list_path, 'r') as file:
            urls = file.readlines()

        async with httpx.AsyncClient() as client:
            tasks = []
            for index, url in enumerate(urls):
                url = url.strip()
                if url:
                    tasks.append(self.fetch_and_log(client, url, index))
            await asyncio.gather(*tasks)

    async def fetch_and_log(self, client, url, index):
        start_time = timezone.now()
        response = await client.get(url)
        end_time = timezone.now()
        duration = end_time - start_time

        await sync_to_async(LogTable.objects.create)(
            url=url,
            status_code=response.status_code,
            duration=duration,
            now=timezone.now(),
            index=index
        )

        # 어싱크 메서드 내 요청 응답 결과 출력 함수
        logger.info(f"URL : {url} : {response.status_code}, index >> {index}")
