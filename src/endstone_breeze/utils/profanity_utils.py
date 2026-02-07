from profanity_check import predict
from .general_utils import split_into_tokens, levenshtein
import base64
from wordfreq import top_n_list

from .words import blacklist, whitelist
from .words import longlist as unlonglisted

_longlist = [
    w.strip().lower()
    for w in base64.b64decode(unlonglisted).decode("utf-8", errors="ignore").splitlines()
    if w.strip()
]

english_words_list = set(top_n_list("en", 10000))


class ProfanityFilter:
    def is_profane(
        self,
        text: str,
        word_list: set[str] | None = None,
        allowed_words_list: set[str] | None = None,
    ) -> bool:
        raise NotImplementedError

    def censor(
        self,
        text: str,
        replacement: str = "#",
        neighbors: int = 1,
        word_list: set[str] | None = None,
        allowed_words_list: set[str] | None = None,
    ) -> str:
        raise NotImplementedError


class ProfanityExtraList(ProfanityFilter):
    def is_profane(self, text: str, word_list=None, allowed_words_list=None) -> bool:
        tokens = [t.lower() for t in split_into_tokens(text)]
        blocked = word_list if word_list is not None else blacklist
        allowed = allowed_words_list if allowed_words_list is not None else whitelist

        for token in tokens:
            if token in allowed or token in english_words_list:
                continue

            for bad in blocked:
                if levenshtein(token, bad) <= max(1, len(bad) // 1.3):
                    return True

                if abs(len(token) - len(bad)) <= 5:
                    for i in range(len(token) - len(bad) + 1):
                        if levenshtein(token[i:i + len(bad)], bad) <= max(1, len(bad) // 2):
                            return True
        return False

    def censor(self, text: str, replacement="#", neighbors=1, word_list=None, allowed_words_list=None) -> str:
        tokens = split_into_tokens(text)
        lowered = [t.lower() for t in tokens]
        n = len(tokens)
        censored = [False] * n

        for i, tok in enumerate(tokens):
            if tok.isalnum() and self.is_profane(tok, word_list, allowed_words_list):
                censored[i] = True

                j = i
                seen = 0
                while j > 0 and seen < neighbors:
                    j -= 1
                    if lowered[j].isalnum():
                        censored[j] = True
                        seen += 1

                j = i
                seen = 0
                while j < n - 1 and seen < neighbors:
                    j += 1
                    if lowered[j].isalnum():
                        censored[j] = True
                        seen += 1

        return "".join(
            replacement * len(t) if censored[i] and lowered[i].isalnum() else t
            for i, t in enumerate(tokens)
        )


class ProfanityList(ProfanityFilter):
    def is_profane(self, text: str, word_list=None, *_args, **_kwargs) -> bool:
        tokens = [t.lower() for t in split_into_tokens(text)]
        blocked = word_list if word_list is not None else _longlist

        for token in tokens:
            for bad in blocked:
                if bad in token:
                    return True
        return False

    def censor(self, text: str, replacement="#", neighbors=1, word_list=None, *_args, **_kwargs) -> str:
        tokens = split_into_tokens(text)
        lowered = [t.lower() for t in tokens]
        n = len(tokens)
        censored = [False] * n

        blocked = word_list if word_list is not None else _longlist

        for i, tok in enumerate(lowered):
            for bad in blocked:
                if bad in tok:
                    censored[i] = True

                    j = i
                    seen = 0
                    while j > 0 and seen < neighbors - 1:
                        j -= 1
                        if lowered[j].isalnum():
                            censored[j] = True
                            seen += 1

                    j = i
                    seen = 0
                    while j < n - 1 and seen < neighbors - 1:
                        j += 1
                        if lowered[j].isalnum():
                            censored[j] = True
                            seen += 1
                    break

        return "".join(
            replacement * len(t) if censored[i] and lowered[i].isalnum() else t
            for i, t in enumerate(tokens)
        )


class ProfanityCheck(ProfanityFilter):
    def is_profane(self, text: str, *_args, **_kwargs) -> bool:
        return bool(predict(["".join(split_into_tokens(text))])[0])

    def censor(self, text: str, replacement="#", neighbors=1, window_size=1, *_args, **_kwargs) -> str:
        tokens = split_into_tokens(text)
        lowered = [t.lower() for t in tokens]
        n = len(tokens)

        windows = [" ".join(lowered[i:i + window_size]) for i in range(n)]
        flags = predict(windows)

        censored = [False] * n
        for i, flag in enumerate(flags):
            if flag:
                for j in range(max(0, i - neighbors), min(n, i + window_size + neighbors)):
                    censored[j] = True

        return "".join(
            replacement * len(t) if censored[i] and t.strip() else t
            for i, t in enumerate(tokens)
        )
