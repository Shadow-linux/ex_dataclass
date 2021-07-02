import time
from concurrent.futures.thread import ThreadPoolExecutor


# 参数times用来模拟网络请求的时间
def get_html(times):
    time.sleep(times)
    print("get page {}s finished".format(times))
    return times

# executor = ThreadPoolExecutor(max_workers=2)
# # 通过submit函数提交执行的函数到线程池中，submit函数立即返回，不阻塞
# task1 = executor.submit(get_html, 3)
# task2 = executor.submit(get_html, (2))
# # done方法用于判定某个任务是否完成
# print(task1.done())
# # cancel方法用于取消某个任务,该任务没有放入线程池中才能取消成功
# print(task2.cancel())
# time.sleep(4)
# print(task1.done())
# # result方法可以获取task的执行结果
# print(task1.result())

from src._turbo import FutureTurboEngine

fte = FutureTurboEngine()
fte.refuel(get_html, 5)
fte.refuel(get_html, 5)
for r in fte.as_complete():
    print(r)