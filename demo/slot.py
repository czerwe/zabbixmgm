

class slotme(object):
    """docstring for slotme"""
    __slots__ = ('b',)

    def __init__(self):
        super(slotme, self).__init__()
        
    @property
    def v(self):
        return self.b

    @v.setter
    def v(self, value):
        self.b = value


class slotmechild(slotme):
    __slots__ = ('l',)
    """docstring for slotmechild"""
    def __init__(self):
        super(slotmechild, self).__init__()
        


z = slotmechild()

z.b = 'sss'
print(z.b)

z.v = 'sss1'
print(z.v)

# z.n = 'ss5s'
# print(z.n)

print(z.__slots__)
