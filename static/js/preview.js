document.addEventListener('DOMContentLoaded', () => {
  const file = document.querySelector('input[type="file"][name$="image"]');
  const img = document.getElementById('preview');
  if (!file || !img) return;
  file.addEventListener('change', () => {
    const f = file.files && file.files[0];
    if (!f) { img.style.display='none'; img.src=''; return; }
    const url = URL.createObjectURL(f);
    img.src = url;
    img.style.display = 'block';
    img.onload = () => URL.revokeObjectURL(url);
  });
});
