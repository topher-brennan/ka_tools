class Royal
  def initialize(ifather=nil, mother=nil, age=0)
    @health = 11 + rand(3) + rand(2)
    @father = father
    @mother = mother
    @age = age
    @children = []
    # TODO: gender
    # TODO: holds_throne?
  end

  def have_birthday
    @age += 1
    make_aging_roll if @age >= 50 
    make_aging_roll if @age >= 70
    2.times { make_aging_roll } if @age >= 90
  end

  def make_aging_roll
  end
end

# Random events:
# * Killed by a hippopotamus (50% chance of affecting heir given heir of age 16+).
# * Killed in battle (50% chance of affecting heir given heir of age 16+).
# * Assassinated by brother, who seizes the throne (king must not no heirs older than 16), only to later be killed by the original heir.
# * If king has two wives, all his heirs are killed by palace intrigues.
# * Distant relative presses dubious claim to throne.
# * Roll twice!

# If a king's heir is very young when the king dies, chance of relative taking the throne (possibly king's brother *or* any female relative with male-line descent).

# 50% of kings have a single primary wife, 50% have two competing wives
# Kings always have at least 1d children per wife. They always keep trying for more children until they have at least one male heir.
# Wives have a 10% chance per month of getting pregnant. Gestation lasts 9 months and there is always 1d+9 months of infertility aftewards.
# ~1 in 200 births are stillbirths, maternal death in childbirth is nearly nonexistant.
# Wives become permanently infertile at 3d+40 years old.

# Aging rolls:
# * Frequency:
#   * Happens 1/year starting at age 50
#   * Happens 2/year starting at age 70
#   * Happens 4/year starting at age 90
# * Roll is vs. health+3:
#   * Failure reduces health by 1
#   * A roll of 17 or 18 automatically fails and reduces health by 2
#   * King dies at health <= 0
