require 'securerandom'

class Dynasty
end

class Royal
  def initialize(options={})
    @genetic_diseases = options[:genetic_diseases] || []
    @carried_genetic_diseases = options[:carried_genetic_diseases] || [SecureRandom.uuid]
    @health = one_d + 8
    @health -= 4 if @genetic_diseases.size > 0
    @father = options[:father]
    @mother = options[:mother]
    @age_quarters = options[:age_quarters] || 0
    @children = options[:children] || []
    @wives = options[:wives] || []
    @husband = options[:husband]
    @gender = options[:gender] = 'MALE'
    @current_ruler = options[:current_ruler] = false
    @former_ruler = options[:former_ruler] = false
  end

  def age_years
    @age_quarters / 4
  end

  def simulate_quarter
    @age_quarters += 1
    if age_years >= 90
      make_aging_roll
    elsif age_years >= 70 && @age_quarters % 2 == 0
      make_aging_roll
    elsif age_years >= 50 && @age_quarters % 4 == 0
      make_aging_roll
    end
  end

  def make_aging_roll
    roll = three_d
    if roll >= 17
      @health -= 2
    elsif roll > @health + 5
      @health -= 1
    elsif !@current_ruler && roll > @health
      @health -= 2
    end
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

# Ways royals can die (should all be very rare):
# * Position in the Southlands overrun (kills with no health check or chance of resurrection, ideally should happen once to ruler and once to crucial non-ruler)
# * Palace intrigue: if king has sons by multiple wives, random wife and all her sons execeuted for treason (ideally should happen exactly once in 700 years)
# * Serious palace coup involving burning of body (ideally should happen exactly once in 700 years)

# If a king's heir is very young when the king dies, chance of relative taking the throne (possibly king's brother *or* any female relative with male-line descent).
#   * IMPORTANT: This event may require some human adjudication

# Kings always have at least 1d+1 children per wife. They always keep trying for more children until they have at least one male heir.
# Pregnancy:
# * Wives have a 8 or less on 3d chance per quarter of getting pregnant.
# * Gestation lasts 9 months.
# * -5 to conceive for the first quarter after giving birth.
# * Decrease penalty by 1 step for each additional quarter after giving birth, to a minimum of 0.
# Ignore stillbirths and maternal death.
# Women can't conceive if age >= 50.
# Kings will take a second wife if the first one doesn't produce an heir within 5 years.
# Other male royals don't take second wives.
# Men first marry at age 12d/4+17 years
# A male royal's first choice is to marry a woman with an independent claim to the throne between the ages of 15 and 20. If none is available, a new female character can be created with a starting age of 4d/4+14.
# * People never marry their direct descendants / ancestors or siblings but everyone else is fair game.

# Kings get +5 to health for all purposes except they are still dead if health reaches 0 for any reason.

# Aging rolls:
# * Frequency:
#   * Happens 1/year starting at age 50
#   * Happens 2/year starting at age 70
#   * Happens 4/year starting at age 90
# * Roll is vs. health-2:
#   * Failure reduces health by 1
#   * A roll of 17 or 18 automatically fails and reduces health by 2
#   * Character dies at health <= 0

# TODO: Game should have a "founder" singleton field.
# Family tree pruning (don't simulate characters who are more than 4 generations from an actual king, e.g. a thrice-great grandchild).
