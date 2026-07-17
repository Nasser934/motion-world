<p align="center">
  <img src="docs/media/hero.svg" alt="Motion World" width="100%" />
</p>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="#البدء-خلال-دقيقة">البدء خلال دقيقة</a> ·
  <a href="#كيف-يعمل-خط-الإنتاج">خط الإنتاج</a> ·
  <a href="#ربط-الحركة-بالتطبيق">ربط التطبيق</a> ·
  <a href="docs/PUBLISH_AR.md">خطوات الرفع إلى GitHub</a>
</p>

# Motion World

**Motion World يحوّل الصور التي تنشئها أو ترفعها إلى حركة يمكن لتطبيقك التحكم بها.** يستطيع إنشاء الصور عبر ChatGPT أو Codex، وإرسال الإطارات المعتمدة إلى Higgsfield أو مزود فيديو آخر، ثم معالجة الفيديو وإنشاء ملفات تشغيل مناسبة لـiOS وAndroid وFlutter وReact Native والويب.

الناتج ليس فيديو تشغيل تلقائي فقط. يمكنك ربط الحركة بالوقت، والعد التنازلي، والعدد، والتمرير، والسحب، والحساس، وحالة التطبيق، وتقدم الشبكة، والصوت، أو أي قيمة بين `0` و`1`.

```text
قيمة التطبيق → progress من 0 إلى 1 → Motion Runtime → الحالة البصرية الدقيقة
```

## شاهد النتيجة

<p align="center">
  <img src="docs/media/motion-world-demo.gif" alt="عرض Motion World" width="800" />
</p>

<p align="center">
  <a href="docs/media/motion-world-demo.mp4"><strong>فتح نسخة MP4</strong></a>
</p>

<table>
  <tr><th align="center">0%</th><th align="center">50%</th><th align="center">100%</th></tr>
  <tr>
    <td><img src="docs/media/demo-start.webp" alt="بداية الحركة" /></td>
    <td><img src="docs/media/demo-middle.webp" alt="منتصف الحركة" /></td>
    <td><img src="docs/media/demo-end.webp" alt="نهاية الحركة" /></td>
  </tr>
</table>

## ما المشكلة التي يحلها؟

منصات الفيديو بالذكاء الاصطناعي تنتج ملف فيديو. التطبيق يحتاج حالة بصرية يمكن فتحها مباشرة عند أي نسبة.

مثال: إذا كانت جلسة مدتها 20 دقيقة ووصل المستخدم إلى الدقيقة 8، يجب أن يعرض التطبيق حالة 40% فورًا بعد فتحه، لا أن يعيد تشغيل الفيديو من البداية.

Motion World يفصل العمل إلى خمسة أجزاء:

| الجزء | الوظيفة |
|---|---|
| مزود الصور | إنشاء صور البداية والنهاية والمراجع |
| مزود الفيديو | تحريك الصور المعتمدة |
| معالج الحركة | تحويل الفيديو إلى Scrub أو إطارات أو Atlas |
| Runtime | عرض الحالة على كل نظام |
| Progress Driver | تحويل بيانات التطبيق إلى نسبة من 0 إلى 1 |

## كيف يعمل خط الإنتاج؟

<p align="center">
  <img src="docs/media/architecture.svg" alt="معمارية Motion World" width="100%" />
</p>

### 1. إنشاء الصور

يمكن استخدام:

- إنشاء الصور داخل ChatGPT.
- `image_gen` عبر Codex.
- ملفات محلية جاهزة.
- أي منصة صور تحفظ الناتج كملف.

### 2. إنشاء الفيديو

يدعم المشروع:

- Higgsfield CLI.
- أي CLI آخر عبر `generic_shell`.
- رفع يدوي إلى أي منصة عبر `manual`.
- عقد `generic_http` لإضافة API مخصص.

### 3. تحويل الفيديو إلى ملفات تطبيق

<p align="center">
  <img src="docs/media/output-matrix.svg" alt="صيغ الحركة" width="100%" />
