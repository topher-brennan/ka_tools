require 'securerandom'

class Dynasty
end

class Royal
  attr_accessor :age_quarters, :children, :current_ruler, :father, :husband, :mother, :predecessor, :quarters_to_next_marriage, :successor, :wives

  def initialize(options={})
    @father = options[:father]
    @mother = options[:mother]
    @health = one_d + 8 - (inbreeding_coefficient * 4).floor
    @age_quarters = options[:age_quarters] || 0
    @children = options[:children] || []
    @wives = options[:wives] || []
    @husband = options[:husband]
    @gender = options[:gender] || :male
    @current_ruler = options[:current_ruler] || false
    @former_ruler = options[:former_ruler] || false
    @quarters_to_next_marriage = 68 + n_d(12)
    @quarters_to_next_birth = nil
    @children_soft_cap = one_d
    @done_having_children = false
    @predecessor = nil
    @successor = nil
    @reign_quarters = 0
    @ancestor_chains = nil
  end

  def print_family_tree(depth=0)
    line = ' ' * depth + "#{alive? ? 'o' : 'x'}#{object_id}:\t"
    line += 'M' if male?
    line += 'F' if female?
    line += '*' if married_to_princess?
    line += "\tAge: #{age_years}"
    if @reign_quarters > 0
      line += "\tReign Length: #{@reign_quarters / 4}" 
    else
      line += "\tGenerations to Claim: #{generations_to_claim}"
    end
    puts line
    @children.each { |child| child.print_family_tree(depth+1) }
    true
  end

  def age_years
    @age_quarters / 4
  end

  def simulate_quarter
    if male?
      @children.each { |child| child.simulate_quarter }
      @wives.each do |wife|
        wife.simulate_quarter if wife.father.nil?
      end
    end

    if alive?
      @age_quarters += 1
      @reign_quarters += 1 if @current_ruler
      if age_years >= 90
        make_aging_roll
      elsif age_years >= 70 && @age_quarters % 2 == 0
        make_aging_roll
      elsif age_years >= 50 && @age_quarters % 4 == 0
        make_aging_roll
      end

      if male? && male_heirs.none? && generations_to_claim < 5
        @quarters_to_next_marriage -= 1
        bride = (generations_to_claim < 3 ? find_bride : nil)

        if (bride && age_years >= 20 && @wives.none?) ||
            (@quarters_to_next_marriage < 1 && @wives.none?(&:pregnant?))
          bride ||= Royal.new({age_quarters: 56 + n_d(4), gender: :female})
          bride.husband = self
          @wives << bride 
          @quarters_to_next_marriage = 16
        end
      end
      
      if female?
        if pregnant?
          if @quarters_to_birth
            @quarters_to_birth -= 1
            if @quarters_to_birth < 1
              @quarters_to_birth = nil
              bear_child
            end
          end
        elsif husband_alive? && age_years < 50 && !@done_having_children
          3.times { @quarters_to_birth = 3 if three_d <= 6 - recent_birth_modifier }
        end

        if @children.size >= @children_soft_cap && @husband.male_heirs.any?
          @done_having_children = true
        end
      end
    end
  end

  def make_aging_roll
    roll = three_d
    if roll >= 17
      @health -= 2
    elsif roll > modified_health - 2
      @health -= 1
    end
  end

  def modified_health
    result = @health
    if @current_ruler
      result += 5
    elsif crown_prince?
      result += 4
    end
    result
  end

  def crown_prince?
    @father && @father.current_ruler && @father.sons.first == self
  end

  def generations_to_claim
    return 0 if @current_ruler || @reign_quarters > 0
    return Float::INFINITY if !@father
    @father.generations_to_claim + 1
  end

  def recent_birth_modifier
    (@children.map { |child| 3 - child.age_quarters / 2 } + [0]).max 
  end

  def bear_child
    child = Royal.new({
      mother: self,
      father: @husband,
      gender: [:male, :female].sample
    })

    @children << child
    @husband.children << child
  end

  def end_reign(heir=nil)
    heir ||= male_heirs.first
    raise Exception.new("Cannot automatically designate heir") if heir.nil?
    
    @current_ruler = false
    heir.current_ruler = true

    @successor = heir
    heir.predecessor = self
    true
  end

  def die
    @health = 0
  end

  def alive?
    @health > 0
  end

  def dead?
    !alive?
  end

  def male?
    @gender == :male
  end

  def female?
    @gender == :female
  end

  def pregnant?
    !@quarters_to_birth.nil?
  end
  
  def husband_alive?
    @husband && @husband.alive?
  end

  def sons
    @children.filter(&:male?)
  end

  def daughters
    @children.filter(&:female?)
  end

  def sisters
    (@father && @father.daughters) || []
  end

  def dynasty_founder
    @father ? @father.dynasty_founder : self
  end

  def male_heirs
    result = []
    sons.each do |son|
      result << son if son.alive?
      result += son.male_heirs
    end
    result
  end

  def female_heirs
    result = daughters.filter(&:alive?)
    sons.each do |son|
      result += son.female_heirs
    end
    result
  end

  def male_heirs_through_multiple_wives?
    @wives.filter do |wife|
      wife.male_heirs.any?
    end.size > 1
  end

  def find_bride
    dynasty_founder.female_heirs.filter do |fr| # fr = female relative
      fr.husband.nil? && 
          fr.age_quarters >= 60 &&
          fr.age_quarters <= 80 &&
          fr.generations_to_claim < 5
          !sisters.include?(fr) && 
          !daughters.include?(fr)
    end.sample
  end

  def married_to_princess?
    @wives.any? { |wife| wife.generations_to_claim < 5 }
  end

  def ancestor_chains(force_recalculate = false)
    return @ancestor_chains if @ancestor_chains && !force_recalculate

    chains = []

    if @father
      chains << [@father]
      @father.ancestor_chains(force_recalculate).each do |chain|
        chains << (chain + [@father])
      end
    end

    if @mother
      chains << [@mother]
      @mother.ancestor_chains(force_recalculate).each do |chain|
        chains << (chain + [@mother])
      end
    end

    @ancestor_chains = chains
    @ancestor_chains
  end

  def inbreeding_coefficient
    result = 0
    l = ancestor_chains.size

    (0...l).each do |i|
      (i+1...l).each do |j|
        first_chain = ancestor_chains[i]
        second_chain = ancestor_chains[j]
        if first_chain.first == second_chain.first && first_chain[1...].none? { |el| second_chain.include?(el) }
          result += 0.5 ** (first_chain.size + second_chain.size - 1)
        end
      end
    end

    result
  end
