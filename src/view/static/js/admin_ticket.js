document.addEventListener("DOMContentLoaded", () => {
  const confirmButtons = document.querySelectorAll(".confirm-btn");

  confirmButtons.forEach((btn) => {
    btn.addEventListener("click", async () => {
      const ticketId = btn.dataset.id;

      try {
        const response = await fetch(`/ticket/${ticketId}/confirm`, {
          method: "PUT",
        });

        if (response.ok) {
          alert("입금 확인 완료");
          window.location.reload();
        } else {
          const error = await response.json();
          alert(error.detail || "처리에 실패했습니다.");
        }
      } catch (err) {
        console.error("❌ 요청 실패:", err);
        alert("서버 오류가 발생했습니다.");
      }
    });
  });
});