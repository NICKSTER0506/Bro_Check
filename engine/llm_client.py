"""
Open-Source AI Inference Client for BroCheck
"""

import os
import json
import random
import requests
from typing import Optional

DEFAULT_OPEN_MODEL = "meta-llama/Llama-3.2-3B-Instruct"

class OpenAIEngine:
    def __init__(self, model_name: str = DEFAULT_OPEN_MODEL):
        self.model_name = model_name
        self.hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")

    def generate_roast(self, system_prompt: str, user_prompt: str) -> str:
        # 1. Try Groq if key is present
        if self.groq_key:
            try:
                res = self._call_groq(system_prompt, user_prompt)
                if res:
                    return res
            except Exception:
                pass

        # 2. Try OpenRouter if key is present
        if self.openrouter_key:
            try:
                res = self._call_openrouter(system_prompt, user_prompt)
                if res:
                    return res
            except Exception:
                pass

        # 3. Try Hugging Face Inference API
        try:
            res = self._call_huggingface(system_prompt, user_prompt)
            if res:
                return res
        except Exception:
            pass

        # 4. Try local Ollama if running on localhost:11434
        try:
            res = self._call_ollama(system_prompt, user_prompt)
            if res:
                return res
        except Exception:
            pass

        # 5. Fallback to Built-in Dynamic Comedy Roaster (Zero API key / offline guarantee)
        return self._dynamic_fallback_roast(system_prompt, user_prompt)

    def _call_huggingface(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        api_url = f"https://api-inference.huggingface.co/models/{self.model_name}/v1/chat/completions"
        headers = {
            "Content-Type": "application/json"
        }
        if self.hf_token:
            headers["Authorization"] = f"Bearer {self.hf_token}"
            
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 500,
            "temperature": 0.85
        }
        
        resp = requests.post(api_url, headers=headers, json=payload, timeout=12)
        if resp.status_code == 200:
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
        return None

    def _call_groq(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        api_url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.85,
            "max_tokens": 500
        }
        resp = requests.post(api_url, headers=headers, json=payload, timeout=10)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"].strip()
        return None

    def _call_openrouter(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        api_url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "meta-llama/llama-3.2-3b-instruct:free",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.85,
            "max_tokens": 500
        }
        resp = requests.post(api_url, headers=headers, json=payload, timeout=10)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"].strip()
        return None

    def _call_ollama(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        api_url = "http://localhost:11434/api/chat"
        payload = {
            "model": "llama3.2",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False
        }
        resp = requests.post(api_url, json=payload, timeout=3)
        if resp.status_code == 200:
            return resp.json()["message"]["content"].strip()
        return None

    def _dynamic_fallback_roast(self, system_prompt: str, user_prompt: str) -> str:
        is_gordon = "Gordon Ramsay" in system_prompt
        is_techbro = "Silicon Valley" in system_prompt
        is_parent = "disappointed parent" in system_prompt
        
        snippets = user_prompt.split("\n")
        data_preview = snippets[-1] if len(snippets) > 1 else "this questionable taste"
        
        if is_gordon:
            return (
                "LISTEN TO ME! LOOK AT THIS! THIS IS AN ABSOLUTE DISASTER!\n\n"
                f"You brought me '{data_preview[:60]}' and you expect me to sit here and smile? "
                "It is RAW! It has NO FLAVOR, NO PASSION, AND ZERO QUALITY CONTROL! "
                "A toddler banging pots and pans has more refined artistic standards than whatever this is! "
                "My nan could produce something with more seasoning and depth, and she's not even awake!\n\n"
                "SHUT IT DOWN! Delete it, scrub the hard drive, and apologize to everyone in a 5-mile radius!\n\n"
                "🏆 FINAL VERDICT: An absolute culinary and acoustic catastrophe. Get out of my kitchen!"
            )
        elif is_techbro:
            return (
                "Let's do a post-mortem on whatever this is, because frankly, the ROI here is deeply negative.\n\n"
                f"Looking at '{data_preview[:60]}', I'm seeing zero product-market fit and catastrophic bandwidth waste. "
                "This entire setup has negative alpha. If your life strategy was a Series A pitch deck, "
                "every VC on Sand Hill Road would pass before the title slide finished loading. "
                "Where is the synergy? Where is the leverage? This is straight-up sub-optimal grindset behavior.\n\n"
                "You need to pivot immediately. Stop burning runway on this low-tier execution.\n\n"
                "🏆 FINAL VERDICT: Negative ARR, zero scalable moat. Pivot or shut down the startup."
            )
        elif is_parent:
            return (
                "*Deep, prolonged sigh*\n\n"
                f"Look at what you're spending your time on: '{data_preview[:60]}'. "
                "Do you know what your cousin Sharma is doing right now? He's a senior surgeon with two patents and a clean GitHub. "
                "And here you are, presenting this to the world with full confidence. We gave you food, electricity, and an education, "
                "and this is how you repay our sacrifices?\n\n"
                "I'm not even angry. I'm just genuinely wondering what we did wrong.\n\n"
                "🏆 FINAL VERDICT: Sharma's son would never. Deeply disappointed."
            )
        else:
            return (
                "Bro... honestly, who hurt you? What is this actual abomination?\n\n"
                f"I just looked at '{data_preview[:60]}' and my brain cells literally filed for unemployment. "
                "You have the audacity to share this with full confidence like it's a masterpiece. "
                "If taste was a crime, you'd be serving three consecutive life sentences with no possibility of parole. "
                "Please tell me you don't show this to people in public, because I have a reputation to protect as your friend.\n\n"
                "I'm confiscating your aux cord, your keyboard, and your WiFi privileges until further notice.\n\n"
                "🏆 FINAL VERDICT: Unhinged, certified criminal offense. Please seek immediate help."
            )
