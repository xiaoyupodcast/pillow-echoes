import os
import datetime
from xml.sax.saxutils import escape

BASE_URL = os.getenv("RSS_FEED_BASE_URL")
TITLE = os.getenv("PODCAST_TITLE")
DESCRIPTION = os.getenv("PODCAST_DESCRIPTION")
AUTHOR = os.getenv("PODCAST_AUTHOR")
EMAIL = os.getenv("PODCAST_EMAIL") 
COVER_IMAGE = f"{BASE_URL}/images/cover.jpg"
CATEGORY = os.getenv("PODCAST_CATEGORY")
SUBCATEGORY = os.getenv("PODCAST_SUBCATEGORY")

def generate_rss():
    audio_dir = "audio"
    files = [f for f in os.listdir(audio_dir) if f.endswith(".mp3")]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(audio_dir, x)), reverse=True)

    items_xml = ""
    
    for filename in files:
        file_path = os.path.join(audio_dir, filename)
        file_size = os.path.getsize(file_path)
        # use last modified datetime as published datetime
        mtime = os.path.getmtime(file_path)
        pub_date = datetime.datetime.fromtimestamp(mtime).strftime("%a, %d %b %Y %H:%M:%S +0800")
        
        # "ep1.mp3" -> "ep1"
        clean_title = os.path.splitext(filename)[0]
        audio_url = f"{BASE_URL}/audio/{filename}"
        
        # XML block every episode
        items_xml += f"""
        <item>
            <title>{escape(clean_title)}</title>
            <description>{escape(clean_title)}</description>
            <pubDate>{pub_date}</pubDate>
            <enclosure url="{audio_url}" length="{file_size}" type="audio/mpeg"/>
            <guid isPermaLink="false">{filename}</guid>
            <itunes:author>{AUTHOR}</itunes:author>
            <itunes:image href="{COVER_IMAGE}"/>
        </item>"""

    rss_xml = f"""
                <?xml version="1.0" encoding="UTF-8"?>
                <rss version="2.0" xmlns:itunes="www.itunes.com" xmlns:spotify="www.spotify.com" xmlns:podcast="podcastindex.org">
                    <channel>
                        <title>{escape(TITLE)}</title>
                        <link>{BASE_URL}</link>
                        <language>zh-cn</language>
                        <copyright>Copyright 2025 {AUTHOR}</copyright>
                        <itunes:author>{AUTHOR}</itunes:author>
                        <description>{escape(DESCRIPTION)}</description>
                        <itunes:type>episodic</itunes:type>
                        <itunes:owner>
                            <itunes:name>{AUTHOR}</itunes:name>
                            <itunes:email>{EMAIL}</itunes:email>
                        </itunes:owner>
                        <itunes:image href="{COVER_IMAGE}"/>
                        <itunes:category text="{CATEGORY}">
                            <itunes:category text="{SUBCATEGORY}"/>
                        </itunes:category>
                        <itunes:explicit>false</itunes:explicit>
                        {items_xml}
                    </channel>
                </rss>
                """

    # update rss.xml, spotify will be notified a RSS feed for new episodes
    with open("rss.xml", "w", encoding="utf-8") as f:
        f.write(rss_xml.strip())
    print("RSS Feed updated successfully!")

if __name__ == "__main__":
    generate_rss()
