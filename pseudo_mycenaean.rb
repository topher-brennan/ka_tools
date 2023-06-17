SYLLABLES = [
  'a', 'e', 'i', 'o', 'u',
  'da', 'de', 'di', 'do', 'du',
  'ja', 'je', 'jo',
  'ka', 'ke', 'ki', 'ko', 'ku',
  'ma', 'me', 'mi', 'mo', 'mu',
  'na', 'ne', 'ni', 'no', 'nu',
  'pa', 'pe', 'pi', 'po', 'pu',
  'qa', 'qe', 'qi', 'qo',
  'ra', 're', 'ri', 'ro', 'ru',
  'sa', 'se', 'si', 'so', 'su',
  'ta', 'te', 'ti', 'to', 'tu',
  'wa', 'we', 'wi', 'wo', 'wo',
  'za', 'ze', 'zo',
  'ai', 'au', 'dwe', 'dwo', 'nwa', 'pte', 'phu', 'rya', 'rai', 'tya', 'twe', 'two',
  'swi', 'ju', 'zu', 'swa'
]

puts Array.new(2) { SYLLABLES.sample }.join.capitalize
puts Array.new(3) { SYLLABLES.sample }.join.capitalize
