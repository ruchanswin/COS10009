def read_user_name (prompt)
    puts prompt
    name = gets
    return name
end

def read_user_age(prompt, user_age)
    puts prompt
    puts user_age

    case user_age
    when 1..24
      puts "The user is quite young"
    when 25..35
      puts "The user is not-so-young"
    when 36..46
      puts "The user is really not-so-young"
    else 
      puts "The user is either under 1 or over 46"
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