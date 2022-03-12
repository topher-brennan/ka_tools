from random import randint

def d(n=1):
    return sum([randint(1, 6) for _ in range(n)])

class Character(object):
    def __init__(self, ht=10, max_hp=10):
        self.ht = ht
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.alive = True

    def take_damage(self, damage):
        new_hp = self.hp - damage
        death_check_thresholds = [multiple * self.max_hp for multiple in [-1, -2, -3, -4]]
        for threshold in death_check_thresholds:
            if self.hp > threshold and new_hp <= threshold:
                self.make_death_check()
        self.hp = new_hp

    def make_death_check(self):
        if not self.make_ht_check():
            self.alive = False

    def make_ht_check(self):
        return d(3) <= min(self.get_effective_ht(), 16)

    # This assumes all missing HP is due to cholera, which works for this simulation.
    def get_effective_ht(self):
        if self.hp < self.max_hp / 3.0:
            return max(4, self.ht - 8)
        elif self.hp < self.max_hp / 2.0:
            return max(4, self.ht - 4)
        elif self.hp < self.max_hp * 2 / 3.0:
            return max(4, self.ht - 2)
        else:
            return self.ht

def inflict_cholera(character):
    for _ in range(d() + 1):
        if character.make_ht_check():
            break
        character.take_damage(d())
