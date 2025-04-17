document.addEventListener("DOMContentLoaded", () => {
  const buyButtons = document.querySelectorAll(".buy-btn");

  buyButtons.forEach((btn) => {
    btn.addEventListener("click", async () => {
      const ticketId = btn.dataset.id;

      try {
        const response = await fetch(`/ticket/${ticketId}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          //body: JSON.stringify({ ticket_id: parseInt(ticketId) })
        });

        if (response.ok) {
          alert("티켓이 신청되었습니다.");
          window.location.reload();
        } else {
          const error = await response.json();
          alert(error.detail || "신청에 실패했습니다.");
        }
      } catch (err) {
        console.error("❌ 요청 실패:", err);
        alert("서버 오류가 발생했습니다.");
      }
    });
  });
});