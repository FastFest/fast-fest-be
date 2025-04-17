document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("question-form");
  const submitBtn = document.getElementById("submit-btn");

  submitBtn.addEventListener("click", async () => {
    const title = document.getElementById("title").value.trim();
    const content = document.getElementById("content").value.trim();

    if (!title || !content) {
      alert("제목과 내용을 모두 입력해주세요.");
      return;
    }

    try {
      const response = await fetch("/qna/question", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title,
          content,
        }),
      });

      if (response.ok) {
        alert("질문이 등록되었습니다.");
        window.location.href = "/qna";
      } else {
        const error = await response.json();
        alert(error.detail || "질문 등록에 실패했습니다.");
      }
    } catch (err) {
      console.error("❌ 요청 실패:", err);
      alert("서버 오류가 발생했습니다.");
    }
  });
});