import threading
import time
import asyncio

from app.topics.tasks import auto_close_pending_closed_discussion, mark_stale_discussions


def execute_task_with_countdown(task, args=None, countdown=3):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    time.sleep(countdown)
    if args:
        task(*args)
    else:
        task()
    return


def execute_task_periodically(task, num_periods, period_length, args=None):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    for i in range(num_periods):
        if args:
            task(*args)
        else:
            task()
        time.sleep(period_length)


def auto_close_pending_closed_discussion_task(args, countdown):
    thread = threading.Thread(target=execute_task_with_countdown, args=(auto_close_pending_closed_discussion,),
                              kwargs={'args': args, 'countdown': countdown}, daemon=True)
    thread.start()


def mark_stale_discussions_task(num_periods=3, period_length=2.5):
    thread = threading.Thread(target=execute_task_periodically,
                              args=(mark_stale_discussions, num_periods, period_length),
                              daemon=True)
    thread.start()
