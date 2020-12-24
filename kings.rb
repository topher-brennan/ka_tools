require 'securerandom'

class Dynasty
end

class Royal
  attr_accessor :carried_genetic_diseases, :children, :current_ruler, :father, :predecessor, :quarters_to_next_marriage, :successor

  def initialize(options={})
    @genetic_diseases = options[:genetic_diseases] || []
    @carried_genetic_diseases = options[:carried_genetic_diseases] || [SecureRandom.uuid]
    @health = one_d + 8
    @health -= 4 if @genetic_diseases.any?
    @father = options[:father]
    @mother = options[:mother]
    @age_quarters = options[:age_quarters] || 0
    @children = options[:children] || []
    @wives = options[:wives] || []
    @husband = options[:husband]
    @gender = options[:gender] || :male
    @current_ruler = options[:current_ruler] || false
    @former_ruler = options[:former_ruler] || false
    @quarters_to_next_marriage = 68 + n_d(12)
    @quarters_to_next_birth = nil
    @quarters_since_last_birth = nil
    @children_soft_cap = one_d
    @done_having_children = false
    @predecessor = nil
    @successor = nil
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
      if age_years >= 90
        make_aging_roll
      elsif age_years >= 70 && @age_quarters % 2 == 0
        make_aging_roll
      elsif age_years >= 50 && @age_quarters % 4 == 0
        make_aging_roll
      end

      if male? && male_heirs.empty?
        @quarters_to_next_marriage -= 1
        if @quarters_to_next_marriage < 1 && @wives.none?(&:pregnant?)
          @wives << Royal.new({age_quarters: 56 + n_d(4), gender: :female, husband: self})
          @quarters_to_next_marriage = 16
        end
      end
      
      if female?
        if pregnant?
          if @quarters_to_birth
            @quarters_to_birth -= 1
            if @quarters_to_birth < 1
              @quarters_to_birth = nil
              @quarters_since_last_birth = 0
              bear_child
            end
          end
        elsif husband_alive? && age_years < 50 && !@done_having_children
          roll = three_d
          if roll < 8 - recent_birth_modifier
            @quarters_to_birth = 3
          end
        elsif @quarters_since_last_birth
          @quarters_since_last_birth += 1
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

    if @health < 1
      if female? && husband_alive?
        @husband.quarters_to_next_marriage = one_d
      end

      if male? && @current_ruler
        @current_ruler = false
        @former_ruler = true
        male_heirs.first && male_heirs.first.current_ruler = true
      end
    end
  end

  def modified_health
    result = @health
    result += 5 if @current_ruler
    result
  end

  def bear_child
    maternal_curse = generate_curse
    paternal_curse = @husband.generate_curse

    full_curse = maternal_curse & paternal_curse
    half_curse = (maternal_curse | paternal_curse) - full_curse

    child = Royal.new({
      genetic_diseases: full_curse,
      carried_genetic_diseases: half_curse,
      mother: self,
      father: @husband,
      gender: [:male, :female].sample
    })

    @children << child
    @husband.children << child
  end

  def generate_curse
    Set.new(@genetic_diseases + @carried_genetic_diseases.filter { one_d <= 3 })
  end
  
  def die
    @health = 0
  end

  def alive?
    @health > 0
  end

  def dead?
    !alive!
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

  def recent_birth_modifier
    @quarters_since_last_birth ? [5 - @quarters_since_last_birth, 0].max : 0
  end

  def sons
    @children.filter(&:male?)
  end

  def male_heirs
    result = []
    sons.each do |son|
      result << son if son.alive?
      result += son.male_heirs
    end
    result
  end
end

def one_d
  rand(6)+1
end

def n_d(n)
  Array.new(n) { one_d }.inject(0, :+)
end

def three_d
  n_d(3)
end

# Ways royals can die young (should all be very rare):
# * Position in the Southlands overrun (kills with no health check or chance of resurrection, ideally should happen once to ruler and once to crucial non-ruler)
# * Palace intrigue: if king has sons by multiple wives, random wife and all her sons execeuted for treason (ideally should happen exactly once in 700 years)
# * Serious palace coup involving burning of body (ideally should happen exactly once in 700 years)

# If a king's heir is very young when the king dies, chance of relative taking the throne (possibly king's brother *or* any female relative with male-line descent).
#   * IMPORTANT: This event may require some human adjudication

# A male royal's first choice is to marry a woman with an independent claim to the throne between the ages of 15 and 20. If none is available, a new female character can be created with a starting age of 4d/4+14.
# * People never marry their direct descendants / ancestors or siblings but everyone else is fair game.

# Kings get +5 to health for all purposes except they are still dead if health reaches 0 for any reason.

# TODO: Game should have a "founder" singleton field.
# TODO: Family tree pruning (don't simulate characters who are more than 4 generations from an actual king, e.g. a thrice-great grandchild).
