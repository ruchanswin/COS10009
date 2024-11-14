"""
Solitaire clone.
"""
from typing import Optional

import random
import arcade
import time
import pyglet

# Screen title and size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Solitaire"

# Constants for sizing
CARD_SCALE = 0.6

# How big are the cards?
CARD_WIDTH = 140 * CARD_SCALE
CARD_HEIGHT = 190 * CARD_SCALE

# How big is the mat we'll place the card on?
MAT_PERCENT_OVERSIZE = 1.25
MAT_HEIGHT = int(CARD_HEIGHT * MAT_PERCENT_OVERSIZE)
MAT_WIDTH = int(CARD_WIDTH * MAT_PERCENT_OVERSIZE)

# How much space do we leave as a gap between the mats?
# Done as a percent of the mat size.
VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10

# The Y of the bottom row (2 piles)
BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The X of where to start putting things on the left side
START_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# The Y of the top row (4 piles)
TOP_Y = SCREEN_HEIGHT - MAT_HEIGHT / 2 - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The Y of the middle row (7 piles)
MIDDLE_Y = TOP_Y - MAT_HEIGHT - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# How far apart each pile goes
X_SPACING = MAT_WIDTH + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# Card constants
CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]

# If we fan our cards stacked on each other, how far apart to fan them?
CARD_VERTICAL_OFFSET = CARD_HEIGHT * CARD_SCALE * 0.3

# Face down image
FACE_DOWN_IMAGE = ":resources:images/cards/cardBack_red2.png"

# Constants that represent "what pile is what" for the game
PILE_COUNT = 13
BOTTOM_FACE_DOWN_PILE = 0
BOTTOM_FACE_UP_PILE = 1
PLAY_PILE_1 = 2
PLAY_PILE_2 = 3
PLAY_PILE_3 = 4
PLAY_PILE_4 = 5
PLAY_PILE_5 = 6
PLAY_PILE_6 = 7
PLAY_PILE_7 = 8
TOP_PILE_1 = 9
TOP_PILE_2 = 10
TOP_PILE_3 = 11
TOP_PILE_4 = 12


