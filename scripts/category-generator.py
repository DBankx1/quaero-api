import pdfplumber
import json
from slugify import slugify

PDF_PATH = "data/raw/yelp-business-categories-list.pdf"
OUTPUT_PATH = "data/processed/categories.json"


def normalize(text: str) -> str:
    return text.strip()


def make_slug(*parts: str) -> str:
    return ".".join(slugify(p) for p in parts if p)


def generate_categories():
    categories = []

    current_primary = None
    current_secondary = None

    with pdfplumber.open(PDF_PATH) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            lines = [normalize(l) for l in text.split("\n") if l.strip()]

            for line in lines:
                # PRIMARY CATEGORY (ALL CAPS)
                if line.isupper():
                    current_primary = line.title()
                    current_secondary = None

                    categories.append({
                        "slug": make_slug(current_primary),
                        "name": current_primary,
                        "level": "primary",
                        "primary": current_primary,
                        "secondary": None,
                        "parent_slug": None
                    })
                    continue

                # SECONDARY CATEGORY (Indented or bullet-like)
                if current_primary and not line.startswith("-") and line.istitle():
                    current_secondary = line

                    categories.append({
                        "slug": make_slug(current_primary, current_secondary),
                        "name": current_secondary,
                        "level": "secondary",
                        "primary": current_primary,
                        "secondary": current_secondary,
                        "parent_slug": make_slug(current_primary)
                    })
                    continue

                # TERTIARY CATEGORY (usually bullet-prefixed)
                if current_primary and current_secondary and (
                    line.startswith("-") or line.startswith("•")
                ):
                    tertiary = line.lstrip("-• ").strip()

                    categories.append({
                        "slug": make_slug(current_primary, current_secondary, tertiary),
                        "name": tertiary,
                        "level": "tertiary",
                        "primary": current_primary,
                        "secondary": current_secondary,
                        "parent_slug": make_slug(current_primary, current_secondary)
                    })

    return categories


def main():
    categories = generate_categories()

    print(f"Generated {len(categories)} categories")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(categories, f, indent=2, ensure_ascii=False)

    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
