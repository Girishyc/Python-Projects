from Youtube import Youtube
from YoutubeDataWriter import YoutubeDataWriter
import logging
import logging.config

logging.config.fileConfig('config/logging.conf')
logger = logging.getLogger(__name__)


def run():
    channel_id = 'UCHAK6CyegY22Zj2GWrcaIxg'
    youtube = Youtube(channel_id)
    logger.info(f'Downloading data for youtube channel {channel_id}')
    result = youtube.get_channel_stats()
    logger.info(f'Finished downloading data for youtube channel {channel_id}')
    YoutubeDataWriter.dump_data_in_json_format(result)
    YoutubeDataWriter.dump_data_in_csv_format(result)


if __name__ == '__main__':
    run()
