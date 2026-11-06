"""Tests for skills/meme-factory/scripts/meme_generator.py.

Pins the behavior documented in the script docstring and the meme-factory
SKILL.md: the CLI prints the generated memegen URL (or markdown with
--markdown), prints a template suggestion for a context, and prints every
known template. All behavior is pure URL/string construction; no test
touches the network.
"""

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/meme-factory/scripts/meme_generator.py"

BASE_URL = "https://api.memegen.link"


def load_module():
    spec = importlib.util.spec_from_file_location("meme_generator_under_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MEME = load_module()


def run_cli(*args):
    """Run the script's CLI and return its stdout."""
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=True,
    ).stdout


class GenerateCliTests(unittest.TestCase):
    def test_generate_prints_memegen_url(self):
        out = run_cli("generate", "buzz", "memes", "memes everywhere")
        self.assertEqual(
            out.strip(),
            f"{BASE_URL}/images/buzz/memes/memes_everywhere.png",
        )

    def test_generate_markdown_flag_prints_markdown_image(self):
        out = run_cli("generate", "buzz", "memes", "memes everywhere", "--markdown")
        self.assertIn(
            f"![Meme]({BASE_URL}/images/buzz/memes/memes_everywhere.png)",
            out,
        )

    def test_generate_alt_flag_sets_markdown_alt_text(self):
        out = run_cli("generate", "fine", "a", "b", "--markdown", "--alt", "Dog in fire: prod is fine")
        self.assertEqual(out.strip(), f"![Dog in fire: prod is fine]({BASE_URL}/images/fine/a/b.png)")

    def test_generate_extension_flag_sets_extension(self):
        out = run_cli("generate", "buzz", "a", "b", "--extension", "jpg")
        self.assertTrue(out.strip().endswith("/images/buzz/a/b.jpg"), out)

    def test_generate_dimension_and_layout_flags_set_query_params(self):
        out = run_cli(
            "generate", "buzz", "a", "b", "--width", "800", "--height", "600", "--layout", "top"
        )
        self.assertIn("width=800&height=600&layout=top", out)

    def test_generate_font_style_background_flags_are_query_encoded(self):
        out = run_cli(
            "generate", "custom", "a", "b", "--font", "impact", "--style", "default",
            "--background", "https://example.com/x.png",
        )
        self.assertIn("style=default&font=impact&background=https%3A%2F%2Fexample.com%2Fx.png", out)

    def test_generate_single_caption_is_one_segment(self):
        out = run_cli("generate", "cmm", "tabs beat spaces")
        self.assertEqual(out.strip(), f"{BASE_URL}/images/cmm/tabs_beat_spaces.png")

    def test_generate_three_captions_for_db(self):
        out = run_cli("generate", "db", "me", "new JS framework", "a/b tested code")
        self.assertEqual(out.strip(), f"{BASE_URL}/images/db/me/new_JS_framework/a~sb_tested_code.png")

    def test_remaining_reserved_characters_are_percent_encoded(self):
        out = run_cli("generate", "buzz", "C++ @ 9:00!", "ok")
        self.assertEqual(out.strip(), f"{BASE_URL}/images/buzz/C%2B%2B_%40_9%3A00%21/ok.png")


class SuggestCliTests(unittest.TestCase):
    def test_suggest_json_prints_template(self):
        self.assertEqual(run_cli("--json", "suggest", "deployment success").strip(), '{"template": "success"}')

    def test_suggest_falls_back_to_buzz_for_unknown_context(self):
        out = run_cli("suggest", "an unrelated situation entirely")
        self.assertEqual(out.strip(), "buzz")

    def test_deployment_success_and_failure_are_resolved_before_topic(self):
        self.assertEqual(run_cli("suggest", "deployment success").strip(), "success")
        self.assertEqual(run_cli("suggest", "deployment failed").strip(), "fine")

    def test_ambiguous_deployment_uses_neutral_template(self):
        self.assertEqual(run_cli("suggest", "deployment update").strip(), "fry")


