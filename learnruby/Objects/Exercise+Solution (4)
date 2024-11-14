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

  def to_s
    "#{self.name}"
  end

  def inspect
    "[#{name}, #{email}, #{age}]"
  end
end

user = User.new('Elvis', 'elvis@presley.com', 55)
puts user
p user
