document.addEventListener("DOMContentLoaded", () => {
  const pass = document.querySelector('input[name="password"]');
  if (pass) {
    pass.addEventListener("input", () => {
      if (pass.value.length < 8)
        pass.setCustomValidity("Use 8 characters or more for your password");
      else
        pass.setCustomValidity("");
    });
  }
});
