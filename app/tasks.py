from celery import shared_task
import time



@shared_task
def add(x, y):
    time.sleep(3)
    return x + y



@shared_task
def mul(x, y):
    time.sleep(5)
    return x * y



@shared_task
def calculate(a, b):
    if a < b:
        result = b - a
    else:
        result = a - b
    return result



@shared_task
def sum_results(results):
    return sum(results)



def on_raw_message(body):
    print(body)