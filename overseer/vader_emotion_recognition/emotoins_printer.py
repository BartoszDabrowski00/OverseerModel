from typing import Dict


def print_all_emotions_distribution(file_path: str, emotions_distribution: Dict[str, float]) -> None:
    print(f'File:{file_path}')
    for emotion_class, value in emotions_distribution.items():
        print(f'\t{emotion_class}: {value}')
    print()
