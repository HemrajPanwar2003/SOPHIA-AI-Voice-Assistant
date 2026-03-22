import re


def extract_yt_term(command):
    """Improved regex patterns for YouTube search extraction"""
    command = str(command).lower()

    # Multiple patterns for different ways users might speak
    patterns = [
        r"play\s+(.+?)(?:\s+on\s+youtube|\s+on\s+yt)?$",
        r"(?:youtube|yt)\s+(.+?)$",
        r"play\s+(.+?)(?=\s|$)",
        r"open\s+youtube\s+(.+?)$",
    ]

    for pattern in patterns:
        match = re.search(pattern, command, re.IGNORECASE)
        if match:
            term = match.group(1).strip()
            # Clean up the term
            term = re.sub(r"(music|song|video)\s+", "", term, flags=re.IGNORECASE)
            return term if len(term) > 1 else None

    # Fallback: everything after "play"
    if "play" in command:
        return command.split("play")[-1].strip()

    return None


def remove_words(input_string, words_to_remove):
    try:
        if not input_string:
            return ""

        # 🔹 Normalize input
        text = input_string.lower().strip()

        # 🔹 Remove punctuation
        text = re.sub(r"[^\w\s]", " ", text)

        # 🔹 Normalize spaces
        text = re.sub(r"\s+", " ", text)

        # 🔹 Separate single words & phrases
        single_words = set()
        phrases = []

        for word in words_to_remove:
            if not word:
                continue
            word = word.lower().strip()
            if " " in word:
                phrases.append(word)
            else:
                single_words.add(word)

        # 🔹 Remove phrases first (important!)
        for phrase in phrases:
            text = text.replace(phrase, "")

        # 🔹 Remove single words
        words = text.split()
        filtered_words = [w for w in words if w not in single_words]

        return " ".join(filtered_words).strip()

    except Exception as e:
        print(f"❌ Error in remove_words: {e}")
        return input_string
