import unittest

from preprocess import normalize, preprocess
from sentiment import analyze, load_lexicon


class PreprocessTests(unittest.TestCase):
    def test_normalize_strips_urls_and_mentions(self) -> None:
        text = normalize("Merhaba @ahmet https://t.co/abc çok güzel!")
        self.assertNotIn("@", text)
        self.assertNotIn("http", text)
        self.assertIn("güzel", text)

    def test_preprocess_drops_short_tokens(self) -> None:
        tokens = preprocess("a ve bu çok güzel bir film")
        self.assertTrue(all(len(token) > 1 for token in tokens))


class SentimentTests(unittest.TestCase):
    def test_lexicon_loads(self) -> None:
        lexicon = load_lexicon()
        self.assertGreater(len(lexicon), 50)

    def test_positive_example(self) -> None:
        result = analyze("bu film çok güzeldi bayıldım")
        self.assertEqual(result.label, "positive")
        self.assertGreater(result.score, 0)

    def test_negative_example(self) -> None:
        result = analyze("berbat bir gündü her şey çok kötüydü")
        self.assertEqual(result.label, "negative")
        self.assertLess(result.score, 0)


if __name__ == "__main__":
    unittest.main()
