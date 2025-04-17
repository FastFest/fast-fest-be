document.addEventListener("DOMContentLoaded", () => {
  const submitBtn = document.getElementById("submit-ticket");

  submitBtn.addEventListener("click", async () => {
    const title = document.getElementById("title").value.trim();
    const quantity = parseInt(document.getElementById("quantity").value);
    const price = parseInt(document.getElementById("price").value);

    if (!title || isNaN(quantity) || isNaN(price)) {
      alert("모든 항목을 정확히 입력해주세요.");
      return;
    }

    try {
      const response = await fetch("/ticket", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          title,
          quantity,
          price
        })
      });

      if (response.ok) {
        alert("티켓이 성공적으로 생성되었습니다.");
        window.location.href = "/ticket";
      } else {
        const error = await response.json();
        alert(error.detail || "티켓 생성 실패");
      }
    } catch (err) {
      console.error("❌ 요청 실패:", err);
      alert("서버 오류가 발생했습니다.");
    }
  });
});