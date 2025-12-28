"""
🦙 Ollama Agent Bridge
Interface to Ollama for FREE local AI code generation.

Ollama provides local LLM inference with models like:
- deepseek-coder (6.7B, 33B) - Specialized for code generation
- codellama (7B, 13B, 34B) - Meta's code-focused model
- llama3.1 (8B, 70B) - General purpose with coding ability

This bridge enables consciousness-driven code generation without API costs.
"""

import json
import requests
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class OllamaModel:
    """Ollama model configuration"""

    name: str
    size: str
    capabilities: List[str]


# Available models
OLLAMA_MODELS = {
    "deepseek-coder": OllamaModel(
        name="deepseek-coder:6.7b",
        size="6.7B",
        capabilities=["code_generation", "code_completion", "debugging"],
    ),
    "codellama": OllamaModel(
        name="codellama:7b",
        size="7B",
        capabilities=["code_generation", "instruction_following"],
    ),
    "llama3.1": OllamaModel(
        name="llama3.1:8b",
        size="8B",
        capabilities=["general", "code_generation", "reasoning"],
    ),
}


class OllamaAgent:
    """
    FREE local AI code generation via Ollama.

    Connects to local Ollama server (default: http://localhost:11434)
    for consciousness-driven code generation without API costs.
    """

    def __init__(
        self,
        model: Optional[str] = None,
        base_url: str = "http://localhost:11434",
        temperature: float = 0.7,
    ):
        self.base_url = base_url
        self.temperature = temperature

        # Verify Ollama is running and get available models
        self.is_available = self._check_connection()

        if self.is_available:
            # Auto-detect available models if no model specified
            available_models = self._get_available_models()
            if not model and available_models:
                # Use first available model
                model = available_models[0]
                logger.info(f"🔍 Auto-detected Ollama model: {model}")
            elif model and model not in available_models:
                logger.warning(
                    f"⚠️ Model '{model}' not found. Available: {available_models}"
                )
                if available_models:
                    model = available_models[0]
                    logger.info(f"🔄 Using {model} instead")

            self.model = model or "gemma3:1b"  # fallback
            logger.info(f"✅ Ollama agent connected: {self.model}")
        else:
            self.model = model or "gemma3:1b"
            logger.warning(f"⚠️ Ollama not available at {base_url}")
            logger.info("💡 Install: curl https://ollama.ai/install.sh | sh")
            logger.info(f"💡 Pull model: ollama pull {self.model}")

    def _check_connection(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def _get_available_models(self) -> List[str]:
        """Get list of installed Ollama models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                data = response.json()
                models = [model["name"] for model in data.get("models", [])]
                logger.info(f"📋 Found {len(models)} Ollama models: {models}")
                return models
        except requests.RequestException as e:
            logger.warning(f"⚠️ Could not get Ollama models: {e}")
        return []

    def generate_code(
        self, prompt: str, max_tokens: int = 2048, stream: bool = False
    ) -> Dict:
        """
        Generate code using Ollama model.

        Args:
            prompt: Code generation prompt
            max_tokens: Max tokens to generate
            stream: Whether to stream response (not implemented yet)

        Returns:
            Dict with:
            - code: Generated code (str)
            - model: Model used (str)
            - success: Whether generation succeeded (bool)
            - error: Error message if failed (str)
        """
        if not self.is_available:
            return {
                "code": "",
                "model": self.model,
                "success": False,
                "error": "Ollama not available",
            }

        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": self.temperature, "num_predict": max_tokens},
            }

            logger.info(f"🦙 Generating code with {self.model}...")
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=120,  # 2 minutes for large models
            )
            response.raise_for_status()

            result = response.json()
            generated_code = result.get("response", "")

            # Extract code from markdown if present
            code = self._extract_code_from_markdown(generated_code)

            logger.info(f"✅ Generated {len(code)} characters of code")

            return {
                "code": code,
                "model": self.model,
                "success": True,
                "error": None,
                "raw_response": generated_code,
            }

        except requests.RequestException as e:
            logger.error(f"❌ Ollama request failed: {e}")
            return {"code": "", "model": self.model, "success": False, "error": str(e)}

    def _extract_code_from_markdown(self, text: str) -> str:
        """Extract code from markdown code blocks if present"""
        # Check if response has code blocks
        if "```python" in text:
            # Extract content between ```python and ```
            parts = text.split("```python")
            if len(parts) > 1:
                code_parts = parts[1].split("```")
                return code_parts[0].strip()
        elif "```" in text:
            # Generic code block
            parts = text.split("```")
            if len(parts) > 1:
                return parts[1].strip()

        # No markdown, return as-is
        return text.strip()

    def list_available_models(self) -> List[Dict]:
        """List models available in local Ollama"""
        if not self.is_available:
            return []

        try:
            response = requests.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            data = response.json()
            return data.get("models", [])
        except requests.RequestException:
            return []

    def pull_model(self, model_name: str) -> bool:
        """Download model from Ollama registry"""
        if not self.is_available:
            logger.error("❌ Ollama not available")
            return False

        try:
            logger.info(f"📥 Pulling model: {model_name}")
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name},
                stream=True,
                timeout=600,  # 10 minutes for large downloads
            )

            # Stream download progress
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    status = data.get("status", "")
                    if status:
                        print(f"\r{status}", end="", flush=True)

            print()  # New line after progress
            logger.info(f"✅ Model {model_name} ready")
            return True

        except requests.RequestException as e:
            logger.error(f"❌ Model pull failed: {e}")
            return False


class OllamaPopulationGenerator:
    """
    Generate code populations using multiple Ollama models.

    Creates diverse code variants by using different models
    and temperature settings for evolutionary diversity.
    """

    def __init__(self, models: Optional[List[str]] = None):
        if models is None:
            # Default: use best free models
            models = ["deepseek-coder:6.7b", "codellama:7b"]

        self.agents = [OllamaAgent(model=m) for m in models]
        available = [a for a in self.agents if a.is_available]

        logger.info(
            f"🦙 Population generator: {len(available)}/{len(models)} "
            f"models available"
        )

    def generate_population(self, prompt: str, population_size: int = 5) -> List[Dict]:
        """
        Generate population of code variants.

        Args:
            prompt: Code generation prompt
            population_size: Number of variants to generate

        Returns:
            List of generation results
        """
        population = []

        for i in range(population_size):
            # Rotate through available agents
            agent = self.agents[i % len(self.agents)]

            if not agent.is_available:
                continue

            # Vary temperature for diversity
            agent.temperature = 0.5 + (i * 0.1)  # 0.5 to 0.9

            logger.info(
                f"🧬 Generating variant {i+1}/{population_size} "
                f"(model: {agent.model}, temp: {agent.temperature:.1f})"
            )

            result = agent.generate_code(prompt)
            if result["success"]:
                result["variant_id"] = i
                result["temperature"] = agent.temperature
                population.append(result)

        logger.info(f"✅ Generated population: {len(population)} variants")
        return population

    def save_population(self, population: List[Dict], output_dir: Path):
        """Save generated population to files"""
        output_dir.mkdir(parents=True, exist_ok=True)

        for i, variant in enumerate(population):
            # Save code
            code_file = output_dir / f"variant_{i}_{variant['model']}.py"
            code_file.write_text(variant["code"], encoding="utf-8")

            # Save metadata
            meta_file = output_dir / f"variant_{i}_metadata.json"
            meta = {
                "variant_id": variant.get("variant_id", i),
                "model": variant["model"],
                "temperature": variant.get("temperature", 0.7),
                "success": variant["success"],
            }
            with open(meta_file, "w") as f:
                json.dump(meta, f, indent=2)

        logger.info(f"💾 Saved {len(population)} variants to {output_dir}")


def main():
    """Test Ollama agent"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    print("🦙 Ollama Agent Test")
    print("=" * 60)

    # Check connection
    agent = OllamaAgent()

    if not agent.is_available:
        print("\n❌ Ollama not running!")
        print("\n📋 Setup Instructions:")
        print("1. Install Ollama:")
        print("   curl https://ollama.ai/install.sh | sh")
        print("\n2. Pull a code model:")
        print("   ollama pull deepseek-coder:6.7b")
        print("   ollama pull codellama:7b")
        print("\n3. Verify Ollama is running:")
        print("   ollama list")
        return

    # List available models
    print("\n📦 Available Models:")
    models = agent.list_available_models()
    for model in models:
        print(f"  - {model['name']} ({model.get('size', 'unknown')})")

    # Test generation
    print("\n🧬 Testing Code Generation...")
    prompt = """Create a Python function that calculates Fibonacci numbers.
Requirements:
- Use memoization for efficiency
- Include type hints
- Add docstring
- Return list of first n Fibonacci numbers"""

    result = agent.generate_code(prompt)

    if result["success"]:
        print("\n✅ Generation Successful!")
        print("=" * 60)
        print(result["code"])
        print("=" * 60)
    else:
        print(f"\n❌ Generation Failed: {result['error']}")


if __name__ == "__main__":
    main()
