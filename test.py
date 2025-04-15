import builtins

def print(*args, **kwargs):
    if 'flush' not in kwargs:
        kwargs['flush'] = True
    builtins.print(*args, **kwargs)

print('hi', 'bi', sep='qt')

from urllib.parse import urlparse

def convert_to_proxy_url(original_url: str) -> str:
    parsed = urlparse(original_url)
    host = parsed.hostname  # ex: rr3---sn-xxxxx.googlevideo.com
    print(host)
    path = parsed.path.lstrip('/')
    print(path)
    query = parsed.query
    print(query)
    return f"http://proxy.ll/youtube/{host}/{path}?{query}"

original_url = 'https://rr3---sn-ogul7n7z.googlevideo.com/videoplayback?expire=1744691594&ei=Ko39Z7ecNLeX1d8Px93boQo&ip=89.147.101.6&id=o-ABjyGfZ64Z61-RluhnU0FfN6GqriQoHh3AYiHxfHW_2i&itag=251&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&met=1744669994%2C&mh=j2&mm=31%2C29&mn=sn-ogul7n7z%2Csn-oguelnsy&ms=au%2Crdu&mv=m&mvi=3&pl=24&rms=au%2Cau&pcm2=yes&gcr=kr&initcwndbps=1878750&bui=AccgBcMc7dBt3Z27nqj1sbwAgPFtiiyVcXPflkrQxSSR54ewluCr56AoFBSowtWEc_FAAmxgAzvOgRJj&vprv=1&svpuc=1&mime=audio%2Fwebm&ns=Sv_lnM828GnGtTEWf7TxHp4Q&rqh=1&gir=yes&clen=3541182&dur=213.901&lmt=1714852755473358&mt=1744669519&fvip=5&keepalive=yes&lmw=1&c=TVHTML5&sefc=1&txp=5432434&n=AChk6PWl2zjCtQ&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cpcm2%2Cgcr%2Cbui%2Cvprv%2Csvpuc%2Cmime%2Cns%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=met%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=ACuhMU0wRAIgRGDe_WoAaQvBCHjN1CS8H4U-KcUzXssz6HOurvAoE8MCIDTnuqYiZ1L_AY6rmoFvu2XGxfAPQhYq_yB8YsVxrhj6&sig=AJfQdSswRgIhAN2S6PvPz8sN9SNNfubPJh5SHojL-PbHp6YrGHID89abAiEA39S17C3iGq1DK8i0hWaTQVPIqSVX_fIH3nW8bme30Bo%3D'
url = convert_to_proxy_url(original_url)
print(url)
