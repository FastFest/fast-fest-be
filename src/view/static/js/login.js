// document.addEventListener("DOMContentLoaded", () => {
//   const loginBtn = document.getElementById("login-btn");
//
//   loginBtn.addEventListener("click", async (e) => {
//     e.preventDefault();
//
//     const email = document.getElementById("loginEmail").value;
//     const password = document.getElementById("loginPassword").value;
//
//     const user = {
//       email,
//       password
//     };
//
//     try {
//       const response = await fetch("/auth/login", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json"
//         },
//         credentials: "include",
//         body: JSON.stringify(user)
//       });
//       console.log("2: fetch 응답 도착", response.status);
//       if (response.ok) {
//         alert("hello");
//         console.log("hello")
//         //window.location.href = "/";  // 로그인 성공 시 리다이렉트할 경로
//       } else {
//         const data = await response.json();
//         alert(data.detail || "로그인에 실패했습니다.");
//       }
//     } catch (error) {
//       alert("서버 오류가 발생했습니다.");
//       console.error(error);
//     }
//   });
// });

document.addEventListener("DOMContentLoaded", () => {
    const loginBtn = document.getElementById("login-btn");

    if (!loginBtn) {
      console.error("❗ login-btn 요소를 찾을 수 없습니다.");
      return;
    }

    loginBtn.addEventListener("click", async (e) => {
      e.preventDefault();
      console.log("🔍 로그인 버튼 클릭됨");

      const email = document.getElementById("loginEmail")?.value;
      const password = document.getElementById("loginPassword")?.value;

      if (!email || !password) {
        alert("이메일과 비밀번호를 모두 입력해주세요.");
        return;
      }

      const user = { email, password };

      try {
        console.log("🚀 fetch 시작");

        const response = await fetch("/auth/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          credentials: "include",
          body: JSON.stringify(user)
        });

        console.log("✅ fetch 응답 도착", response.status);

        if (response.ok) {
          alert("로그인 성공!");
          window.location.href = "/";
        } else {
          const data = await response.json();
          alert(data.detail || "로그인 실패");
        }
      } catch (error) {
        alert("서버 오류가 발생했습니다.");
        console.error("❌ fetch 에러:", error);
      }
    });
  });