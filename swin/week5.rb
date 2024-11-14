def read_list
    list = []
    index = 0
    count = 10
    while (index < count)
      puts "Please enter an element: "
      list << gets
      puts "added: " + list [index]
      index += 1
    end
end

def print_elements list
    index = 0
    puts "Printing list:"
    while (index < list.size)
       puts "#{index} element is: " + list [ins
       index +=1
    end
end

def main
    list = read_list()
    print_elements(list)
end

main