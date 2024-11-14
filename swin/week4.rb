def read_user_name (prompt)
    puts prompt
    name = gets
    return name
end

def read_user_age(prompt, user_age)
    puts prompt
    age = gets.to_i

    while (age < 1 || age > 120)
        puts "Incorrect age entered, please re-entered: "
    end
    return age
    
    #Another way
    #begin 
        #puts prompt
        #age = gets.to_i
    #end while (age < 1 || age > 120)
    #return age
end

def print_user_name (prompt, user_name)
    puts prompt
    puts user_name
end

def main
    prompt = "Please enter user name: "
    display_prompt = "The user name entered was:

    user_name = read_user_name(prompt)
    user_age = read_user_age("Please enter the user's age: ")

    print_user_name(display_prompt, user_name)
    print_user_age("The user age was: ", user_age)
end

main