document.addEventListener("DOMContentLoaded", () => {
  const submitBtn = document.getElementById("submit-answer");
  const contentInput = document.getElementById("answer-content");

  submitBtn.addEventListener("click", async () => {
    const content = contentInput.value.trim();
    if (!content) {
      alert("답변 내용을 입력해주세요.");
      return;
    }

    const pathParts = window.location.pathname.split("/");
    const questionId = pathParts[pathParts.length - 1] || pathParts[pathParts.length - 2]; // 경로 끝이 슬래시로 끝날 수도 있음

    try {
      const response = await fetch(`/qna/answer`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ content , question_id: questionId}),
      });

      if (response.ok) {
        window.location.reload();  // ✅ 페이지 새로고침
      } else {
        const error = await response.json();
        alert(error.detail || "답변 등록에 실패했습니다.");
      }
    } catch (err) {
      console.error("❌ 요청 실패:", err);
      alert("서버 오류가 발생했습니다.");
    }
  });
});