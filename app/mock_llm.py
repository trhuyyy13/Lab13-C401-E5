from __future__ import annotations

import os
import random
import time
from dataclasses import dataclass

from .incidents import STATE

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None


@dataclass
class FakeUsage:
    input_tokens: int
    output_tokens: int


@dataclass
class FakeResponse:
    text: str
    usage: FakeUsage
    model: str


SYSTEM_PROMPT = (
    "Bạn là một trợ lý AI về định hướng nghề nghiệp dành cho sinh viên HUST. "
    "Hỗ trợ tìm kiếm thực tập, cải thiện CV, chuẩn bị phỏng vấn và xây dựng lộ trình nghề nghiệp. "
    "Hãy trả lời ngắn gọn, thực tế và tránh tiết lộ dữ liệu cá nhân."
)


class FakeLLM:
    def __init__(self, model: str = "gpt-4o-mini") -> None:
        self.model = model
        api_key = os.getenv("OPENAI_API_KEY")
        self._client = OpenAI(api_key=api_key) if (OpenAI is not None and api_key) else None

    def generate(self, prompt: str) -> FakeResponse:
        if self._client is not None:
            try:
                response = self._client.responses.create(
                    model=self.model,
                    input=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt},
                    ],
                )
                usage = response.usage
                input_tokens = getattr(usage, "input_tokens", max(20, len(prompt) // 4))
                output_tokens = getattr(usage, "output_tokens", 120)
                if STATE["cost_spike"]:
                    output_tokens *= 4

                text = (response.output_text or "").strip()
                if not text:
                    text = "Xin loi, he thong dang ban. Vui long thu lai sau it phut."

                return FakeResponse(
                    text=text,
                    usage=FakeUsage(input_tokens=input_tokens, output_tokens=output_tokens),
                    model=self.model,
                )
            except Exception:
                # Fallback keeps the lab runnable offline or when OpenAI is unavailable.
                return self._fallback_generate(prompt)

        return self._fallback_generate(prompt)

    def _fallback_generate(self, prompt: str) -> FakeResponse:
        time.sleep(0.15)
        input_tokens = max(20, len(prompt) // 4)
        output_tokens = random.randint(80, 180)
        if STATE["cost_spike"]:
            output_tokens *= 4
        answer = (
            "Chào bạn, mình là AI Career Assistant dành cho sinh viên HUST. "
            "Mình có thể hỗ trợ bạn tìm kiếm cơ hội thực tập, gợi ý cải thiện CV, "
            "luyện phỏng vấn và xây dựng lộ trình nghề nghiệp phù hợp với ngành bạn quan tâm."
        )
        return FakeResponse(text=answer, usage=FakeUsage(input_tokens, output_tokens), model=self.model)
