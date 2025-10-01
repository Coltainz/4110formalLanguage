print("Hello, formal language project!")

def is_in_language (s):
    if len(s) == 0:
        return False
    
    for ch in s:
        if ch not in ("a", "b"):
            return False
    
    i = 0
    n = len(s)
    while i < n and s[i] == 'a':
        i+=1
    
    count_a = i

    if count_a == 0:
        return False
    
    while i < n and s[i] == 'b':
        i+=1

    count_b = n - count_a

    if i != n:
        return False
    
    if count_b != count_a:
        return False
    
    return True



def kleene_closure_generator(base_language, max_length):

    #checks if w is string and then puts it into set, which will also get rid of duplicates
    is_base_language = set()
    for w in base_language:
        if isinstance(w, str):
            is_base_language.add(w)

    correct_length = set()
    for w in is_base_language:
        if len(w) > 0 and len(w) <= max_length:
            correct_length.add(w)


    # Create a list of sets. 
    # Each index will store all strings we can build of that length.
    combinations_by_length = []  

    # Fill the list with empty sets for every possible length from 0 up to max_length
    for length_index in range(max_length + 1):       # 0,1,2,...max_length
        combinations_by_length.append(set())         # make an empty set for each length

    # Base case: for length 0 we can always make the empty string
    combinations_by_length[0].add("")                # start with an empty string of length 0


    # Outer loop: build strings for every target length from 1 up to max_length
    for target_length in range(1, max_length + 1):

    # Check every allowed word piece
        for word_piece in correct_length:

    # How long is this word piece?
            piece_length = len(word_piece)

    # Only proceed if the piece fits into the current target length
            if piece_length <= target_length:

    # Figure out how much length is left before adding this piece.
    # We will extend all existing strings of this leftover length.
                leftover_length = target_length - piece_length

    # Look at every string we already know how to make of leftover_length
                for existing_string in combinations_by_length[leftover_length]:

    # Create a new string by adding the word_piece to the end
                    new_string = existing_string + word_piece

    # Store that new string in the bucket for the current target length
                    combinations_by_length[target_length].add(new_string)



#so basically it gets a target length, then figures out how much room we have to work with length wise by seeing how long this current piece is that we are looking at,
#then if lets say theres 3 spots left (piece length is 5 and target length is 8) then it'll grab everything from the array group spot that is of length 3, (cuz spot 3 in the array is all the stuff that is of length 3)
#and then add each of those onto the end?(might not be the end but it adds it onto them) to create a new word, that will fit in that target length we need, by using 
#whatever piece we are looking at. 



def generate_recursive_language_M(n):
    """
    n = 0 -> "x"
    n > 0 -> "y" + M(n-1) + "z"
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return "x"
    return "y" + generate_recursive_language_M(n - 1) + "z"

