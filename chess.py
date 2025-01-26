# given a board state that the user enters, with 1 white figure and up to 16 black figures, which black figures can the white figure take?


# 1. ask the user for input -> white pieces, only two choices and the user should be informed about that, format knight a5
# 2. ask to enter black pieces, same format, 1 - 16 pieces, after at least one piece added, user can write "done" -> check if done is written too early (<1 black piece)
# 3. after 16 pieces -> confirmation or error message if two pieces in same coordinates
# 4. print what black pieces if any, white piece can take


def main():
   
   # Get initial board state
   board_state = get_new_board_state()
   
   # Ask for the white piece and its position
   white_piece = ask_for_user_white_piece_input()
   board_state = update_board_state(board_state, white_piece)
   
   # Ask for black pieces and their positions
   black_pieces = ask_for_user_black_pieces_input(board_state, white_piece)
   
   # List black pieces that can be taken
   capturable_pieces = find_capturable_pieces(white_piece, black_pieces)

   if capturable_pieces:
    print("\nThe white piece can capture the following black pieces:")
    for piece in capturable_pieces:
            black_piece_type, black_column, black_row = piece  # Unpack black piece details
            black_row_indexed = black_row
            position = black_column + str(black_row_indexed)  # Correctly format the position output
            full_piece_name = black_piece_type.capitalize()  # Get the name of the piece
            print(f"Piece: {full_piece_name} at position: {position}")
   else:
       print("The white piece cannot capture any black pieces.")
  

def get_new_board_state():
  return [[" ", " ", " ", " ", " ", " ", " ", " "],
          [" ", " ", " ", " ", " ", " ", " ", " "],
          [" ", " ", " ", " ", " ", " ", " ", " "],
          [" ", " ", " ", " ", " ", " ", " ", " "],
          [" ", " ", " ", " ", " ", " ", " ", " "],
          [" ", " ", " ", " ", " ", " ", " ", " "],
          [" ", " ", " ", " ", " ", " ", " ", " "],
          [" ", " ", " ", " ", " ", " ", " ", " "]]

def ask_for_user_white_piece_input():

  asking = True
  while asking:
    user_input = input("Enter where to place a white piece (pawn or rook) on the board in the format 'piece x0': ").strip().lower()

    # Spliting the input for the format check
    parts = user_input.split()

    # Check for the format
    if len(parts) != 2:
        print("Invalid format. Write in the format 'piece x0'.")
        continue

    # Split the input into words
    piece, position = user_input.split()
    
    # Validate piece type
    if piece not in ["pawn", "rook"]:
        print("Invalid piece. Choose either 'pawn' or 'rook'.")
        continue

    # Extract x and y coordinates
    x = position[0]
    y = int(position[1])

    # Validate coordinate
    if x not in ["a", "b", "c", "d", "e", "f", "g", "h"] or not (1 <= y <= 8):
        print("Invalid coordinate. Choose coordinates between a1 and h8.")
        continue
    
    return [piece, x, 8 - y]

def ask_for_user_black_pieces_input(board_state, white_piece):

# Black pieces moves storage
  black_pieces = []

# Counters for each piece type
  piece_count = {
    "pawn": 0,
    "rook": 0,
    "king": 0,
    "queen": 0,
    "bishop": 0,
    "knight": 0
  }

  while True:
    user_input = input(
       "Enter where to place a black piece (king, queen, bishop, knight, rook, or pawn) "
            "on the board in the format 'piece x0'. Type 'done' to finish: "
       ).strip().lower()

    # Allow the user to finish adding pieces
    if user_input == "done":
        if black_pieces:
            return black_pieces # Stop if at least one black piece has been added
        else:
            print("You must add at least one black piece before typing 'done'.")
            continue
    
    # Spliting the input for the format check
    parts = user_input.split()

    # Check for the format
    if len(parts) != 2:
        print("Invalid format. Write in the format 'piece x0'.")
        continue

    # Split the input into words
    piece, position = user_input.split()
    
    # Validate piece type
    if piece not in piece_count:
        print("Invalid piece. Choose 'king', 'queen', 'bishop', 'knight', 'pawn' or 'rook'.")
        continue
    
    # Check how many pieces user enters
    if piece == "pawn":
        if piece_count["pawn"] >= 8:
            print("You cannot add more than 8 pawns.")
            continue
    elif piece in ["rook", "knight", "bishop"]:
        if piece_count[piece] >= 2:
            print(f"You cannot add more than 2 {piece}s.")
            continue
    elif piece in ["king", "queen"]:
        if piece_count[piece] >= 1:
            print(f"You cannot add more than 1 {piece}.")
            continue

    # Extract x and y coordinates
    x = position[0]
    y = int(position[1])

    # Validate coordinate
    if x not in ["a", "b", "c", "d", "e", "f", "g", "h"] or not (1 <= y <= 8):
        print("Invalid coordinate. Choose coordinates between a1 and h8.")
        continue

    # Convert the coordinates for comparison with board state
    column_mapping = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    column_index = column_mapping[x]
    row_index = 8 - y

    # Check if the position is already occupied by the white piece
    if [column_index, row_index] == [column_mapping[white_piece[1]], white_piece[2]]:
        print("Invalid move. The white piece is already on that square!")
        continue

    # Check if the position is already occupied by black pieces
    for bp in black_pieces:  # Look at each piece in the list of black pieces
        if bp[1] == x and bp[2] == 8 - y:  # If the x and y of the new piece match any existing piece
            print("Invalid move. There's already a piece there!")
            break
    else:    
        black_pieces.append([piece, x, row_index])
        piece_count[piece] += 1 # Add one to the current count
        print(f"Black piece {piece} at {x}{y} added successfully.")


    # When there 16 black pieces - stop
    if len(black_pieces) == 16:
        print("You have added the maximum number of black pieces (16).")
        return black_pieces
    

def update_board_state(board_state, move):
  # Extract the piece name, column letter, and row number from the move
    piece = move[0]  
    column = move[1]  
    row = move[2]

    # Convert the column letter (a-h) to a number index (0-7)
    column_mapping = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    column_index = column_mapping[column]

    # Place the piece on the board
    board_state[row][column_index] = piece

    return board_state

def find_capturable_pieces(white_piece, black_pieces):

    capturable = []  # This list will hold all the black pieces that can be captured
    
    piece_type, column, row = white_piece

    # Convert the column letter (a-h) to a number index (0-7)
    column_mapping = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    column_index = column_mapping[column]

    # Loop through each black piece to check if it can be captured
    for black_piece in black_pieces:
        black_piece_type, black_column, black_row = black_piece
    
        # Convert the column letter (a-h) to a number index (0-7)
        black_column_index = column_mapping[black_column]

        # Black row is already indexed
        black_row_index = black_row 

        # Check if the white piece can capture the black piece based on its type
        if piece_type == "rook":
            # Rooks can move in straight lines
            if row == black_row_index or column_index == black_column_index:
                capturable.append(black_piece)  # Add to capturable list
        elif piece_type == "pawn":
            # Pawns can only capture diagonally and must move forward
            # For a white pawn, it can capture a black piece if the black piece is on a higher row
            if row - 1 == black_row_index and abs(column_index - black_column_index) == 1:
                capturable.append(black_piece)  # Add to capturable list

    return capturable

if __name__ == "__main__":
    main()


# 8
# 7
# 6
# 5
# 4
# 3
# 2
# 1
#   a b c d e f g h