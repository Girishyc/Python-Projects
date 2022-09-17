import Youtube
from YoutubeApi import YoutubeApiHandler


def get_channel_videos(channel_id):
    return YoutubeApiHandler.get_channel_statistics(channel_id)


def get_channel_video_stats(channel_id):
    youtube_videos = []
    videos = get_channel_videos(channel_id)
    for video_id in videos:
        video_stats = YoutubeApiHandler.get_video_stats(video_id)
        video_comments = YoutubeApiHandler.get_comments(video_id)
        video = Youtube.Video(video_id, video_stats, video_comments)
        youtube_videos.append(video)
    return youtube_videos


def get_channel_video_stats_filtered(channel_id, vid):
    youtube_videos = []
    videos = get_channel_videos(channel_id)
    for video_id in videos:
        if video_id == vid:
            video_stats = YoutubeApiHandler.get_video_stats(video_id)
            video_comments = YoutubeApiHandler.get_comments(video_id)
            video = Youtube.Video(video_id, video_stats, video_comments)
            youtube_videos.append(video)
    return youtube_videos


def get_channel_video_comments(channel_id):
    youtube_video_comments = []
    videos = get_channel_videos(channel_id)
    for video_id in videos:
        video_comments = YoutubeApiHandler.get_comments(video_id)
        youtube_video_comments.append(video_comments)
    return youtube_video_comments
