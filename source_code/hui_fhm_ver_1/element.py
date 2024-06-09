class Element:
    def __init__(self, t_id=-1, iutils=0, rutils=0):
        """
        pass params
        :param tid: transaction id (Integer)
        :param iutils: itemset utility (Integer)
        :param rutils: remaining utility (Integer)
        """
        self.t_id = t_id
        self.iutils = iutils
        self.rutils = rutils

    @property
    def get_iutils(self):
        return self.iutils

    @property
    def get_rutils(self):
        return self.rutils

    def __str__(self):
        return f"{self.tid}: iutils = {self.iutils} - rutils = {self.rutils}"
