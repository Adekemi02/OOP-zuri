class CascadingPalindrome:
    def __init__(self, sequence):
        if not sequence or sequence == " ": # validate sequence is not empty
            raise ValueError("Sequence cannot be empty")
        
        self.sequence = sequence
        self.palindromes = self.get_palindrome_sequences()
        
        return

    def __repr__(self):
        return self.sequence
    
    """
    def sample(self, s):
        length = len(s)
        middle = length // 2
        left_half = s[:middle]
        right_half = s[middle + 1:] if length % 2 == 0 else s[middle:]
    """
    
    # Get the palindromes from the parameters array
    def get_palindrome_sequences(self):
        words = self.sequence.split()
        palindromes = []

        for item in words:
            # item must contain only numbers and letters
            if not isinstance(item, str) or not item.isalnum():
                raise ValueError("Invalid sequence. Words can only contain letters, numbers")
    
        for word in words:
            word_length = len(word)

            if word_length <= 2:
                continue

            middle = word_length // 2
            left_half = middle - 1
            right_half = middle + 1 if word_length % 2 == 1 else middle
            
            while left_half >= 0 and right_half < word_length:
                if word[left_half] != word[right_half]:
                    break
                
                left_half -= 1
                right_half += 1

            if right_half - left_half > 2:
                palindromes.append(word)
        
        return palindromes

if __name__ == "__main__":
    input_sequence = [" ", 
                    "1230321 09234 0124210",
                    "abcd5dcba 1230321 09234 0124210",
                    "Racecar madam radar",
                    "A man, a plan, a canal – Panama",
                    "abcdedcba abcbadef",
                    "1230321 09234 @#$%", 
                    1230321,
                    "abcd5dcba 1230321 09234",
                    "=-----BEGIN CERTIFICATE-----",
                    ""
    ]   
    # change any int type to string
    input_sequence = [str(item) for item in input_sequence]
    for input_str in input_sequence:
        try:
            palindrome = CascadingPalindrome(input_str)
        
            result = palindrome.palindromes
            print(result)

        except ValueError as e:
            print(e)
    