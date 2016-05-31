'''
@author: Gergely Acs <acs@crysys.hu>
'''

from progressbar import Bar, ETA, Percentage, ProgressBar

class MyProgressBar:

    def __init__(self, label, maxv):
        widgets = [label + ' ', Percentage(), ' ', Bar(), ' ', ETA()]
        self.pbar = ProgressBar(widgets=widgets, maxval=maxv).start()

    def update(self, num):
        self.pbar.update(num)

    def finish(self):
        self.pbar.finish()

