VOWELS = ['a', 'e', 'i', 'u']
CONSONANTS = ['', 'b', 'd', 'g', 'h', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'z']


10.times do
  name = ''
  consonant_first = [true, false].sample
  3.times do
    syllable = [VOWELS.sample, CONSONANTS.sample].join
    syllable.reverse! if consonant_first
    name << syllable
    consonant_first = true if syllable.size == 1
    consonant_first = !consonant_first if rand(3) == 0
  end
  puts name.capitalize
end


