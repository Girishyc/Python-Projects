import YoutubeRequstHandler
import json


class Channel:

    def __init__(self, channel_id, channel_video_stats):
        self.channel_id = channel_id
        self.channel_video_stats = channel_video_stats

    def to_json(self):
        return dict(channel_id=self.channel_id, channel_video_stats=self.channel_video_stats)


class Video:

    def __init__(self, video_id, video_stats, video_comments):
        self.video_id = video_id
        self.video_stats = video_stats
        self.video_comments = video_comments

    def to_json(self):
        return dict(video_id=self.video_id, video_stats=self.video_stats, video_comments=self.video_comments)

    def get_video_id(self):
        return self.video_id

    def get_video_stats(self):
        return self.video_stats

    def get_video_comments(self):
        return self.video_comments


class Comment:

    def __init__(self, comment_id, comment_text, comment_author_name):
        self.comment_id = comment_id
        self.comment_text = comment_text
        self.author_name = comment_author_name

    def to_json(self):
        return dict(comment_id=self.comment_id, comment_text=self.comment_text, comment_author_name=self.author_name)

    def get_comment_id(self):
        return self.comment_id

    def get_comment_text(self):
        return self.comment_text

    def get_author_name(self):
        return self.author_name


class Youtube:

    def __init__(self, channel_id):
        self.channel_id = channel_id

    def get_channel_stats(self):
        channel_video_stats = YoutubeRequstHandler.get_channel_video_stats(self.channel_id)
        return Channel(self.channel_id,  channel_video_stats)

    def get_video_stats(self, video_id):
        channel_video_stats = YoutubeRequstHandler.get_channel_video_stats_filtered(self.channel_id, video_id)
        return Channel(self.channel_id,  channel_video_stats)

