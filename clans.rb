INITIAL_NUM_CLANS = 750_000

def get_num_wives
  case rand
  when 0...0.35
    0
  when 0.35...0.8
    1
  when 0.8...0.9
    2
  when 0.9...0.95
    3
  when 0.95...1
    4
  end
end

def get_adult_sons_for_wife
  result = 0
  7.times { result += 1 if rand < 1.0 / 7 }
  result
end

clans = [1] * INITIAL_NUM_CLANS
3.times do
  clans.map! do |num_members|
    new_num_members = 0
    num_members.times do
      get_num_wives.times do
        new_num_members += get_adult_sons_for_wife
      end
    end
    new_num_members
  end
end

def median(array)
  return nil if array.empty?
  sorted = array.sort
  len = sorted.length
  (sorted[(len - 1) / 2] + sorted[len / 2]) / 2.0
end

clans.reject! { |item| item == 0 }.sort!
households = []
clans.each do |item|
  item.times do
    households << item
  end
end

total_households = clans.inject(:+)

puts "Total households: #{total_households}"
puts "Number of clans: #{clans.size}"
puts "Number of one-household clans: #{clans.select { |item| item == 1}.size}"
puts "Largest clan: #{clans[-1]} households"
puts "Mean households per clan: ~#{(total_households / clans.size).round(1)}"
puts "The median clan contains #{median(clans).to_i} households."
puts "The median household has #{median(households).to_i - 1} other households in its clan."
