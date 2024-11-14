require 'gosu'

WIDTH = 1024
HEIGHT = 768

CARD_SCALE = 0.6
CARD_WIDTH = 140 * CARD_SCALE
CARD_HEIGHT = 190 * CARD_SCALE

class Card
  attr_accessor :suit, :value, :face_up

  def initialize(suit, value, image_path)
    @suit = suit
    @value = value
    @face_up = false
    @image = Gosu::Image.new(image_path)
    @x = 0
    @y = 0
  end

  def draw
    if @face_up
      @image.draw(@x, @y, 1)
    else
      # Draw face-down image
    end
  end

  def face_up
    @face_up = true
  end

  def face_down
    @face_up = false
  end
end

class CardGame < Gosu::Window
  def initialize
    super(WIDTH, HEIGHT)
    self.caption = "Drag and Drop Cards"
    @cards = [] # Store your card objects here
    @dragging = nil
  end

  def load_images
    # Load card images and create Card objects
    CARD_SUITS.each do |suit|
      CARD_VALUES.each do |value|
        image_path = "path_to_card_image"  # Replace with actual image path
        card = Card.new(suit, value, image_path)
        @cards << card
      end
    end
  end

  def draw
    @cards.each(&:draw)
  end

  def update
    # Update logic here
  end

  def button_down(id)
    if id == Gosu::MsLeft
      x, y = mouse_x, mouse_y
      @cards.reverse_each do |card|
        if card.face_up && card_contains_point?(card, x, y)
          @dragging = card
          break
        end
      end
    end
  end

  def button_up(id)
    if id == Gosu::MsLeft && @dragging
      x, y = mouse_x, mouse_y
      # Check if the mouse is released over a valid drop zone
      # Update the card's position accordingly
      @dragging = nil
    end
  end

  def card_contains_point?(card, x, y)
    x >= card.x && x <= card.x + CARD_WIDTH &&
      y >= card.y && y <= card.y + CARD_HEIGHT
  end

  def needs_cursor?
    true
  end
end

CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]

window = CardGame.new
window.load_images
window.show
