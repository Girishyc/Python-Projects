import json

import logging
import csv


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_json'):
            return obj.to_json()
        else:
            return json.JSONEncoder.default(self, obj)


class YoutubeDataWriter:
    CHANNEL_VIDEO_STATS_FILE_PATH = "data/channel_video_stats.json"
    CHANNEL_VIDEO_STATS_FILE_PATH_CSV = "data/channel_video_stats.csv"
    CHANNEL_VIDEO_COMMENTS_FILE_PATH_CSV = "data/channel_video_comments.csv"

    @staticmethod
    def dump_data_in_json_format(result):
        logging.info("Writing Channel stats to " + YoutubeDataWriter.CHANNEL_VIDEO_STATS_FILE_PATH)

        results_json_string = json.dumps(result.to_json(), cls=JSONEncoder, indent=2)
        data = json.loads(results_json_string)

        with open(YoutubeDataWriter.CHANNEL_VIDEO_STATS_FILE_PATH, 'w') as f:
            json.dump(data, f, indent=2)

        logging.info("Finished writing data to JSON file.")

    @staticmethod
    def dump_data_in_csv_format(result):
        logging.info("Writing channel video stats to " + YoutubeDataWriter.CHANNEL_VIDEO_STATS_FILE_PATH_CSV)
        results = json.dumps(result.to_json(), cls=JSONEncoder, indent=2)
        data = json.loads(results)

        rows = []
        for video in data['channel_video_stats']:
            row = {"video_id": video['video_id'],
                   "video_title": video['video_stats']['video_title'],
                   "video_view_count": video['video_stats']['statistics']['viewCount'],
                   "video_like_count": video['video_stats']['statistics']['likeCount'],
                   "video_dislike_count": video['video_stats']['statistics']['dislikeCount'],
                   "video_favorite_count": video['video_stats']['statistics']['favoriteCount'],
                   "video_comment_count": video['video_stats']['statistics']['commentCount']
                   }
            rows.append(row)

        YoutubeDataWriter.write_to_csv(rows, YoutubeDataWriter.CHANNEL_VIDEO_STATS_FILE_PATH_CSV)

        logging.info("Writing channel video comments to " + YoutubeDataWriter.CHANNEL_VIDEO_STATS_FILE_PATH_CSV)

        rows = []
        for video in data['channel_video_stats']:
            for comment in video['video_comments']:
                row = {"video_id": video['video_id'],
                       "video_title": video['video_stats']['video_title'],
                       "comment_id": comment['comment_id'],
                       "comment_text": comment['comment_text'],
                       "comment_author_name": comment['comment_author_name']
                       }
                rows.append(row)

        YoutubeDataWriter.write_to_csv(rows, YoutubeDataWriter.CHANNEL_VIDEO_COMMENTS_FILE_PATH_CSV)

        logging.info("Finished writing data to CSV files.")

    @staticmethod
    def write_to_csv(rows, file_name):
        count = 0
        with open(file_name, 'w') as f:
            csv_writer = csv.writer(f)
            for row in rows:
                if count == 0:
                    # Writing headers of CSV file
                    header = row.keys()
                    csv_writer.writerow(header)
                    count += 1

                # Writing data of CSV file
                csv_writer.writerow(row.values())
