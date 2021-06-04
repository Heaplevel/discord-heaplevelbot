import unittest
import sched, time
from schedule import Scheduler

"""
Trying out scheduled task runner 
"""


class MyTestCase(unittest.TestCase):
    def test_something(self):
        scheduler = sched.scheduler()
        scheduler.run()

    def test_every_stuff(self):
        s = Scheduler()
        s.every(5).seconds.do(lambda x: print('hello'))




if __name__ == '__main__':
    unittest.main()
