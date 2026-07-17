# رفع Motion World إلى GitHub

اسم المستودع المقترح:

```text
motion-world
```

الوصف المقترح:

```text
Turn generated images into progress-controlled motion for iOS, Android, Flutter, React Native, and Web.
```

## الطريقة الأسهل: GitHub Desktop

1. فك ضغط `motion-world-v0.3.0-github-ready.zip`.
2. افتح GitHub Desktop وسجل الدخول بحسابك.
3. اختر **File → Add local repository**.
4. اختر مجلد `motion-world`.
5. إذا ظهر أن المجلد ليس Git repository، اختر **create a repository**.
6. اجعل الاسم `motion-world`.
7. اكتب أول Commit باسم:

```text
Initial public release of Motion World 0.3.0
```

8. اضغط **Publish repository**.
9. ألغِ خيار **Keep this code private** حتى يكون المستودع عامًا.
10. بعد النشر افتح تبويب Actions وتأكد أن Workflow باسم `Verify` نجح.

## عبر موقع GitHub ثم Terminal

### 1. إنشاء المستودع

افتح:

```text
https://github.com/new
```

استخدم الإعدادات التالية:

| الحقل | القيمة |
|---|---|
| Owner | `Nasser934` |
| Repository name | `motion-world` |
| Description | الوصف الموجود أعلى الصفحة |
| Visibility | Public |
| Add README | لا تحدده |
| Add .gitignore | None |
| License | None |

اضغط **Create repository**.

### 2. الرفع من macOS أو Linux

من داخل المجلد بعد فك الضغط:

```bash
cd motion-world
git init
git add .
git commit -m "Initial public release of Motion World 0.3.0"
git branch -M main
git remote add origin https://github.com/Nasser934/motion-world.git
git push -u origin main
```

### 3. الرفع من Windows PowerShell

```powershell
cd C:\path\to\motion-world
git init
git add .
git commit -m "Initial public release of Motion World 0.3.0"
git branch -M main
git remote add origin https://github.com/Nasser934/motion-world.git
git push -u origin main
```

## بعد الرفع

### إعداد About

من الصفحة الرئيسية للمستودع اضغط ترس **About** ثم أدخل:

**Description**

```text
Turn generated images into progress-controlled motion for iOS, Android, Flutter, React Native, and Web.
```

**Topics**

```text
agent-skills
codex
claude-code
higgsfield
image-to-video
ffmpeg
swiftui
jetpack-compose
flutter
react-native
scroll-animation
progress-animation
ai-video
```

### إنشاء أول Release

1. افتح **Releases**.
2. اختر **Draft a new release**.
3. أنشئ Tag باسم `v0.3.0`.
4. العنوان:

```text
Motion World 0.3.0 — First public release
```

5. أرفق ملف ZIP وملف SHA-256.
6. استخدم قسم `0.3.0` من `CHANGELOG.md` كوصف للإصدار.
7. اضغط **Publish release**.

### فحص الروابط

تأكد من عمل:

- صورة Hero.
- GIF داخل README.
- رابط MP4.
- صور 0% و50% و100%.
- روابط README العربي والإنجليزي.
- Badge الخاص بـVerify بعد انتهاء GitHub Actions.
