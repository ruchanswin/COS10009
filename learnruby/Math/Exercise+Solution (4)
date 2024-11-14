def add(a, b)
  display(a + b)
end

def divide(a, b)
  display(a / b)
end

def subtract(a, b)
  display(a - b)
end

def multiply(a, b)
  display(a * b)
end

def power(a, b)
  display(a ** b)
end

def display(result)
  puts sprintf("%.2f", result)
end

puts "Welcome to calculator"
puts "What is the first operand?"
op_a = gets.chomp.to_f

puts "What is the second operand?"
op_b = gets.chomp.to_f

puts "What operator would you like to use?"
operator = gets.chomp

add(op_a, op_b) if operator == 'add'
subtract(op_a, op_b) if operator == 'subtract'
multiply(op_a, op_b) if operator == 'multiply'
power(op_a, op_b) if operator == 'power'
divide(op_a, op_b) if operator == 'divide'
