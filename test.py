import youtube_dl 

ydl_opts = {'format': 'bestaudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info("https://www.youtube.com/watch?v=kTJczUoc26U", download=False)
    URL = info['formats'][0]['url']
print(info['thumbnails'][0]['url'])

