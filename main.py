print("Hello, formal language project!")

def is_in_language_L(s):
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



# Collect everything of length 0..max_length into one set to return
    result_set = set()

    # Add every string from each length bucket
    length_index = 0
    while length_index <= max_length:
        for s in combinations_by_length[length_index]:
            result_set.add(s)
        length_index += 1

    return result_set


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











def regex_match(pattern, string):
    """
    Check if 'string' matches the given regular expression 'pattern'
    Supported: concatenation, union (|), Kleene star (*), and optional parentheses ().
    Examples:
        regex_match("a*", "aaa") -> True
        regex_match("a*b", "aab") -> True
        regex_match("a|b", "a") -> True
        regex_match("a|b", "c") -> False
        regex_match("(ab)*|c", "abab") -> True
    """

    # --------------------------
    # 1) Quick checks for edge cases
    # --------------------------
    if not isinstance(pattern, str) or not isinstance(string, str):
        raise TypeError("Both pattern and string must be strings.")

    # Empty pattern matches only empty string
    if pattern == "":
        return string == ""

    # --------------------------
    # 2) PARSER: build a tiny AST for the regex
    # Grammar (with precedence):
    #   regex       := union
    #   union       := concat ('|' concat)*
    #   concat      := repeat+
    #   repeat      := base ('*')*
    #   base        := literal | '(' regex ')'
    #
    # Precedence (highest to lowest): * , concatenation , |
    # --------------------------

    # We'll walk through the pattern using a simple index.
    parse_index = 0

    def peek_char():
        """Return the current character or None if we're at the end."""
        nonlocal parse_index
        if parse_index < len(pattern):
            return pattern[parse_index]
        return None

    def get_char():
        """Return the current character and advance by one."""
        nonlocal parse_index
        ch = peek_char()
        if ch is not None:
            parse_index += 1
        return ch

    def is_literal_char(ch):
        """A 'literal' is any char that is not a special operator."""
        return ch is not None and ch not in ['|', '*', '(', ')']

    # AST node helpers (we'll use small tuples to keep it simple)
    def make_lit(ch):       return ("lit", ch)
    def make_union(a, b):   return ("union", a, b)
    def make_concat(a, b):  return ("concat", a, b)
    def make_star(a):       return ("star", a)

    def parse_regex():
        return parse_union()

    def parse_union():
        left_node = parse_concat()
        # Keep building a union chain like a|b|c as left-associative
        while peek_char() == '|':
            get_char()  # consume '|'
            right_node = parse_concat()
            left_node = make_union(left_node, right_node)
        return left_node

    def parse_concat():
        """
        Concatenation is implicit: e.g., 'ab' means 'a' followed by 'b'.
        We read one or more 'repeat' nodes and chain them with concat.
        """
        # At least one piece must be present to form concatenation.
        nodes = []

        # A concatenation can start with:
        #   - a literal
        #   - an opening parenthesis '('
        # If none of those are present, this concat is empty (used by union/right side).
        while True:
            ch = peek_char()
            if is_literal_char(ch) or ch == '(':
                nodes.append(parse_repeat())
            else:
                break

        if not nodes:
            # Return an empty concatenation marker so higher levels know it's empty.
            # We'll represent empty as ("lit", "") so concat logic can deal with it.
            return make_lit("")  # empty string literal

        # Build left-associative concat: (((n1 . n2) . n3) . ...)
        current = nodes[0]
        i = 1
        while i < len(nodes):
            current = make_concat(current, nodes[i])
            i += 1
        return current

    def parse_repeat():
        """
        Handle Kleene star on a base: base ('*')*
        Multiple stars like 'a**' are allowed as repeated stars around the same base.
        """
        node = parse_base()
        while peek_char() == '*':
            get_char()  # consume '*'
            node = make_star(node)
        return node

    def parse_base():
        """
        Base is either a literal character or a parenthesized regex.
        """
        ch = peek_char()

        if ch == '(':
            get_char()  # consume '('
            inner = parse_regex()
            if peek_char() != ')':
                raise ValueError("Missing closing parenthesis ')' in pattern.")
            get_char()  # consume ')'
            return inner

        if is_literal_char(ch):
            get_char()
            return make_lit(ch)

        # If we reach here, it's an error (like dangling operator).
        # For robustness, treat as empty literal so higher levels can continue.
        return make_lit("")

    # Build the AST
    ast_root = parse_regex()

    # If we didn't consume the whole pattern, it's a malformed regex
    if parse_index != len(pattern):
        raise ValueError("Invalid pattern syntax near: " + pattern[parse_index:])

    # --------------------------
    # 3) MATCHER: evaluate the AST against the input string
    # We'll return the set of ending positions reachable after matching the node,
    # starting from a given start position. If len(s) is in that set, it's a match.
    # This style avoids tricky backtracking and is easier to follow.
    # --------------------------

    def match_node(node, s, start_pos):
        node_type = node[0]

        # Literal node
        if node_type == "lit":
            literal_value = node[1]

            # Empty literal matches without consuming characters
            if literal_value == "":
                return {start_pos}

            # Non-empty literal must match exactly one char
            if start_pos < len(s) and s[start_pos] == literal_value:
                return {start_pos + 1}
            else:
                return set()

        # Union node: either left OR right can match
        if node_type == "union":
            left_node = node[1]
            right_node = node[2]

            end_positions_left = match_node(left_node, s, start_pos)
            end_positions_right = match_node(right_node, s, start_pos)

            result_positions = set()
            for p in end_positions_left:
                result_positions.add(p)
            for p in end_positions_right:
                result_positions.add(p)
            return result_positions

        # Concat node: match left first, then right starting from each left end
        if node_type == "concat":
            left_node = node[1]
            right_node = node[2]

            result_positions = set()
            left_end_positions = match_node(left_node, s, start_pos)

            for middle_pos in left_end_positions:
                right_end_positions = match_node(right_node, s, middle_pos)
                for p in right_end_positions:
                    result_positions.add(p)

            return result_positions

        # Star node: zero or more repetitions of the inner node
        if node_type == "star":
            inner_node = node[1]

            # Always include start_pos (zero repetitions)
            result_positions = {start_pos}

            # We will repeatedly try to apply the inner node from any newly
            # discovered position until no more new positions are found.
            positions_to_expand = [start_pos]
            seen_positions = {start_pos}

            while positions_to_expand:
                current_pos = positions_to_expand.pop()

                inner_end_positions = match_node(inner_node, s, current_pos)

                for p in inner_end_positions:
                    if p not in seen_positions:
                        seen_positions.add(p)
                        result_positions.add(p)
                        positions_to_expand.append(p)

            return result_positions

        # Should not reach here
        raise ValueError("Unknown AST node type: " + str(node_type))

    # Start matching from position 0
    final_positions = match_node(ast_root, string, 0)

    # It's a match if any end position lands exactly at the end of the string
    return (len(string) in final_positions)





