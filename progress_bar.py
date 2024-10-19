import sys


def progress_bar(bar_name: str, iteration: int, total: int, length: int = 40):
    percent = (iteration / total) * 100
    bar_length = int(length * percent // 100)
    bar = '█' * bar_length + '-' * (length - bar_length)

    sys.stdout.write(f'\r|{bar_name}|{bar}| {percent:.2f}%')
    sys.stdout.flush()
