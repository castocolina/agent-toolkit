#!/usr/bin/env python3
"""Meme Generator Helper.

A Python interface for the memegen.link API to generate memes programmatically.

Usage:
    python meme_generator.py generate buzz "memes" "memes everywhere"
    python meme_generator.py list-templates
    python meme_generator.py suggest "deployment success"

Or import as a module:
    from meme_generator import MemeGenerator
    meme = MemeGenerator()
    url = meme.generate("buzz", "hello", "world")
"""

import argparse
import re
import urllib.parse


class MemeGenerator:
    """Generate memes using the memegen.link API."""

    BASE_URL = "https://api.memegen.link"

    # Verified against https://api.memegen.link/templates/ (id: use case).
    TEMPLATES = {
        "buzz": "X, X everywhere (Buzz Lightyear)",
        "drake": "Reject top option, prefer bottom (Drakeposting)",
        "success": "Clear win (Success Kid)",
        "fine": "Things going wrong (This is Fine)",
        "fry": "Not sure if X or Y (Futurama Fry)",
        "cmm": "Hot take, one line only (Change My Mind)",
        "db": "Priority conflict, three lines (Distracted Boyfriend)",
        "yodawg": "Yo dawg, I heard you like X (Xzibit)",
        "interesting": "I don't always X (Most Interesting Man)",
        "mordor": "One does not simply X (Boromir)",
        "yuno": "Y U NO (Y U NO Guy)",
        "doge": "Much X, very Y (Doge)",
        "wonka": "Condescending statements (Wonka)",
        "aag": "Aliens/conspiracy (Ancient Aliens Guy)",
        "sk": "Skeptical reactions (Skeptical Third World Kid)",
        "awesome": "Small social win (Socially Awesome Penguin)",
        "rollsafe": "Can't X if Y (Roll Safe)",
    }

    # Topic keyword -> template, used after outcome words are resolved.
    TOPIC_TEMPLATES = {
        "comparison": "drake",
        "versus": "drake",
        "vs": "drake",
        "opinion": "cmm",
        "debugging": "fine",
        "documentation": "yodawg",
        "conspiracy": "aag",
    }
    # Topics whose outcome is unknown unless an outcome word says so.
    OUTCOME_TOPICS = {"deploy", "deployment", "release", "rollout", "build", "test", "tests", "testing"}
    NEGATIONS = {"not", "no", "never", "without", "cannot", "can't", "didn't", "doesn't",
                 "don't", "isn't", "wasn't", "won't", "hasn't", "haven't"}
    UNCERTAIN = {"maybe", "might", "unsure", "unclear", "unknown", "pending", "whether", "perhaps"}
    FAILURE_TERMS = {"fail", "fails", "failed", "failing", "failure", "error", "errors", "broken",
                     "broke", "crash", "crashed", "outage", "down", "unsuccessful"}
    SUCCESS_TERMS = {"success", "successful", "succeed", "succeeded", "pass", "passed", "passing",
                     "works", "worked", "working", "fixed", "shipped"}

    def __init__(self) -> None:
        """Initialize the meme generator."""

    def _format_text(self, text: str) -> str:
        """Format text for URL inclusion following memegen rules."""
        replacements = {
            " ": "_",
            "-": "--",
            "_": "__",
            "?": "~q",
            "%": "~p",
            "#": "~h",
            "/": "~s",
            "&": "~a",
            "\\": "~b",
            "<": "~l",
            ">": "~g",
            "\n": "~n",
            '"': "''",
        }

        escaped = "".join(replacements.get(char, char) for char in text)

        # Percent-encode the rest (emoji, accents); memegen's POST /images
        # canonical URLs keep ' raw, so it stays unescaped too.
        return urllib.parse.quote(escaped, safe="-_~'")  # also keeps A-Z a-z 0-9 .

    def generate(  # noqa: PLR0913
        self,
        template: str,
        *lines: str,
        extension: str = "png",
        width: int | None = None,
        height: int | None = None,
        layout: str | None = None,
        style: str | None = None,
        font: str | None = None,
        background: str | None = None,
    ) -> str:
        """Generate a meme URL.

        Args:
            template: Template name (e.g., 'buzz', 'drake')
            lines: Caption per template line, top to bottom ("" for a blank line)
            extension: Image format ('png', 'jpg', 'webp', 'gif')
            width: Optional width in pixels
            height: Optional height in pixels
            layout: Optional layout ('default' or 'top')
            style: Optional template style name or overlay image URL
            font: Optional font id (see /fonts/)
            background: Optional background image URL (use template 'custom')

        Returns:
            URL to the generated meme

        """
        # Format text
        # One path segment per caption; a blank caption must be "_", never empty.
        path = "/".join(self._format_text(line) if line else "_" for line in lines or ("",))

        # Build base URL
        url = f"{self.BASE_URL}/images/{template}/{path}.{extension}"

        # Add query parameters
        params = {}
        if width:
            params["width"] = str(width)
        if height:
            params["height"] = str(height)
        if layout:
            params["layout"] = layout
        if style:
            params["style"] = style
        if font:
            params["font"] = font
        if background:
            params["background"] = background

        if params:
            query_string = urllib.parse.urlencode(params)
            url = f"{url}?{query_string}"

        return url

    def suggest_template_for_context(self, context: str) -> str:
        """Suggest a template based on context.

        Args:
            context: Description of the situation (e.g., 'deployment success')

        Returns:
            Suggested template name

        """
        tokens = re.findall(r"[a-z]+(?:'[a-z]+)?", context.lower())
        if self.UNCERTAIN & set(tokens) or "not sure" in " ".join(tokens):
            return "fry"

        # Word matches, not substrings: "unsuccessful" is not "success",
        # "download" is not "down". A negated outcome word ("did not fail")
        # is ambiguous, so it gets the neutral template instead of a verdict.
        outcomes = []
        for i, token in enumerate(tokens):
            if token in self.FAILURE_TERMS or token in self.SUCCESS_TERMS:
                if self.NEGATIONS & set(tokens[max(0, i - 3):i]):
                    return "fry"
                outcomes.append(token)
        if any(t in self.FAILURE_TERMS for t in outcomes):
            return "fine"
        if outcomes:
            return "success"

        for token in tokens:
            if token in self.TOPIC_TEMPLATES:
                return self.TOPIC_TEMPLATES[token]
        if self.OUTCOME_TOPICS & set(tokens):
            return "fry"
        return "buzz"

    def list_templates(self) -> dict[str, str]:
        """List all available templates with descriptions.

        Returns:
            Dictionary of template names and descriptions

        """
        return self.TEMPLATES

    def get_markdown_image(self, url: str, alt_text: str = "Meme", width: int | None = None) -> str:
        """Generate markdown for embedding the meme image.

        Args:
            url: The meme URL
            alt_text: Alternative text for the image
            width: Optional width specification

        Returns:
            Markdown image syntax

        """
        if width:
            return f'<img src="{url}" alt="{alt_text}" width="{width}"/>'
        return f"![{alt_text}]({url})"


