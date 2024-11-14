class User
  attr_accessor :name, :email, :age

  def initialize(name, email, age)
    self.name = name
    self.email = email
    self.age = age
  end

  def celebrate_birthday
    puts "Happy Birthday!"
    self.age += 1
  end
end

dan = User.new('Dan', 'dan@coderdan.co', 34)
puts "I'm #{dan.age}"
dan.celebrate_birthday
puts "Doh! Now I'm #{dan.age}"