end

def one_d
  rand(6)+1
end

def n_d(n)
  Array.new(n) { one_d }.inject(:+)
end

def three_d
  n_d(3)
end

def run_simulation(ruler, random_pause_chance=0.01)
  raise Exception.new("Invalid ruler.") unless ruler.current_ruler
  founder = ruler.dynasty_founder
  while ruler.alive? && rand > random_pause_chance && !ruler.male_heirs_through_multiple_wives? &&
      !(ruler.male_heirs.first && ruler.male_heirs.first.male_heirs_through_multiple_wives?)
    founder.simulate_quarter
  end

  ruler.end_reign if ruler.dead?
  ruler.alive?
end

# Ways royals can die young (should all be very rare):
# * Position in the Southlands overrun (kills with no health check or chance of resurrection, ideally should happen once to ruler and once to crucial non-ruler)
# * Palace intrigue: if king has sons by multiple wives, random wife and all her sons execeuted for treason (ideally should happen exactly once in 700 years)
# * Serious palace coup involving burning of body (ideally should happen exactly once in 700 years)

# If a king's heir is very young when the king dies, chance of relative taking the throne (possibly king's brother *or* any female relative with male-line descent).
#   * IMPORTANT: This event may require some human adjudication

# TODO: Figure out how to calculate degree of inbred-ness.
