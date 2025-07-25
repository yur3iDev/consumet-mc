from __future__ import annotations

import re
from consumet_mc.models.source import Source
from consumet_mc.models.video import Video
from consumet_mc.utils.packer import unpack
from consumet_mc.extractors.video_extractor import VideoExtractor


class Engifuosi(VideoExtractor):
    def extract(self) -> Source:
        videos = []
        try:
            headers = {"Referer": self.server.extra_data["referer"]}
            response = self.http_client.request("GET", self.server.url, headers=headers)
            response.raise_for_status()
            decoded_source = unpack(response.text)
            if decoded_source:
                video_url_regex = r"file:\"([^\"]*)\""
                match = re.search(video_url_regex, decoded_source)
                if match:
                    video_url = match.group(1)
                    videos.append(
                        Video(video_url, True if ".m3u8" in video_url else False)
                    )
            return Source(videos)

        except Exception as e:
            raise e
