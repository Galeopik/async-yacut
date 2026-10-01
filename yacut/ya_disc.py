import asyncio
import urllib

import aiohttp

from settings import Config

AUTH_HEADERS = {
    'Authorization': f'OAuth {Config.DISK_TOKEN}'
}
REQUEST_UPLOAD_URL = f'{Config.YANDEX_DISK_API_URL}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{Config.YANDEX_DISK_API_URL}/disk/resources/download'


async def async_upload_files_to_ya_disc(files):
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            *[
                asyncio.ensure_future(upload_file_and_get_url(session, file))
                for file in files
            ]
        )


async def upload_file_and_get_url(session, file):
    payload = {
        'path': f'app:/{file.filename}',
        'overwrite': 'True'
    }
    async with session.get(
        headers=AUTH_HEADERS,
        params=payload,
        url=REQUEST_UPLOAD_URL
    ) as response:
        data = await response.json()
        url = data['href']
    async with session.put(
        data=file.read(),
        url=url,
    ) as response:
        location = urllib.parse.unquote(response.headers['Location'])
        location = location.replace('/disk', '')
    async with session.get(
        headers=AUTH_HEADERS,
        url=DOWNLOAD_LINK_URL,
        params={'path': f'{location}'}
    ) as response:
        data = await response.json()
        link = data['href']
    return link