class Card(arcade.Sprite):
    """ Card sprite """

    def __init__(self, suit, value, scale=1):
        """ Card constructor """

        # Attributes for suit and value
        self.suit = suit
        self.value = value

        # Image to use for the sprite when face up
        self.image_file_name = f":resources:images/cards/card{self.suit}{self.value}.png"
        self.is_face_up = False
        super().__init__(FACE_DOWN_IMAGE, scale, hit_box_algorithm="None")

    def is_black(self):
        return self.suit in ["Spades", "Clubs"]

    def is_red(self):
        return self.suit in ["Hearts", "Diamonds"]

    def face_down(self):
        """ Turn card face-down """
        self.texture = arcade.load_texture(FACE_DOWN_IMAGE)
        self.is_face_up = False

    def face_up(self):
        """ Turn card face-up """
        self.texture = arcade.load_texture(self.image_file_name)
        self.is_face_up = True

    @property
    def is_face_down(self):
        """ Is this card face down? """
        return not self.is_face_up


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list: Optional[arcade.SpriteList] = None

        self.background_color = arcade.color.AMAZON
        self.random_color = False

        # List of cards we are dragging with the mouse
        self.held_cards = None

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = None

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list = None

        # Create a list of lists, each holds a pile of cards.
        self.piles = None

        # Initialize the main game timer
        self.start_time = time.time()
        self.elapsed_time = 0

        # Define time limits for different timers
        self.default_time_limit_1 = 600  # Default timer limit (e.g., 10 minutes)

        # Variable to track if the player has won the game
        self.has_won = False

        # Variable to track if the player has lost
        self.has_lost = False

        # Load the first background music track
        self.background_music_tracks = ["musics/red.mp3", "musics/blue.mp3", "musics/bys.mp3", "musics/red.mp3",
                                        "musics/22.mp3", "musics/die_for_you.mp3", "musics/dissolve.mp3",
                                        "musics/drunk.mp3", "musics/glimpse_of_us.mp3", "musics/just_friend.mp3",
                                        "musics/starlight.mp3", "musics/start_music.mp3", "musics/what_am_i.mp3"]
        self.current_track_index = 0
        self.background_music_player = None

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # List of cards we are dragging with the mouse
        self.held_cards = []

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = []

        # ---  Create the mats the cards go on.

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        # Create the mats for the bottom face down and face up piles
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = START_X, BOTTOM_Y
        self.pile_mat_list.append(pile)

        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = START_X + X_SPACING, BOTTOM_Y
        self.pile_mat_list.append(pile)

        # Create the seven middle piles
        for i in range(7):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_X + i * X_SPACING, MIDDLE_Y
            self.pile_mat_list.append(pile)

        # Create the top "play" piles
        for i in range(4):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_X + i * X_SPACING, TOP_Y
            self.pile_mat_list.append(pile)

        # --- Create, shuffle, and deal the cards

        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list = arcade.SpriteList()

        # Create every card
        for card_suit in CARD_SUITS:
            for card_value in CARD_VALUES:
                card = Card(card_suit, card_value, CARD_SCALE)
                card.position = START_X, BOTTOM_Y
                self.card_list.append(card)

        # Shuffle the cards
        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list.swap(pos1, pos2)

        # Create a list of lists, each holds a pile of cards.
        self.piles = [[] for _ in range(PILE_COUNT)]

        # Put all the cards in the bottom face-down pile
        for card in self.card_list:
            self.piles[BOTTOM_FACE_DOWN_PILE].append(card)

        # - Pull from that pile into the middle piles, all face-down
        # Loop for each pile
        for pile_no in range(PLAY_PILE_1, PLAY_PILE_7 + 1):
            # Deal proper number of cards for that pile
            for j in range(pile_no - PLAY_PILE_1 + 1):
                # Pop the card off the deck we are dealing from
                card = self.piles[BOTTOM_FACE_DOWN_PILE].pop()
                # Put in the proper pile
                self.piles[pile_no].append(card)
                # Move card to same position as pile we just put it in
                card.position = self.pile_mat_list[pile_no].position
                # Put on top in draw order
                self.pull_to_top(card)

        # Flip up the top cards
        for i in range(PLAY_PILE_1, PLAY_PILE_7 + 1):
            self.piles[i][-1].face_up()

        # Start playing the first track
        self.play_track(self.current_track_index)

    def play_track(self, track_index):
        if self.background_music_player:
            self.background_music_player.delete()

        # Load and play the track, with looping behavior
        track = pyglet.media.load(self.background_music_tracks[track_index], streaming=False)
        self.background_music_player = pyglet.media.Player()
        self.background_music_player.queue(track)
        self.background_music_player.loop = True  # Set looping behavior
        self.background_music_player.play()

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        # Draw the mats the cards go on to
        self.pile_mat_list.draw()

        # Draw the cards
        self.card_list.draw()

        # Check if the player has won or lost and display the message
        if self.has_won:
            arcade.draw_text("You won the game!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, arcade.color.BLACK, 36,
                             anchor_x="center")
        elif self.has_lost:
            arcade.draw_text("You ran out of time and lost!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, arcade.color.BLACK,
                             36,
                             anchor_x="center")

        if self.default_time_limit_1:
            # Display the remaining time in the top-right corner
            remaining_time = max(0, self.default_time_limit_1 - int(self.elapsed_time))
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            time_text = f"Time: {minutes:02}:{seconds:02}"
            arcade.draw_text(time_text, SCREEN_WIDTH - 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 18, anchor_x="right")

        arcade.draw_text("'R': restart the game, 'Space': skip the music", SCREEN_WIDTH - 5, SCREEN_HEIGHT - 720,
                         arcade.color.WHITE, 18, anchor_x="right")
        arcade.draw_text("'D': turn on/off music, 'C': change background color", SCREEN_WIDTH - 5,
                         SCREEN_HEIGHT - 750, arcade.color.WHITE, 18, anchor_x="right")

    def pull_to_top(self, card: arcade.Sprite):
        """ Pull card to top of rendering order (last to render, looks on-top) """

        # Remove, and append to the end
        self.card_list.remove(card)
        self.card_list.append(card)

    def on_key_press(self, symbol: int, modifiers: int):
        """ User presses key """
        if symbol == arcade.key.R:
            # Restart
            self.setup()
            # Restart the selected timer
            self.start_time = time.time()
        if symbol == arcade.key.SPACE:
            # Skip to the next track when the space bar is pressed
            self.current_track_index = (self.current_track_index + 1) % len(self.background_music_tracks)
            self.play_track(self.current_track_index)
        if symbol == arcade.key.C:
            # Change the background color to a random color
            self.background_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if symbol == arcade.key.D:
            # Toggle background music on/off when the "D" key is pressed
            if self.background_music_player:
                if self.background_music_player.playing:
                    self.background_music_player.pause()
                else:
                    self.background_music_player.play()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """

        # Get list of cards we've clicked on
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        # Have we clicked on a card?
        if len(cards) > 0:

            # Might be a stack of cards, get the top one
            primary_card = cards[-1]
            assert isinstance(primary_card, Card)

            # Figure out what pile the card is in
            pile_index = self.get_pile_for_card(primary_card)

            # Are we clicking on the bottom deck, to flip three cards?
            if pile_index == BOTTOM_FACE_DOWN_PILE:
                # Flip three cards
                for i in range(3):
                    # If we ran out of cards, stop
                    if len(self.piles[BOTTOM_FACE_DOWN_PILE]) == 0:
                        break
                    # Get top card
                    card = self.piles[BOTTOM_FACE_DOWN_PILE][-1]
                    # Flip face up
                    card.face_up()
                    # Move card position to bottom-right face up pile
                    card.position = self.pile_mat_list[BOTTOM_FACE_UP_PILE].position
                    # Remove card from face down pile
                    self.piles[BOTTOM_FACE_DOWN_PILE].remove(card)
                    # Move card to face up list
                    self.piles[BOTTOM_FACE_UP_PILE].append(card)
                    # Put on top draw-order wise
                    self.pull_to_top(card)

            elif primary_card.is_face_down:
                # Is the card face down? In one of those middle 7 piles? Then flip up
                primary_card.face_up()
            else:
                # All other cases, grab the face-up card we are clicking on
                self.held_cards = [primary_card]
                # Save the position
                self.held_cards_original_position = [self.held_cards[0].position]
                # Put on top in drawing order
                self.pull_to_top(self.held_cards[0])

                # Is this a stack of cards? If so, grab the other cards too
                card_index = self.piles[pile_index].index(primary_card)
                for i in range(card_index + 1, len(self.piles[pile_index])):
                    card = self.piles[pile_index][i]
                    self.held_cards.append(card)
                    self.held_cards_original_position.append(card.position)
                    self.pull_to_top(card)

        else:
            # Click on a mat instead of a card?
            mats = arcade.get_sprites_at_point((x, y), self.pile_mat_list)

            if len(mats) > 0:
                mat = mats[0]
                mat_index = self.pile_mat_list.index(mat)

                # Is it our turned over flip mat? and no cards on it?
                if mat_index == BOTTOM_FACE_DOWN_PILE and len(self.piles[BOTTOM_FACE_DOWN_PILE]) == 0:
                    # Flip the deck back over so we can restart
                    temp_list = self.piles[BOTTOM_FACE_UP_PILE].copy()
                    for card in reversed(temp_list):
                        card.face_down()
                        self.piles[BOTTOM_FACE_UP_PILE].remove(card)
                        self.piles[BOTTOM_FACE_DOWN_PILE].append(card)
                        card.position = self.pile_mat_list[BOTTOM_FACE_DOWN_PILE].position

    def remove_card_from_pile(self, card):
        """ Remove card from whatever pile it was in. """
        for pile in self.piles:
            if card in pile:
                pile.remove(card)
                break

    def get_pile_for_card(self, card):
        """ What pile is this card in? """
        for index, pile in enumerate(self.piles):
            if card in pile:
                return index

    def move_card_to_new_pile(self, card, pile_index):
        """ Move the card to a new pile """
        self.remove_card_from_pile(card)
        self.piles[pile_index].append(card)

    @staticmethod
    def check_valid_tableau_sequence(pile):
        """
        Check if the tableau pile has a valid sequence
        """
        if len(pile) >= 2:
            valid_sequence = True
            for i in range(1, len(pile)):
                current_card = pile[i]
                previous_card = pile[i - 1]
                if (
                        CARD_VALUES.index(current_card.value) >= CARD_VALUES.index(previous_card.value)
                        or current_card.suit != previous_card.suit
                ):
                    valid_sequence = False
                    break
            if valid_sequence:
                return True
        return False

    @staticmethod
    def check_valid_foundation_sequence(pile):
        """
        Check if the foundation pile has a valid sequence
        """
        if len(pile) == 13:
            suit = pile[0].suit
            valid_sequence = True
            for i, card in enumerate(pile):
                if (
                        card.suit != suit
                        or card.value != CARD_VALUES[i]
                ):
                    valid_sequence = False
                    break
            if valid_sequence:
                return True
        return False

    def check_win_condition(self):
        # Check if all foundation piles have cards with the same suit
        suits = set(card.suit for card in self.piles[TOP_PILE_1])
        if len(suits) == 1:
            # Check if all foundation piles have cards in ascending order
            for pile in range(TOP_PILE_1, TOP_PILE_4 + 1):
                if not self.check_valid_foundation_sequence(self.piles[pile]):
                    return False
            return True
        return False

    def on_update(self, delta_time):
        # Update the main game timer
        self.elapsed_time = time.time() - self.start_time

        # Check if the main game timer has exceeded its time limit
        if self.elapsed_time >= self.default_time_limit_1:
            self.has_lost = True

        # Check if the win condition is met
        if self.check_win_condition():
            self.has_won = True
            self.on_draw()  # Call on_draw to display the winning message

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """ Called when the user presses a mouse button. """

        # If we don't have any cards, who cares
        if len(self.held_cards) == 0:
            return

        # Find the closest pile, in case we are in contact with more than one
        pile, distance = arcade.get_closest_sprite(self.held_cards[0], self.pile_mat_list)
        reset_position = True

        # See if we are in contact with the closest pile
        if arcade.check_for_collision(self.held_cards[0], pile):

            # What pile is it?
            pile_index = self.pile_mat_list.index(pile)

            #  Is it the same pile we came from?
            if pile_index == self.get_pile_for_card(self.held_cards[0]):
                # If so, who cares. We'll just reset our position.
                pass

            # Is it on a middle play pile?
            elif PLAY_PILE_1 <= pile_index <= PLAY_PILE_7:
                # Are there already cards there?
                if len(self.piles[pile_index]) > 0:
                    # Move cards to proper position
                    top_card = self.piles[pile_index][-1]
                    for i, dropped_card in enumerate(self.held_cards):
                        dropped_card.position = top_card.center_x, \
                            top_card.center_y - CARD_VERTICAL_OFFSET * (i + 1)
                else:
                    # Are there no cards in the middle play pile?
                    for i, dropped_card in enumerate(self.held_cards):
                        # Move cards to proper position
                        dropped_card.position = pile.center_x, \
                            pile.center_y - CARD_VERTICAL_OFFSET * i

                for card in self.held_cards:
                    # Cards are in the right position, but we need to move them to the right list
                    self.move_card_to_new_pile(card, pile_index)

                # Success, don't reset position of cards
                reset_position = False

            # Release on top play pile? And only one card held?
            elif TOP_PILE_1 <= pile_index <= TOP_PILE_4 and len(self.held_cards) == 1:
                # Move position of card to pile
                self.held_cards[0].position = pile.position
                # Move card to card list
                for card in self.held_cards:
                    self.move_card_to_new_pile(card, pile_index)

                reset_position = False

        if reset_position:
            # Where-ever we were dropped, it wasn't valid. Reset each card's position
            # to its original spot.
            for pile_index, card in enumerate(self.held_cards):
                card.position = self.held_cards_original_position[pile_index]

        # We are no longer holding cards
        self.held_cards = []

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """

        # If we are holding cards, move them with the mouse
        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy


def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
