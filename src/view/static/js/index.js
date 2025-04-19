document.addEventListener("DOMContentLoaded", () => {
  const logoutButton = document.getElementById("logoutButton");

  logoutButton.addEventListener("click", async () => {
    document.cookie = "access_token=; Max-Age=0; path=/";
    window.location.href = "/auth/login";
  });
});