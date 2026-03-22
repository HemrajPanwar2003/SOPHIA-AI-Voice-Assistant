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


def remove_words_advanced(input_string, words_to_remove):
    if not input_string:
        return ""

    remove_set = {w.lower() for w in words_to_remove}

    words = re.findall(r"\b\w+\b", input_string)

    result = []
    for word in words:
        if word.lower() not in remove_set:
            result.append(word)

    return " ".join(result)
