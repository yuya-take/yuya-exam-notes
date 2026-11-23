// ノートの確認問題（<div class="quiz" data-answer="B">）を、選んで答え合わせできるようにする。
// build_site.py が site_src/javascripts/ に写す。JavaScript が動かなくても、
// 選択肢の一覧と、折りたたみの「答えと解説」は読める。
(function () {
  function letterOf(li) {
    var m = li.textContent.trim().match(/^([A-Z])[.．]/);
    return m ? m[1] : null;
  }

  function setup(quiz) {
    if (quiz.dataset.ready) return;
    quiz.dataset.ready = "1";
    var answers = (quiz.dataset.answer || "").split(",").map(function (s) { return s.trim(); }).filter(Boolean);
    var items = Array.prototype.slice.call(quiz.querySelectorAll(":scope > ul > li"));
    if (!answers.length || !items.length) return;

    var details = quiz.nextElementSibling;
    if (!details || details.tagName !== "DETAILS") details = null;

    var status = document.createElement("p");
    status.className = "quiz-status";
    quiz.appendChild(status);

    var picked = [];
    var done = false;

    function reset() {
      picked = [];
      done = false;
      items.forEach(function (li) { li.classList.remove("picked", "correct", "wrong", "missed"); });
      status.className = "quiz-status";
      status.textContent = answers.length > 1 ? answers.length + "つ選ぶと答え合わせします" : "選ぶと答え合わせします";
      if (details) details.open = false;
    }

    function grade() {
      done = true;
      items.forEach(function (li) {
        var l = letterOf(li);
        li.classList.remove("picked");
        if (answers.indexOf(l) >= 0) li.classList.add(picked.indexOf(l) >= 0 ? "correct" : "missed");
        else if (picked.indexOf(l) >= 0) li.classList.add("wrong");
      });
      var ok = answers.every(function (a) { return picked.indexOf(a) >= 0; });
      status.textContent = ok ? "正解" : "不正解（正解は " + answers.join("・") + "）";
      status.classList.add(ok ? "ok" : "ng");
      var again = document.createElement("button");
      again.type = "button";
      again.className = "quiz-again";
      again.textContent = "もう一度";
      again.addEventListener("click", reset);
      status.appendChild(again);
      if (details) details.open = true;
    }

    function pick(li) {
      if (done) return;
      var l = letterOf(li);
      var i = picked.indexOf(l);
      if (i >= 0) {
        picked.splice(i, 1);
        li.classList.remove("picked");
        return;
      }
      picked.push(l);
      li.classList.add("picked");
      if (picked.length === answers.length) grade();
    }

    items.forEach(function (li) {
      li.tabIndex = 0;
      li.setAttribute("role", "button");
      li.addEventListener("click", function () { pick(li); });
      li.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          pick(li);
        }
      });
    });
    reset();
  }

  function init() {
    document.querySelectorAll(".quiz").forEach(setup);
  }

  // Material の instant navigation では、ページを移るたびに document$ が通知する
  if (typeof document$ !== "undefined") document$.subscribe(init);
  else document.addEventListener("DOMContentLoaded", init);
})();
