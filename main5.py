import streamlit as st
import time

# Constants for the Wordle game
WORD = 'PAKIS'
MAX_ATTEMPTS = 6
WORD_LENGTH = 5

# Function to check the guess and return feedback
def check_guess(guess, word):
    feedback = ['⬛'] * len(guess)  # Default to incorrect (grey)
    word_chars = list(word)

    # Check for correct letters in correct positions (green)
    for i in range(len(guess)):
        if guess[i] == word[i]:
            feedback[i] = '🟩'
            word_chars[i] = None  # Mark the character as used

    # Check for correct letters in wrong positions (yellow)
    for i in range(len(guess)):
        if feedback[i] == '⬛' and guess[i] in word_chars:
            feedback[i] = '🟨'
            # Remove the first occurrence of the letter in word_chars
            word_chars[word_chars.index(guess[i])] = None

    return feedback

# Initialize session state variables
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'guesses' not in st.session_state:
    st.session_state.guesses = [''] * MAX_ATTEMPTS
if 'feedback' not in st.session_state:
    st.session_state.feedback = [['⬛'] * WORD_LENGTH for _ in range(MAX_ATTEMPTS)]
if 'current_guess' not in st.session_state:
    st.session_state.current_guess = ''
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'used_letters' not in st.session_state:
    st.session_state.used_letters = {}  # To store the status of each letter: 'green', 'yellow', 'grey'
if 'game_complete' not in st.session_state:
    st.session_state.game_complete = False

# Function to handle letter input dynamically
def add_letter(letter):
    if len(st.session_state.current_guess) < WORD_LENGTH:
        st.session_state.current_guess += letter

# Function to handle deletion of a letter
def delete_letter():
    st.session_state.current_guess = st.session_state.current_guess[:-1]

# Function to update the feedback and keyboard after the guess is submitted
def submit_guess():
    current_guess = st.session_state.current_guess
    attempt = st.session_state.attempts

    # Update the current guess and feedback
    st.session_state.guesses[attempt] = current_guess
    feedback = check_guess(current_guess, WORD)
    st.session_state.feedback[attempt] = feedback

    # Update keyboard status
    for idx, letter in enumerate(current_guess):
        if feedback[idx] == '🟩':
            st.session_state.used_letters[letter] = 'green'
        elif feedback[idx] == '🟨' and letter not in st.session_state.used_letters:
            st.session_state.used_letters[letter] = '#FFF176'  # Light yellow
        elif feedback[idx] == '⬛':
            st.session_state.used_letters[letter] = 'grey'

    # Increment the attempts and reset the current guess
    st.session_state.attempts += 1
    st.session_state.current_guess = ''

    # Mark the game as complete if the word is guessed or max attempts are reached
    if current_guess == WORD or st.session_state.attempts == MAX_ATTEMPTS:
        end_time = time.time()
        time_taken = end_time - st.session_state.start_time

        if current_guess == WORD:
            st.balloons()  # Add balloons as a celebratory effect
            st.session_state.congratulations_message = f"Congratulations, {user_name}! You've guessed the word '{WORD}' in {st.session_state.attempts} attempts and it took you {time_taken:.2f} seconds!"
        else:
            st.session_state.congratulations_message = f"Sorry, {user_name}. You've used all your attempts. The word was '{WORD}'."

        # Mark the game as complete
        st.session_state.game_complete = True

# Start of the Streamlit app
st.title('Wordle Game - Guess the Word!')

# User login
user_name = st.text_input('Enter your name to start:', '')

if user_name:
    st.write(f"Welcome, {user_name}!")

    # Grid display
    st.write("Your guesses:")
    for i in range(MAX_ATTEMPTS):
        row = st.columns(WORD_LENGTH, gap="small")  # Create a row with fixed columns for uniform spacing
        for j in range(WORD_LENGTH):
            if i < st.session_state.attempts:
                # Display feedback for past guesses
                letter = st.session_state.guesses[i][j]
                color = 'green' if st.session_state.feedback[i][j] == '🟩' else '#FFF176' if st.session_state.feedback[i][j] == '🟨' else 'grey'
                row[j].markdown(f"""
                    <div style='
                        text-align:center; 
                        font-size:40px; 
                        background-color: {color}; 
                        color: black; 
                        width: 60px; 
                        height: 60px; 
                        display: flex; 
                        align-items: center; 
                        justify-content: center; 
                        border-radius: 5px;'>
                        {letter}
                    </div>
                    """, unsafe_allow_html=True)
            elif i == st.session_state.attempts and j < len(st.session_state.current_guess):
                # Display the current guess being typed
                letter = st.session_state.current_guess[j]
                row[j].markdown(f"""
                    <div style='
                        text-align:center; 
                        font-size:40px; 
                        width: 60px; 
                        height: 60px; 
                        display: flex; 
                        align-items: center; 
                        justify-content: center; 
                        border: 2px solid #ccc; 
                        border-radius: 5px;'>
                        {letter}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                # Empty cells with consistent size
                row[j].markdown(f"""
                    <div style='
                        text-align:center; 
                        font-size:40px; 
                        width: 60px; 
                        height: 60px; 
                        display: flex; 
                        align-items: center; 
                        justify-content: center; 
                        border: 2px solid #ccc; 
                        border-radius: 5px;'>
                    </div>
                    """, unsafe_allow_html=True)

    if not st.session_state.game_complete:
        # Keyboard buttons
        st.write("Keyboard:")
        keyboard = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
        ]

        for row in keyboard:
            cols = st.columns(len(row))
            for idx, letter in enumerate(row):
                button_color = 'lightgrey' if letter not in st.session_state.used_letters else st.session_state.used_letters[letter]
                cols[idx].button(letter, key=letter, on_click=add_letter, args=(letter,), disabled=(st.session_state.used_letters.get(letter) == 'grey'))

        # Delete button
        st.button("Delete", on_click=delete_letter)

        # Submit guess button
        st.button("Submit Guess", on_click=submit_guess)

    # Keep the congratulations or error message visible
    if st.session_state.game_complete:
        if 'congratulations_message' in st.session_state:
            st.write(st.session_state.congratulations_message)

    # Keep the grid and feedback visible
    st.write("Your final guesses:")
    for i in range(MAX_ATTEMPTS):
        row = st.columns(WORD_LENGTH, gap="small")
        for j in range(WORD_LENGTH):
            if i < st.session_state.attempts:
                # Display feedback for past guesses
                letter = st.session_state.guesses[i][j]
                color = 'green' if st.session_state.feedback[i][j] == '🟩' else '#FFF176' if st.session_state.feedback[i][j] == '🟨' else 'grey'
                row[j].markdown(f"""
                    <div style='
                        text-align:center; 
                        font-size:40px; 
                        background-color: {color}; 
                        color: black; 
                        width: 60px; 
                        height: 60px; 
                        display: flex; 
                        align-items: center; 
                        justify-content: center; 
                        border-radius: 5px;'>
                        {letter}
                    </div>
                    """, unsafe_allow_html=True)

