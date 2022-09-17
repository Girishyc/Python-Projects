import requests
import http
import Youtube
import logging


class YoutubeApiHandler:

    @staticmethod
    def get_channel_statistics(channel_id):
        channel_videos = []
        logging.info("Downloading channel video details.")
        try:
            url = f"https://www.googleapis.com/youtube/v3/search?channelId={channel_id}&key=AIzaSyB56CmcQ31" \
                  f"-KgKH_yhnb5pL_RNDbJs7ang&&part=snippet,id&order=date&maxResults=100"
            results, next_page_token = YoutubeApiHandler.get_results_per_page(url)
            first_request = True
            while next_page_token is not None or first_request:
                first_request = False
                for item in results['items']:
                    if item['id']['kind'] == 'youtube#video':
                        video_id = item['id']['videoId']
                        channel_videos.append(video_id)
                if next_page_token:
                    next_url = url + "&pageToken=" + next_page_token
                    results, next_page_token = YoutubeApiHandler.get_results_per_page(next_url)
            logging.info("Finished downloading channel video details.")
            logging.info(f'Downloaded detail for {len(channel_videos)} videos')
        except Exception as e:
            logging.error("Failed to get channel statistics.", e)

        return channel_videos

    @staticmethod
    def get_video_stats(video_id):
        try:
            url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key=AIzaSyB56CmcQ31" \
                  f"-KgKH_yhnb5pL_RNDbJs7ang&fields=items(id,snippet(channelId,title,categoryId)," \
                  f"statistics)&part=snippet,statistics "
            response = requests.get(url)
            if response.status_code != http.HTTPStatus.OK:
                print("Failed to get video stats")
            else:
                results = response.json()
                video_title = results['items'][0]['snippet']['title']
                video_stats = results['items'][0]['statistics']
                return {"video_title": video_title, "statistics": video_stats}
        except Exception:
            logging.error("Failed to get video stats.")
        return None

    @staticmethod
    def get_comments(video_id):
        video_comments = []
        try:
            url = f"https://www.googleapis.com/youtube/v3/commentThreads?key=AIzaSyB56CmcQ31-KgKH_yhnb5pL_RNDbJs7ang" \
                  f"&textFormat=plainText&part=snippet&videoId={video_id}&maxResults=100"
            results, next_page_token = YoutubeApiHandler.get_results_per_page(url)
            first_request = True
            while next_page_token is not None or first_request:
                for item in results['items']:
                    if item['kind'] == 'youtube#commentThread':
                        comment_id = item['id']
                        comment_text = item['snippet']['topLevelComment']['snippet']['textOriginal']
                        comment_author_name = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
                        comment = Youtube.Comment(comment_id, comment_text, comment_author_name)
                        video_comments.append(comment)
                first_request = False
                if next_page_token:
                    next_url = url + "&pageToken=" + next_page_token
                    results, next_page_token = YoutubeApiHandler.get_results_per_page(next_url)
            return video_comments
        except Exception as e:
            logging.error("Failed to get video comments : ", e)

    @staticmethod
    def get_results_per_page(url):
        results = None
        response = requests.get(url)
        if response.status_code != http.HTTPStatus.OK:
            logging.error("Failed to execute youtube api request.")
        else:
            results = response.json()
        return results, results.get('nextPageToken')
