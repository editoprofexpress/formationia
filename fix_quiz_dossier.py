#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standardize quiz behavior for dossier-pattern quiz modules (02, 06, 09).
These share the same quiz code pattern: showQuiz() / answerQuiz() / submitQuiz().

Changes applied:
1. Submit button starts DISABLED until all questions answered
2. answerQuiz() enables submit when all questions are answered
3. submitQuiz() on FAILURE: shows only score + retry button (no answer highlights, no explanations)
4. submitQuiz() on SUCCESS (>=70%): shows highlights + explanations + unlocks certificate
5. Adds retryQuiz() function to reset quiz to blank state
"""

import re
import os

BASE = '/home/user/formationia'

# ─────────────────────────────────────────────────────────────
# NEW answerQuiz: same visual behavior + enable submit when done
# ─────────────────────────────────────────────────────────────

OLD_ANSWER_QUIZ = """function answerQuiz(qIdx,oIdx){
  quizAnswers[qIdx]=oIdx;
  document.querySelectorAll(`.opt[data-q="${qIdx}"]`).forEach(el=>{
    el.classList.remove('selected');
    if(parseInt(el.dataset.o)===oIdx) el.classList.add('selected');
  });
}"""

NEW_ANSWER_QUIZ = """function answerQuiz(qIdx,oIdx){
  quizAnswers[qIdx]=oIdx;
  document.querySelectorAll(`.opt[data-q="${qIdx}"]`).forEach(el=>{
    el.classList.remove('selected');
    if(parseInt(el.dataset.o)===oIdx) el.classList.add('selected');
  });
  // Enable submit button when all questions answered
  if(Object.keys(quizAnswers).length===quizQuestions.length){
    const btn=$('quiz-submit-btn');
    if(btn){btn.disabled=false;btn.style.opacity='1';btn.style.cursor='pointer';}
  }
}"""

# ─────────────────────────────────────────────────────────────
# NEW submitQuiz template (success message extracted per file)
# ─────────────────────────────────────────────────────────────

def build_new_submit_quiz(success_msg, neon_color='var(--neon-green)'):
    return f"""function submitQuiz(){{
  let score=0;
  quizQuestions.forEach((q,i)=>{{ if(quizAnswers[i]===q.correct) score++; }});
  const pct=Math.round(score/quizQuestions.length*100);
  state.quizScore=score; state.quizTotal=quizQuestions.length;
  finalScore=pct;

  $('quiz-submit-btn').style.display='none';

  if(pct>=70){{
    // Success: show highlights + explanations
    quizQuestions.forEach((q,i)=>{{
      const userAns=quizAnswers[i];
      const opts=document.querySelectorAll(`.opt[data-q="${{i}}"]`);
      opts.forEach(el=>{{
        const oIdx=parseInt(el.dataset.o);
        el.style.pointerEvents='none';
        if(oIdx===q.correct) el.classList.add('correct');
        if(oIdx===userAns&&userAns!==q.correct) el.classList.add('wrong');
      }});
      $('explain-'+i).classList.add('show');
    }});
    $('quiz-result').innerHTML=`
    <div class="callout ok" style="text-align:center;padding:30px">
      <h3 style="color:{neon_color};margin-bottom:15px">Félicitations !</h3>
      <p style="font-size:1.3em;margin-bottom:10px">${{score}}/${{quizQuestions.length}} — <strong>${{pct}}%</strong></p>
      <p style="line-height:1.6">{success_msg}</p>
    </div>`;
    unlockCertificate();
  }} else {{
    // Failure: show only score + retry (no answer details)
    $('quiz-result').innerHTML=`
    <div class="callout warn" style="text-align:center;padding:30px">
      <h3 style="color:var(--warn);margin-bottom:15px">Score insuffisant</h3>
      <p style="font-size:1.3em;margin-bottom:10px">${{score}}/${{quizQuestions.length}} — <strong>${{pct}}%</strong></p>
      <p style="line-height:1.6">Il faut au moins 70% pour valider. Réessayez !</p>
      <button class="btn" onclick="retryQuiz()" style="margin-top:20px;background:{neon_color};color:#000;padding:12px 30px">↺ Réessayer</button>
    </div>`;
  }}
}}

