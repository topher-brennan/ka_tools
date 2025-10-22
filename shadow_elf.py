from random import choice, random

stops = ['k', 'p', 't', '']
sonorants = ['f', 'm', 'n', 'ph', 'r', 's', 'sh', 'th', '']
vowels = ['a', 'ai', 'au', 'e', 'ei', 'eu', 'i', 'iu', 'o', 'oi', 'ou', 'u', 'ui']

def generate_word():
    return choice(stops) + choice(sonorants) + choice(vowels) + choice(sonorants) + choice(stops)

def generate_name():
    name = generate_word().capitalize()
    if random() < 0.5:
        name = name + '-' + generate_word()
    return name

print(generate_name())