def test_assignment():
    # Test Task 1: Language L membership
    assert is_in_language_L("ab") == True
    assert is_in_language_L("aabb") == True
    assert is_in_language_L("aaabbb") == True
    assert is_in_language_L("aabbb") == False
    assert is_in_language_L("aba") == False
    assert is_in_language_L("") == False
    assert is_in_language_L("a") == False
    assert is_in_language_L("b") == False
    
    # Test Task 2: Kleene closure
    result = kleene_closure_generator(["a"], 3)
    expected = {"", "a", "aa", "aaa"}
    assert result == expected
    
    result2 = kleene_closure_generator(["ab"], 4)
    assert "" in result2
    assert "ab" in result2
    assert "abab" in result2
    assert len([s for s in result2 if len(s) <= 4]) >= 3
    
    # Test Task 3: Recursive language
    assert generate_recursive_language_M(0) == "x"
    assert generate_recursive_language_M(1) == "yxz"
    assert generate_recursive_language_M(2) == "yyxzz"
    assert generate_recursive_language_M(3) == "yyyxzzz"
    
    # Test Task 4: Regular expressions
    assert regex_match("a*", "") == True
    assert regex_match("a*", "aaa") == True
    assert regex_match("a*b", "aaab") == True
    assert regex_match("a|b", "a") == True
    assert regex_match("a|b", "c") == False
    assert regex_match("ab", "ab") == True
    assert regex_match("ab", "a") == False
    
    print("All tests passed!")

if __name__ == "__main__":
    test_assignment()