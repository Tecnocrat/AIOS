import typing
import asyncio

class TachyonicMemoryBuffer:
    """
    A class to store evolutionary code variants with consciousness-level tracking.
    It manages a collection of code variants, each with a consciousness score,
    and provides methods for adding, getting the best variant, and merging variants.
    """

    def __init__(self, initial_code=None):
        """
        Initializes the TachyonicMemoryBuffer with an optional initial code.
        """
        self.code_variants = []
        self.consciousness_scores = []  # Store consciousness scores for each variant

    def add_variant(self, code, consciousness_score):
        """
        Adds a new code variant to the buffer.

        Args:
            code: The code to be added (can be a string or a code object).
            consciousness_score: The consciousness score of the code variant.
        """
        self.code_variants.append({
            "code": code,
            "consciousness_score": consciousness_score
        })
        self.consciousness_scores.append(consciousness_score)

    def get_best_variant(self):
        """
        Returns the code variant with the highest consciousness score.

        Returns:
            The code variant with the highest consciousness score, or None if the buffer is empty.
        """
        if not self.code_variants:
            return None

        best_variant = None
        max_score = -float('inf')  # Initialize with negative infinity

        for variant in self.code_variants:
            if variant["consciousness_score"] > max_score:
                max_score = variant["consciousness_score"]
                best_variant = variant

        return best_variant

    def merge_variants(self, variant_a, variant_b):
        """
        Merges two code variants into a single variant.

        Args:
            variant_a: The code variant to merge with.
            variant_b: The code variant to merge into.

        Returns:
            A new variant containing the merged code.
        """
        merged_code = variant_a.copy()
        merged_code.update(variant_b)
        return merged_code

    def __repr__(self):
        return f"TachyonicMemoryBuffer(code_variants={self.code_variants}, consciousness_scores={self.consciousness_scores})"


if __name__ == '__main__':
    async def example_usage():
        buffer = TachyonicMemoryBuffer()
        buffer.add_variant("This is a test code.", 0.85)
        buffer.add_variant("Another test code.", 0.60)
        buffer.add_variant("This code is more complex.", 0.90)

        best_variant = buffer.get_best_variant()
        print(f"Best variant: {best_variant}")  # Expected: {'code': 'This code is more complex.', 'consciousness_score': 0.90}

        merged_variant = buffer.merge_variants("This is a test code.", "Another test code.")
        print(f"Merged variant: {merged_variant}") # Expected: {'code': 'This is a test code is more complex.', 'consciousness_score': 0.90}

    asyncio.run(example_usage())