import time
import json

class Vote:
    votes = {"default": 1}

    def __init__(self, name, positions):
        self.name = name
        self.vote_open = True
        self.positions = positions
        self.path = "votes/{}_{}.json".format(time.strftime("%Y%m%d-%H%M"), self.name)
        self.help = "!v [compo_name] [prod_name] [placement (range(0, {}))]".format(self.positions)

    def cast_vote(self, name, position, voter_id):
        if self.vote_open:
            if position in range(1, self.positions):
                self.votes[name][voter_id] = self.positions - position
            else:
                raise ValueError("Vote position out of range")
        else:
            return -1

    def close_voting(self):
        self.vote_open = False
        with open(self.path, "w") as f:
            json.dump(self.votes, f)

    def list_results(self):
        final_score = {}
        for name, vote in self.votes.items():
            for voter_id, score in vote.items():
                if name in final_score:
                    final_score[name] += score
                else:
                    final_score[name] = score

        sorted_results = [(k, final_score[k]) for k in sorted(final_score, key=final_score.get, reverse=True)]

        return sorted_results