function retryQuiz(){{
  Object.keys(quizAnswers).forEach(k => delete quizAnswers[k]);
  showQuiz();
}}"""


# ─────────────────────────────────────────────────────────────
# PROCESSING
# ─────────────────────────────────────────────────────────────

# Per-module configuration
MODULE_CONFIG = {
    'module-02-donnees-sous-influence.html': {
        'success_msg': "Vous avez démontré une solide compréhension de l'apprentissage machine, des données et des biais. Votre attestation est débloquée !",
        'neon_color': 'var(--neon-green)',
        'btn_class': 'btn green',
    },
    'module-06-iteration-amelioration.html': {
        'success_msg': "Vous maîtrisez les techniques de prompt engineering et d'itération. Votre attestation est débloquée !",
        'neon_color': 'var(--neon-green)',
        'btn_class': 'btn green',
    },
    'module-09-hallucinations.html': {
        'success_msg': "Vous avez démontré une solide compréhension des hallucinations IA et des techniques de vérification. Votre attestation est débloquée !",
        'neon_color': 'var(--neon-yellow)',
        'btn_class': 'btn yellow',
    },
}


def fix_submit_button_in_showquiz(content, btn_class):
    """Add disabled attribute + opacity to the quiz submit button."""
    old_btn = f'<button class="{btn_class}" id="quiz-submit-btn" onclick="submitQuiz()" style="font-size:1.1em;padding:15px 40px">Valider mes réponses</button>'
    new_btn = f'<button class="{btn_class}" id="quiz-submit-btn" onclick="submitQuiz()" style="font-size:1.1em;padding:15px 40px;opacity:0.5;cursor:not-allowed;" disabled>Valider mes réponses</button>'
    if old_btn in content:
        return content.replace(old_btn, new_btn)
    # If already has disabled, skip
    if 'disabled' in content and 'quiz-submit-btn' in content:
        return content
    return content


def fix_answer_quiz(content):
    """Replace answerQuiz with version that enables submit when all answered."""
    if 'Enable submit button when all questions answered' in content:
        return content  # already updated
    return content.replace(OLD_ANSWER_QUIZ, NEW_ANSWER_QUIZ)


def extract_success_message(content):
    """Extract the success message from existing submitQuiz."""
    m = re.search(
        r"pct>=70\s*\?\s*'([^']+)'\s*:\s*'Il faut",
        content
    )
    if m:
        return m.group(1)
    return None


def find_submit_quiz_end(content, start):
    """Find the end of the submitQuiz function by brace counting."""
    depth = 0
    i = start
    in_func = False
    while i < len(content):
        c = content[i]
        if c == '{':
            depth += 1
            in_func = True
        elif c == '}':
            depth -= 1
            if in_func and depth == 0:
                return i + 1
        i += 1
    return -1


def fix_submit_quiz(content, config):
    """Replace the submitQuiz function with new behavior."""
    if 'Success: show highlights' in content:
        return content  # already updated

    # Find and replace the old submitQuiz function
    start = content.find('function submitQuiz(){')
    if start == -1:
        start = content.find('function submitQuiz() {')
    if start == -1:
        print('  WARNING: submitQuiz not found')
        return content

    end = find_submit_quiz_end(content, start)
    if end == -1:
        print('  WARNING: could not find end of submitQuiz')
        return content

    new_code = build_new_submit_quiz(config['success_msg'], config['neon_color'])
    return content[:start] + new_code + content[end:]


def process_file(filename, config):
    filepath = os.path.join(BASE, filename)
    print(f'\nProcessing {filename} ...')

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    content = fix_submit_button_in_showquiz(content, config['btn_class'])
    content = fix_answer_quiz(content)
    content = fix_submit_quiz(content, config)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  ✓ Updated')
    else:
        print(f'  - No changes needed')

    return content != original


if __name__ == '__main__':
    changed = 0
    for fn, cfg in MODULE_CONFIG.items():
        if process_file(fn, cfg):
            changed += 1
    print(f'\nDone. {changed}/{len(MODULE_CONFIG)} files updated.')
