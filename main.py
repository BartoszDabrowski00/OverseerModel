import os
import logging
from audio_converter import convert_audio_to_text
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from emotoins_printer import print_all_emotions_distribution
TEST_RECORDINGS = os.environ.get('TEST_RECORDINGS', 'recordings')
log = logging.getLogger(__name__)


def test(path: str) -> None:
    if not os.path.exists(path):
        log.error("Given directory deos not exist.")

    sa = SentimentIntensityAnalyzer()
    file_paths = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for file in file_paths:
        text = convert_audio_to_text(file)
        if text is None:
            continue
        emotions_distribution = sa.polarity_scores(text)
        print_all_emotions_distribution(file, emotions_distribution)


if __name__ == '__main__':
    test(TEST_RECORDINGS)
