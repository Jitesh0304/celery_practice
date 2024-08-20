from celery import shared_task, chunks
import time
from django.utils import timezone
from time import sleep


@shared_task
def process_pdf(pdf_path):
    print(f"Processing PDF: {pdf_path}")
    print(f"Processing time: {timezone.now().time()}")
    sleep(3)

@shared_task
def s3_pro():
    pdf_paths = [[f"pdf_{i}.pdf"] for i in range(1, 101)]
    batch_size=10
    # chunk = process_pdf.chunks(pdf_paths, 10)()
    chunk = process_pdf.chunks(zip(pdf_paths), batch_size)().apply_async()


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