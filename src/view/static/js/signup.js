document.getElementById("signup-btn").addEventListener("click", async function (e) {
  e.preventDefault();

  const user = {
    name: document.getElementById("name").value,
    student_id: parseInt(document.getElementById("student_id").value),
    nickname: document.getElementById("nickname").value,
    email: document.getElementById("email").value,
    password: document.getElementById("password").value
  };

  const response = await fetch("/auth/signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(user)
  });

  if (response.ok) {
    alert("회원가입에 성공했습니다.");
    window.location.href = "/auth/login";
  } else {
    alert("회원가입에 실패했습니다.");
  }
});