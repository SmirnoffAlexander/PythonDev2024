import argparse
import random
from urllib.parse import urlparse
from urllib.request import urlopen


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def bullscows(guess: str, secret: str) -> (int, int):
    if len(guess) != len(secret):
        n = len(guess)
        m = len(secret)
        raise RuntimeError(
            f"Length of guess: {n} is not equal to length of secret: {m}"
        )

    bulls = 0
    secret_list = list(secret)
    cows = 0
    for guess_c, secret_c in zip(guess, secret):
        if guess_c == secret_c:
            bulls += 1
        if guess_c in secret_list:
            secret_list.remove(guess_c)
            cows += 1
    return bulls, cows


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret = random.choice(words)
    guess = ""
    cnt = 0
    while secret != guess:
        cnt += 1
        guess = ask("Введите слово: ", words)
        bulls, cows = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", bulls, cows)

    print(f"Слово угадано! Сделано {cnt} попыток!")
    return cnt


def ask(prompt: str, valid: list[str] = None) -> str:
    while True:
        print(prompt)
        guess = input()
        if valid is None or guess in valid:
            return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--word_dict",
        default="https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt",
        required=False,
        type=str,
    )
    parser.add_argument("--word_len", default=5, required=False, type=int)

    args = parser.parse_args()
    words = []
    if is_valid_url(args.word_dict):
        for line in urlopen(args.word_dict):
            words.append(line.strip().decode("utf-8"))
    else:
        try:
            with open(args.word_dict, "r") as f:
                words = f.read().splitlines()
                words = [word.strip() for word in words]
        except Exception as ex:
            print(ex)
            return

    words = [word for word in words if len(word) == args.word_len]
    gameplay(ask, inform, words)


if __name__ == "__main__":
    main()