</p>

| الصيغة | الاستخدام |
|---|---|
| Scrub MP4 | حركة سينمائية يتحكم التطبيق بزمنها |
| Frame Sequence | فتح أي حالة بدقة داخل التطبيق الأصلي |
| Sprite Atlas | حركات قصيرة بحجم وقراءات ملفات أقل |
| Posters | Reduce Motion والأجهزة الضعيفة والمعاينات |

### 4. ربط الحركة بالتطبيق

يدعم:

- SwiftUI.
- Jetpack Compose.
- Flutter.
- React Native.
- JavaScript للويب.

## البدء خلال دقيقة

### تثبيت المتطلبات

macOS:

```bash
brew install ffmpeg python
python3 -m pip install Pillow
```

Ubuntu:

```bash
sudo apt update
sudo apt install -y ffmpeg python3 python3-pip
python3 -m pip install --user Pillow
```

### تثبيت المهارة في Codex

```bash
npx skills add Nasser934/motion-world -a codex
```

أو اختيار النظام يدويًا:

```bash
npx skills add Nasser934/motion-world
```

### إنشاء مشروع

```bash
python3 skills/motion-world/scripts/init_project.py my-motion \
  --preset generic-cinematic
```

### فحص المشروع

```bash
python3 skills/motion-world/scripts/validate_project.py \
  my-motion/motion-project.json
```

### مشاهدة أوامر مزود الفيديو قبل صرف الرصيد

```bash
python3 skills/motion-world/scripts/provider_runner.py \
  my-motion/motion-project.json \
  --plan
```

### تشغيل المزود

```bash
python3 skills/motion-world/scripts/provider_runner.py \
  my-motion/motion-project.json \
  --execute
```

### معالجة الفيديو

```bash
python3 skills/motion-world/scripts/prepare_motion.py \
  --input my-motion/provider-output/source.mp4 \
  --out my-motion/build \
  --profiles scrub,frames,atlas,posters \
  --fps 30 \
  --frame-count 180
```

### إنشاء ملفات الدمج للأنظمة

```bash
python3 skills/motion-world/scripts/install_runtime_adapters.py \
  my-motion/motion-project.json
```

## مصادر التحكم

| المصدر | المعادلة |
|---|---|
| الوقت | `(now - start) / (end - start)` |
| العد التنازلي | `1 - remaining / total` |
| العدد | `(current - min) / (goal - min)` |
| التمرير | `(offset - start) / distance` |
| السحب | `translation / allowedDistance` |
| حالة التطبيق | تحويل الحالات إلى نقاط بين 0 و1 |
| الشبكة | `transferredBytes / totalBytes` |

## ربط الحركة بالتطبيق

SwiftUI:

```swift
let progress = MotionProgress.elapsed(
    now: Date(),
    start: session.startDate,
    end: session.endDate
)

FrameSequenceView(
    progress: progress,
    frameCount: 180,
    reducedMotion: accessibilityReduceMotion
) { index in
    String(format: "frame_%04d", index)
}
```

Web:

```js
const runtime = new ScrubVideoRuntime(video);
runtime.setProgress(0.42);
```

## قواعد مهمة

- التطبيق هو مصدر الحقيقة، وليس انتهاء الفيديو.
- يجب أن تعمل الحركة عند فتح أي نسبة مباشرة.
- لا تضع النص داخل الصور.
- أنشئ نسخة 9:16 للهاتف بدل قص نسخة 16:9 عند وجود عناصر مهمة.
- استخدم Posters أو Crossfade عند تفعيل Reduce Motion.
- افحص الحجم والأداء على جهاز فعلي.

## سُكون

سُكون موجود كمثال فقط داخل:

```text
skills/motion-world/references/examples/sukun-oasis.motion-project.json
```

المهارة مستقلة ولا توجد داخل مستودع سُكون ولا تعتمد عليه.

## الترخيص

MIT. راجع [`LICENSE`](LICENSE) و[`NOTICE`](NOTICE).
