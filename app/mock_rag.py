from __future__ import annotations

import time

from .incidents import STATE

CORPUS = {
    "intern": [
        "Các kênh tìm thực tập tốt cho sinh viên HUST bao gồm trang tuyển dụng của công ty, LinkedIn và các câu lạc bộ trong trường."
    ],
    "cv": [
        "Một CV tốt nên thể hiện rõ kết quả đạt được bằng số liệu, làm nổi bật dự án cá nhân và giữ trong 1 trang đối với sinh viên mới ra trường."
    ],
    "interview": [
        "Hãy sử dụng phương pháp STAR và chuẩn bị các ví dụ cụ thể từ dự án, bài tập lớn và kinh nghiệm làm việc nhóm."
    ],
    "gpa": [
        "GPA thấp có thể được bù đắp bằng dự án tốt, kinh nghiệm thực tập, đóng góp mã nguồn mở và thể hiện sự tiến bộ rõ ràng."
    ],
}


def retrieve(message: str) -> list[str]:
    if STATE["tool_fail"]:
        raise RuntimeError("Vector store timeout")
    if STATE["rag_slow"]:
        time.sleep(2.5)
    lowered = message.lower()
    for key, docs in CORPUS.items():
        if key in lowered:
            return docs
    return ["Hiện chưa tìm thấy nội dung phù hợp, mình sẽ trả lời dựa trên kiến thức chung nhé."]
