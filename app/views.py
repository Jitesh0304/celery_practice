from django.shortcuts import render
from django.http import HttpResponse
from .tasks import add, mul, calculate, sum_results, on_raw_message
from celery import signature, group, chain, chord, subtask
from project.celery import error_handler, debug_task, hello, addNum
from datetime import datetime, timedelta
from django.utils import timezone
from kombu.exceptions import TimeoutError


# Create your views here.
def homepage(request):
        ## add signature to a task
    # task1_res = add.signature((2, 2),countdown=2)
        ## call the task to excute
    # task1_res()


        ## s is the shutcut of signature .... you need to call this signature after defining ()
    # task1_res = add.s(2, 2)()
        ## or
    # task1_res = add.s(2, 2)
    # task1_res.apply_async()       ## add signature and call it using apply_async()


    # task1_res = add.s(2, 2).set(countdown=20)         ## countdown will help you to execute the task after the mentioned time
    # task1_res.apply_async()                           ## celery will receive the task but it execute the task after mentioned time


        ## delay is our beloved shortcut to apply_async taking star-arguments:
    # task1_res = add.delay(2, 2)


        ## apply_async takes the same arguments 
    # task1_res = add.s(2, 2).apply_async()
    # task1_res = add.apply_async((2, 2), countdown=10)


    #     ## Create an initial task signature
    # original_sig = add.s(2, 2)
    #     ## Clone the signature 
    # cloned_sig = original_sig.clone()
    #     ## Apply the cloned signature
    # clone_result = cloned_sig.apply_async()


        ## using link task i can execute one after another task ... 1st task result will go to 2nd task as a input
    # add.apply_async((2, 2), link=add.s(8))



        ## group multiple tasks together to run in parallel
    # task_group = group(add.s(2, 2), add.s(4, 4), add.s(8, 8))
    # result = task_group.apply_async()


    # task_group = [add.s(2, 2), add.s(4, 4), add.s(8, 8)]
    # result = group(task_group).apply_async()



    # job = group([
    #             add.subtask((2, 2)),
    #             add.subtask((4, 4)),
    #             add.subtask((8, 8)),
    #             add.subtask((16, 16)),
    #             add.subtask((32, 32)),
    # ])
    # result = job.apply_async()




        ## Chain multiple tasks together
    # chain_task = add.s(2, 2) | mul.s(4)    ## 1st task result will go to 2nd task as a input
    # chain_result = chain_task.apply_async()


    # chain_task = chain(add.s(2, 2), mul.s(5))     ## 1st task result will go to 2nd task as a input
    # result = chain_task.apply_async()
            ## chain
    # chain_task = chain(add.s(2, 2), mul.s(5))()     ## 1st task result will go to 2nd task as a input
    # result.get()


    # chain_task = chain(add.s(2, 2), mul.s(5,10))     ## 1st task result will go to 2nd task as a input
    # result = chain_task.apply_async(link_error=error_handler.s())


    # chain_task = chain(add.s(2, 2), mul.s(5, 10).set(immutable=True))    ## in this casesSecond task, will not use the result of the first task
    # result = chain_task.apply_async()



        ## Create a chord where a callback is called after a group of tasks completes
    # group_tasks = [
    #     add.s(2, 2),
    #     mul.s(3, 3),
    #     add.s(4, 4),
    #     mul.s(5, 5)
    # ]
    # chord_task = chord(group_tasks)(sum_results.s())


            ## map and starmap are built-in tasks that call the provided calling task for every element in a sequence.
            ## Both map and starmap are signature objects, so they can be used as other signatures and combined in groups
    # ~sum_results.map([list(range(10)), list(range(50))])
            ## or
    # sum_results.map([list(range(10)), list(range(50))]).apply_async(countdown=10)




    # ~add.starmap(zip(range(10), range(10)))
            ## or
    # add.starmap(zip(range(10), range(10))).apply_async(countdown=10)



    # add.chunks(zip(range(100), range(100)), 10)()
            ## or
    # res = add.chunks(zip(range(10), range(10)), 5)()
            ## or
    # add.chunks(zip(range(100), range(100)), 10).apply_async()
            ## or
    # group_task = add.chunks(zip(range(100), range(100)), 10).group()
    # group_task.skew(start=1, stop=10)()



    # debug_task.apply_async()


        ## because of some reason "on_message" is showing error
    # a, b = 1, 1
    # r = hello.apply_async(args=(a, b))
    # print(r.get(on_message=on_raw_message, propagate=False))




    """
    The ETA (estimated time of arrival) lets you set a specific date and time that is the earliest time at 
    which your task will be executed. countdown is a shortcut to set ETA by seconds into the future.

    While countdown is an integer, eta must be a datetime object, specifying an exact date and time 
    (including millisecond precision, and timezone information):
    """

    # result = add.apply_async((2, 2), countdown=3)
            ## or
    # tomorrow = timezone.now() + timedelta(days=1)
    # add.apply_async((2, 2), eta=tomorrow)


        ## The expires argument defines an optional expiry time, either as seconds after task publish, 
        ## or a specific date and time using datetime:

    # add.apply_async((10, 10), expires=10)
            ## or
    # add.apply_async((10, 10), expires=datetime.now(timezone.utc) + timedelta(days=1))



            ## retry
    # add.apply_async((2, 2), retry=False)
    # add.apply_async((2, 2), retry=True)
            ## or
    # add.apply_async((2, 2), retry=True, retry_policy={
    #     'max_retries': 3,
    #     'interval_start': 0,
    #     'interval_step': 0.2,
    #     'interval_max': 0.2,
    #     'retry_errors': None,
    # })

    return HttpResponse('task completed')


