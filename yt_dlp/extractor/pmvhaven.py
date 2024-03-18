from .common import InfoExtractor
from ..utils import str_to_int


class PMVHavenIE(InfoExtractor):
    _VALID_URL = r"https?://(?:www\.)?pmvhaven\.com/video/(?P<id>[^/?#&]+)"
    _TESTS = [
        {
            "url": "https://pmvhaven.com/video/The-World-PMV-Games-2024-Teaser-Trailer_65b59829a16402620cc668ca",
            "md5": "d4fb76a4ed8111d4e93acaa2877fd7d5",
            "info_dict": {
                "id": "65b59829a16402620cc668ca",
                "display_id": "The-World-PMV-Games-2024-Teaser-Trailer_65b59829a16402620cc668ca",
                "ext": "mp4",
                "title": "The World PMV Games 2024 Teaser Trailer",
                "description": "Experience the mesmerizing PMV - The World PMV Games 2024 Teaser Trailer created by AverageJay",
                "tags": "count:13",
                "thumbnail": "https://storage.pmvhaven.com/65b597e12dd3bd447560833e/thumbnail/240_65b597e12dd3bd447560833e.jpeg",
                "width": 1920,
                "height": 1080,
                "age_limit": 18,
            },
        }
    ]

    def _real_extract(self, url):
        # video_id is initially the display ID from the URL until we get the real ID from the page's source
        video_id = self._match_valid_url(url).group("id")
        html = self._download_webpage(url, video_id)

        # Update the video_id to the *actual* ID from the page's video-id meta tag
        display_id = video_id
        video_id = self._html_search_meta("video-id", html)

        # Title, description, etc.
        title = self._html_search_meta(["og:title", "twitter:title"], html, "title")
        description = self._html_search_meta(
            ["og:description", "description"], html, "description"
        )
        tags = self._html_search_meta(["og:video:tag", "keywords"], html)
        thumbnail = self._html_search_meta(["og:image", "twitter:image"], html)
        width = self._html_search_meta(["og:video:width", "twitter:player:width"], html)
        height = self._html_search_meta(
            ["og:video:height", "twitter:player:height"], html
        )

        # Actual source video URL
        video_url = self._html_search_meta(
            ["og:video:secure_url", "og:video", "twitter:player"], html
        )

        return {
            "url": video_url,
            "id": video_id,
            "display_id": display_id,
            "title": title,
            "description": description,
            "tags": [x for x in tags.split(", ") if x],
            "thumbnail": thumbnail,
            "width": str_to_int(width),
            "height": str_to_int(height),
            "age_limit": 18,
        }
