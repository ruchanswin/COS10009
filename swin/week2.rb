def get_user_name (prompt)
    puts prompt
    name = gets
    return name
end

def print_user_name (prompt, user_name)
    puts prompt
    puts user_name
    return user_name, display_prompt
end


def main
    prompt = 'Enter your name: '
    display_prompt = 'The user name entered was:'

    user_name = get_user_name(prompt)
    print_user_name(display_prompt, user_name)
end

main()