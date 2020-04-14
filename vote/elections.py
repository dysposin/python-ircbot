#!/usr/bin/python3
from vote import vote

class Elections:
    def __init__(self):
        self.elections = {}
    def add_election(self, name):
        self.elections[name] = vote.Vote(name)

    def close_election(self, name):
        self.elections[name].close_voting()

    def vote(self, name, points, voter_id):
        self.elections[name].cast_vote(points, voter_id)

    def results(self, name=None):
        if name==None:
            for name, vote in self.elections.items():
                return name, vote.list_results()
        else:
            return name, self.elections[name].list_results()