import asyncio
import httpx
from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import LogTable


class Command(BaseCommand):
    help = 'django command 에서 async로 httpx 요청 하는 데모 코드 작성 해주세요.'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        url = options['url']

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.exam(url))

    async def exam(self, url):
        """
        어싱크 메서드를 만들고 해당 함수 호출 시 특정 이벤트를 만들면 된다.
        """
        async with httpx.AsyncClient() as client:
            tasks = []
            for index in range(40):
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

        # 요청 응답 결과 출력
        self.stdout.write(f"Request {index}: {response.status_code}")
