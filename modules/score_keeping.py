import time


def get_current_time():
    start_time = time.time()
    return start_time


def get_score_time(start_time, end_time, timer):
    score_time = timer - (end_time - start_time)
    return score_time
