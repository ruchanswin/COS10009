
# Version 1
def included?(range, number)
  number >= range.begin && number <= range.end
end

puts "\nVersion 1"
puts included?(1.3..2.0, 1.4)

def included2?(range, number)
  if range.exclude_end?
    number >= range.begin && number < range.end
  else
    number >= range.begin && number <= range.end
  end
end

puts "\nVersion 2"
puts included2?(1.3..2.0, 1.4)
puts included2?(1.3...2.0, 2.0)

def included3?(range, number)
  range.cover?(number)
end

puts "\nVersion 3"
puts included3?(1.3..2.0, 1.4)