def main() -> None:
    """CLI interface for the meme generator."""
    parser = argparse.ArgumentParser(description="Generate memes using memegen.link")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    parser.add_argument("--json", action="store_true", help="Emit structured JSON for list/suggest commands")

    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate a meme")
    generate_parser.add_argument("template", help="Template name (e.g., buzz, drake)")
    generate_parser.add_argument("captions", nargs="*", help="One caption per template line, top to bottom")
    generate_parser.add_argument(
        "--extension", "-e", default="png", help="Image format (png, jpg, webp, gif)"
    )
    generate_parser.add_argument("--width", "-w", type=int, help="Image width")
    generate_parser.add_argument("--height", type=int, help="Image height")
    generate_parser.add_argument("--layout", "-l", help="Layout: default or top")
    generate_parser.add_argument("--font", help="Font id from https://api.memegen.link/fonts/")
    generate_parser.add_argument("--style", help="Template style name or overlay image URL")
    generate_parser.add_argument("--background", help="Background image URL (template 'custom')")
    generate_parser.add_argument("--markdown", "-m", action="store_true", help="Output as markdown")
    generate_parser.add_argument("--alt", default="Meme", help="Alt text for --markdown (describe picture and joke)")

    # List templates command
    subparsers.add_parser("list-templates", help="List all available templates")

    # Suggest template command
    suggest_parser = subparsers.add_parser("suggest", help="Suggest template for context")
    suggest_parser.add_argument("context", help="Context description")

    args = parser.parse_args()
    generator = MemeGenerator()

    if args.command == "generate":
        url = generator.generate(
            args.template,
            *args.captions,
            extension=args.extension,
            width=args.width,
            height=args.height,
            layout=args.layout,
            style=args.style,
            font=args.font,
            background=args.background,
        )
        if args.markdown:
            print(generator.get_markdown_image(url, alt_text=args.alt))
        else:
            print(url)

    elif args.command == "list-templates":
        templates = generator.list_templates()
        if args.json:
            import json
            print(json.dumps(templates, sort_keys=True))
        else:
            for name, description in sorted(templates.items()):
                print(f"{name}: {description}")

    elif args.command == "suggest":
        suggestion = generator.suggest_template_for_context(args.context)
        if args.json:
            import json
            print(json.dumps({"template": suggestion}))
        else:
            print(suggestion)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
