// 確認問題（<div class="quiz" data-answer="B">）を、選んで答え合わせできるようにする。
// build_site.py が site_src/javascripts/ に写す。JavaScript が動かなくても、
// 選択肢の一覧と、折りたたみの「答えと解説」は読める。
//
// ページに <div class="exam-start" data-minutes="120" data-pass="72"></div> があるときは
// 模擬試験のモードになる。1問ずつは採点せず、最後の「採点する」でまとめて採点し、
// 正答率・ドメイン別の結果を出す。選んだ答えと開始時刻は、このブラウザに保存する。
// ドメインの名前は exam-start の data-domains（"1:名前|2:名前|…"）で渡す。無ければ CCAR-F の名前を使う。
(function () {
  var DOMAINS = {
    "1": "エージェントの構成とオーケストレーション",
    "2": "ツール設計と MCP の組み込み",
    "3": "Claude Code の設定とワークフロー",
    "4": "プロンプトエンジニアリングと構造化出力",
    "5": "コンテキスト管理と信頼性"
  };

  function letterOf(li) {
    var m = li.textContent.trim().match(/^([A-Z])[.．]/);
    return m ? m[1] : null;
  }

  function answersOf(quiz) {
    return (quiz.dataset.answer || "").split(",").map(function (s) { return s.trim(); }).filter(Boolean);
  }

  function itemsOf(quiz) {
    return Array.prototype.slice.call(quiz.querySelectorAll(":scope > ul > li"));
  }

  function detailsOf(quiz) {
    var d = quiz.nextElementSibling;
    return d && d.tagName === "DETAILS" ? d : null;
  }

  function store(key, value) {
    try {
      if (value === undefined) return JSON.parse(localStorage.getItem(key) || "null");
      if (value === null) localStorage.removeItem(key);
      else localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
      return null;
    }
  }

  // 1問ずつ答え合わせする（ノートの確認問題）
  function setupPractice(quiz) {
    var answers = answersOf(quiz);
    var items = itemsOf(quiz);
    if (!answers.length || !items.length) return;
    var details = detailsOf(quiz);
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
      markResult(items, answers, picked);
      var ok = isCorrect(answers, picked);
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

    bindItems(items, function (li) {
      if (done) return;
      togglePick(li, picked);
      if (picked.length === answers.length) grade();
    });
    reset();
  }

  function bindItems(items, onPick) {
    items.forEach(function (li) {
      li.tabIndex = 0;
      li.setAttribute("role", "button");
      li.addEventListener("click", function () { onPick(li); });
      li.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          onPick(li);
        }
      });
    });
  }

  function togglePick(li, picked) {
    var l = letterOf(li);
    var i = picked.indexOf(l);
    if (i >= 0) {
      picked.splice(i, 1);
      li.classList.remove("picked");
    } else {
      picked.push(l);
      li.classList.add("picked");
    }
  }

  function isCorrect(answers, picked) {
    return picked.length === answers.length && answers.every(function (a) { return picked.indexOf(a) >= 0; });
  }

  function markResult(items, answers, picked) {
    items.forEach(function (li) {
      var l = letterOf(li);
      li.classList.remove("picked");
      if (answers.indexOf(l) >= 0) li.classList.add(picked.indexOf(l) >= 0 ? "correct" : "missed");
      else if (picked.indexOf(l) >= 0) li.classList.add("wrong");
    });
  }

  // 模擬試験のモード
  function setupExam(start) {
    var quizzes = Array.prototype.slice.call(document.querySelectorAll(".quiz"));
    var minutes = parseInt(start.dataset.minutes || "120", 10);
    var pass = parseInt(start.dataset.pass || "72", 10);
    if (start.dataset.domains) {
      DOMAINS = {};
      start.dataset.domains.split("|").forEach(function (s) {
        var i = s.indexOf(":");
        if (i > 0) DOMAINS[s.slice(0, i).trim()] = s.slice(i + 1).trim();
      });
    }
    var key = "exam:" + location.pathname;
    var saved = store(key) || {};
    var state = { picks: saved.picks || {}, startedAt: saved.startedAt || null, graded: !!saved.graded };
    var timerId = null;

    function save() { store(key, state); }

    var bar = document.createElement("div");
    bar.className = "exam-bar";
    var info = document.createElement("span");
    var timer = document.createElement("span");
    timer.className = "exam-timer";
    var startBtn = button("開始", startExam);
    var gradeBtn = button("採点する", gradeExam);
    var resetBtn = button("最初から解き直す", resetExam);
    bar.appendChild(info);
    bar.appendChild(timer);
    bar.appendChild(startBtn);
    bar.appendChild(gradeBtn);
    bar.appendChild(resetBtn);
    start.appendChild(bar);
    var result = document.createElement("div");
    result.className = "exam-result";
    start.appendChild(result);

    var bottom = document.createElement("p");
    bottom.className = "exam-bottom";
    bottom.appendChild(button("採点する", gradeExam));
    var last = quizzes[quizzes.length - 1];
    var anchor = (last && detailsOf(last)) || last;
    if (anchor) anchor.parentNode.insertBefore(bottom, anchor.nextSibling);

    function button(label, fn) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "exam-btn";
      b.textContent = label;
      b.addEventListener("click", fn);
      return b;
    }

    quizzes.forEach(function (quiz, idx) {
      var answers = answersOf(quiz);
      var items = itemsOf(quiz);
      var picked = state.picks[idx] || (state.picks[idx] = []);
      items.forEach(function (li) { if (picked.indexOf(letterOf(li)) >= 0) li.classList.add("picked"); });
      bindItems(items, function (li) {
        if (state.graded) return;
        if (!state.startedAt) startExam();
        var l = letterOf(li);
        if (picked.indexOf(l) < 0 && picked.length >= answers.length) {
          // 選べる数を超えたら、いちばん古い選択を外す
          var old = picked.shift();
          items.forEach(function (x) { if (letterOf(x) === old) x.classList.remove("picked"); });
        }
        togglePick(li, picked);
        save();
        refresh();
      });
    });

    function answeredCount() {
      return quizzes.filter(function (q, i) { return (state.picks[i] || []).length === answersOf(q).length; }).length;
    }

    function refresh() {
      info.textContent = "回答済み " + answeredCount() + " / " + quizzes.length + " 問";
      startBtn.style.display = state.startedAt || state.graded ? "none" : "";
      gradeBtn.style.display = state.graded ? "none" : "";
      bottom.style.display = state.graded ? "none" : "";
      resetBtn.style.display = state.graded || state.startedAt ? "" : "none";
      document.body.classList.toggle("exam-graded", state.graded);
    }

    function tick() {
      if (!state.startedAt) { timer.textContent = "制限時間 " + minutes + "分"; return; }
      var left = state.startedAt + minutes * 60000 - Date.now();
      if (state.graded) { timer.textContent = ""; return; }
      if (left <= 0) {
        timer.textContent = "時間切れ";
        timer.classList.add("over");
        return;
      }
      var m = Math.floor(left / 60000), s = Math.floor((left % 60000) / 1000);
      timer.textContent = "残り " + m + ":" + (s < 10 ? "0" : "") + s;
    }

    function startExam() {
      if (state.startedAt) return;
      state.startedAt = Date.now();
      save();
      refresh();
    }

    function gradeExam() {
      var unanswered = quizzes.length - answeredCount();
      if (unanswered && !window.confirm("まだ " + unanswered + " 問が答えていません。採点しますか？（答えていない問題は誤答になります）")) return;
      state.graded = true;
      state.finishedAt = Date.now();
      save();
      showResult();
      refresh();
      start.scrollIntoView({ behavior: "smooth" });
    }

    function resetExam() {
      if (!window.confirm("選んだ答えを消して、最初から解き直しますか？")) return;
      store(key, null);
      location.reload();
    }

    function showResult() {
      var total = 0, byDomain = {};
      quizzes.forEach(function (quiz, idx) {
        var answers = answersOf(quiz);
        var picked = state.picks[idx] || [];
        var ok = isCorrect(answers, picked);
        if (ok) total++;
        var d = quiz.dataset.domain || "?";
        byDomain[d] = byDomain[d] || { ok: 0, n: 0 };
        byDomain[d].n++;
        if (ok) byDomain[d].ok++;
        markResult(itemsOf(quiz), answers, picked);
        var st = document.createElement("p");
        st.className = "quiz-status " + (ok ? "ok" : "ng");
        st.textContent = ok ? "正解" : "不正解（正解は " + answers.join("・") + "）";
        quiz.appendChild(st);
        var det = detailsOf(quiz);
        if (det && !ok) det.open = true;
      });
      var rate = Math.round((total / quizzes.length) * 1000) / 10;
      var used = state.startedAt ? Math.round(((state.finishedAt || Date.now()) - state.startedAt) / 60000) : null;
      var html = "<p class='exam-score " + (rate >= pass ? "ok" : "ng") + "'>" + total + " / " + quizzes.length + " 問正解（" + rate + "%）</p>";
      html += "<p>目安の合格ライン: 正答率 " + pass + "%（本番はスケールスコア 720。正答率からの換算は公開されていないので、あくまで目安）";
      if (used !== null) html += "。かかった時間: " + used + "分 / " + minutes + "分";
      html += "</p><table><thead><tr><th>ドメイン</th><th>正解</th><th>正答率</th></tr></thead><tbody>";
      Object.keys(byDomain).sort().forEach(function (d) {
        var r = byDomain[d];
        var p = Math.round((r.ok / r.n) * 100);
        html += "<tr><td><span class='domain-dot d" + d + "'></span>" + d + ". " + (DOMAINS[d] || "") + "</td><td>" + r.ok + " / " + r.n + "</td><td class='" + (p >= pass ? "ok" : "ng") + "'>" + p + "%</td></tr>";
      });
      html += "</tbody></table><p>間違えた問題は、下で解説が開いています。</p>";
      result.innerHTML = html;
    }

    if (state.graded) showResult();
    refresh();
    tick();
    timerId = setInterval(tick, 1000);
    // instant navigation でページを離れたら止める
    if (typeof document$ !== "undefined") {
      var sub = document$.subscribe(function () {
        if (!document.body.contains(start)) { clearInterval(timerId); if (sub) sub.unsubscribe(); }
      });
    }
  }

  function init() {
    var start = document.querySelector(".exam-start");
    // instant navigation では body が使い回されるので、ページごとに付け直す
    document.body.classList.toggle("exam-mode", !!start);
    if (!start) document.body.classList.remove("exam-graded");
    if (start) {
      if (start.dataset.ready) return;
      start.dataset.ready = "1";
      setupExam(start);
      return;
    }
    document.querySelectorAll(".quiz").forEach(function (quiz) {
      if (quiz.dataset.ready) return;
      quiz.dataset.ready = "1";
      setupPractice(quiz);
    });
  }

  // Material の instant navigation では、ページを移るたびに document$ が通知する
  if (typeof document$ !== "undefined") document$.subscribe(init);
  else document.addEventListener("DOMContentLoaded", init);
})();
