VOWELS = ['a', 'e', 'i', 'u']
CONSONANTS = ['', 'b', 'd', 'g', 'h', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'z']
NASAL_CONSONANTS = ['m', 'n']

10.times do
  name = ''
  consonant_first = [true, false].sample
  # (3+rand(3)).times do
  5.times do
    syllable = [VOWELS.sample, CONSONANTS.sample].join
    if consonant_first
        syllable.reverse!
        syllable << NASAL_CONSONANTS.sample if rand(20) == 0
    end
    name << syllable
    consonant_first = true if syllable.size == 1
    consonant_first = !consonant_first if rand(3) == 0
  end
  puts name.capitalize
end


