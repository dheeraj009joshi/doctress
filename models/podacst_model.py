class Podcast:
    def __init__(self, pod_title="", pod_thumbnail="", pod_video_url="", pod_description=""):
        self.pod_title = pod_title
        self.pod_thumbnail = pod_thumbnail
        self.pod_video_url = pod_video_url
        self.pod_description = pod_description

    @staticmethod
    def from_dict(podcast_dict):
        return Podcast(
            podcast_dict.get('pod_title', ""),
            podcast_dict.get('pod_thumbnail', ""),
            podcast_dict.get('pod_video_url', ""),
            podcast_dict.get('pod_description', "")
        )

    def to_dict(self):
        return {
            'pod_title': self.pod_title,
            'pod_thumbnail': self.pod_thumbnail,
            'pod_video_url': self.pod_video_url,
            'pod_description': self.pod_description
        }
