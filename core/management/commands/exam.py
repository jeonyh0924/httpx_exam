import asyncio
import httpx
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'django command 에서 async로 httpx 요청 하는 데모 코드 작성 해주세요.'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        url = options['url']

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.exam(url))

    async def exam(self, url):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            print(f"비동기 요청 응답 값 : {response.status_code}")