class SuggestOutcomeTests(unittest.TestCase):
    """Negation and uncertainty win over outcome words; matching is per word."""

    def suggest(self, context):
        return MEME.MemeGenerator().suggest_template_for_context(context)

    def test_negated_success_is_neutral(self):
        self.assertEqual(self.suggest("the deploy is not working"), "fry")
        self.assertEqual(self.suggest("tests haven't passed yet"), "fry")

    def test_negated_failure_is_neutral(self):
        self.assertEqual(self.suggest("the build didn't fail this time"), "fry")

    def test_uncertainty_is_neutral(self):
        self.assertEqual(self.suggest("release might be broken"), "fry")
        self.assertEqual(self.suggest("not sure if bug or feature"), "fry")

    def test_substring_collisions_do_not_match(self):
        self.assertEqual(self.suggest("unsuccessful rollout"), "fine")
        self.assertEqual(self.suggest("download page for passwords"), "buzz")

    def test_failure_wins_over_success_in_mixed_outcome(self):
        self.assertEqual(self.suggest("flaky tests failing even though lint passed"), "fine")

    def test_topic_keyword_maps_to_template(self):
        self.assertEqual(self.suggest("manual vs automated testing"), "drake")

    def test_every_suggestion_is_a_listed_template(self):
        known = set(MEME.MemeGenerator.TEMPLATES)
        self.assertLessEqual(set(MEME.MemeGenerator.TOPIC_TEMPLATES.values()), known)
        self.assertIn("fry", known)


class ListTemplatesCliTests(unittest.TestCase):
    def test_list_templates_prints_every_template(self):
        out = run_cli("list-templates")
        names = {line.split(":", 1)[0].strip() for line in out.strip().splitlines()}
        self.assertEqual(names, set(MEME.MemeGenerator.TEMPLATES))
        self.assertEqual(len(out.strip().splitlines()), len(MEME.MemeGenerator.TEMPLATES))

    def test_list_templates_json_is_parseable(self):
        import json
        out = run_cli("--json", "list-templates")
        self.assertEqual(json.loads(out), MEME.MemeGenerator.TEMPLATES)


class ModuleApiTests(unittest.TestCase):
    """The docstring documents importing the module: MemeGenerator().generate(...)."""

    def setUp(self):
        self.generator = MEME.MemeGenerator()

    def test_generate_returns_memegen_url(self):
        self.assertEqual(
            self.generator.generate("buzz", "hello", "world"),
            f"{BASE_URL}/images/buzz/hello/world.png",
        )

    def test_generate_encodes_special_characters_per_memegen_rules(self):
        url = self.generator.generate("buzz", "hello world?", "50% a/b")
        self.assertEqual(url, f"{BASE_URL}/images/buzz/hello_world~q/50~p_a~sb.png")

    def test_generate_matches_memegen_canonical_escaping(self):
        # Expected path is what POST https://api.memegen.link/images returned for the same text.
        url = self.generator.generate("buzz", 'a & "q" it\'s x-y_z #1', "a<b>c \\ d\nnew")
        self.assertEqual(
            url, f"{BASE_URL}/images/buzz/a_~a_''q''_it's_x--y__z_~h1/a~lb~gc_~b_d~nnew.png"
        )

    def test_empty_top_uses_placeholder_segment(self):
        self.assertEqual(self.generator.generate("custom", "", "b"), f"{BASE_URL}/images/custom/_/b.png")

    def test_suggest_template_for_context_returns_first_keyword_match(self):
        self.assertEqual(self.generator.suggest_template_for_context("celebrating success"), "success")

    def test_list_templates_returns_every_template(self):
        self.assertEqual(self.generator.list_templates(), MEME.MemeGenerator.TEMPLATES)

    def test_get_markdown_image_without_width(self):
        self.assertEqual(
            self.generator.get_markdown_image(f"{BASE_URL}/images/buzz/a/b.png", alt_text="My meme"),
            f"![My meme]({BASE_URL}/images/buzz/a/b.png)",
        )

    def test_get_markdown_image_with_width_uses_img_tag(self):
        self.assertEqual(
            self.generator.get_markdown_image(f"{BASE_URL}/images/buzz/a/b.png", width=500),
            f'<img src="{BASE_URL}/images/buzz/a/b.png" alt="Meme" width="500"/>',
        )


if __name__ == "__main__":
    unittest.main()
