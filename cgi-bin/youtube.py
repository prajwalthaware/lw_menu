#!/usr/bin/env python3
import cgi
import youtube_dl

def download_video(url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_url = info_dict.get("url", None)
        return video_url

def main():
    print("Content-Type: text/html\n")
    
    form = cgi.FieldStorage()
    if "url" in form:
        video_url = form["url"].value.strip()
        if video_url:
            try:
                direct_url = download_video(video_url)
                if direct_url:
                    # Print valid headers for redirection
                    print(f"Location: {direct_url}\n")
                    print("Status: 302 Found\n")
                    print(f'<html><body>Redirecting to <a href="{direct_url}">{direct_url}</a></body></html>')
                else:
                    print('<p>Failed to fetch video URL. Please check the link and try again.</p>')
            except Exception as e:
                print(f'<p>Error: {str(e)}</p>')
        else:
            print('<p>Please provide a valid YouTube video URL.</p>')

if __name__ == "__main__":
    main()

