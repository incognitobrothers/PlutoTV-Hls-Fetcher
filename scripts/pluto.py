import requests
import pathlib
import xml.etree.ElementTree as ET

region = 'all'

playlist = ['#EXTM3U']

url = 'https://raw.githubusercontent.com/matthuisman/i.mjh.nz/refs/heads/master/PlutoTV/all.xml'

resp = requests.get(url, timeout=30)
resp.raise_for_status()

xml_file = pathlib.Path('pluto_all.xml')
xml_file.write_bytes(resp.content)

root = ET.parse(xml_file).getroot()

for channel in root.findall('channel'):
    chnlid = channel.get('id')

    name = channel.findtext('display-name')

    icon = channel.find('icon')
    ico = icon.get('src', '') if icon is not None else ''

    playlist.append(
        f'#EXTINF:-1 tvg-id="{chnlid}" tvg-name="{name}" tvg-logo="{ico}",{name}'
    )

    playlist.append(f'https://jmp2.uk/plu-{chnlid}.m3u8')

pathlib.Path('pluto.m3u').write_text(
    '\n'.join(playlist) + '\n',
    encoding='utf-8'
)

xml_file.unlink(missing_ok=True)

print('Successfully created pluto.m3u')
