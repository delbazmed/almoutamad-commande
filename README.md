# Al Moutamad — صفحة الطلب

الموقع: https://almoutamad-commande.web.app — أي تعديل على `main` يُنشر تلقائياً بعد فحصه.
إن كان الفحص فاشلاً فلا يُنشر شيء ويبقى الموقع الحالي سليماً (تصلك رسالة من GitHub بالسبب).

## الملفات التي تعدّلها أنت فقط
| الملف | ما فيه |
|---|---|
| `public/products.json` | المنتجات: الاسم، السعر، الجودة، الصور |
| `public/config.js` | أرقام الهاتف، رابط Google Sheets، رقم Pixel |
| `public/img/` | صور المنتجات |

لا تعدّل `public/index.html` ولا `public/geo.js`.

## إضافة منتج جديد
1. ارفع صوره إلى `public/img/` (Add file ← Upload files)، بأسماء لاتينية بلا مسافات، مثل `clio-1.jpg`.
2. في `public/products.json` انسخ منتجاً كاملاً (من `{` إلى `}`) وضع فاصلة بين المنتجين، ثم غيّر قيمه:

```json
{
  "id": "clio-plaquettes",          // اسم لاتيني قصير وفريد، هو رابط المنتج: ?p=clio-plaquettes
  "active": true,                    // false = يختفي من الموقع دون حذفه
  "name": "Plaquettes de frein avant",
  "title": "Plaquettes de frein avant — Renault Clio 4",
  "badge": "Clio 4",
  "compat": "Jeu de 4 plaquettes",
  "ref": "",
  "price": 4500,                     // رقم بدون DA، أو null لإخفاء السعر
  "quality": "adaptable",            // "origine" أو "adaptable" أو null
  "images": ["img/clio-1.jpg"],
  "vehiclePrefill": "Renault Clio 4 — ",
  "vehiclePlaceholder": "Renault Clio 4 — 2016",
  "motorisation": false,             // true = يظهر حقل Essence/Diesel
  "unit": "jeu(x)"
}
```
(احذف التعليقات `//` من نسختك، فالـ JSON لا يقبلها.)

## تطبيق الإدارة على الهاتف — `/admin/`
الرابط: https://almoutamad-commande.web.app/admin/ (أضفه إلى الشاشة الرئيسية من قائمة Chrome ← Add to Home screen).
- يضيف المنتجات ويعدّلها ويخفيها، ويرفع صورها من الهاتف (تُصغَّر تلقائياً إلى 900px).
- يعدّل أرقام واتساب والاتصال، Pixel، رابط Sheets.
- كل حفظ = commit واحد على `main` ثم نشر تلقائي (حوالي دقيقة)، وتظهر حالة النشر في التطبيق.
- زر «مشاركة»: يفتح قائمة مشاركة الهاتف بالصورة ويُنسخ النص تلقائياً (فيه رابط الطلب الخاص بالمنتج `/p/ID/` مع وسوم UTM).

### المفتاح (مرة واحدة)
GitHub ← Settings ← Developer settings ← Personal access tokens ← Fine-grained tokens ← Generate new token:
- Repository access: Only select repositories ← `almoutamad-commande` فقط.
- Permissions: Contents = Read and write، Actions = Read-only.
- Expiration: مدة محددة (مثلاً 90 يوماً).
المفتاح يُحفظ في متصفح الهاتف فقط. من يملكه يعدّل الموقع؛ يمكن إلغاؤه في أي وقت من نفس الصفحة.

### ما يُولَّد تلقائياً عند النشر
`scripts/build_pages.py` ينشئ لكل منتج صفحة `/p/ID/` بمعاينة فيسبوك خاصة (عنوان + صورة 1200×630). هذه الملفات غير محفوظة في المستودع.

## سجل الطلبات (Firestore) — شاشة «الطلبات» في Ali_Pub
- الموقع يكتب كل طلب في مجموعة `orders` بمشروع `almoutamad-commande` (بالإضافة إلى رسالة واتساب).
- القواعد المرجعية في `firestore.rules`: الزبون يستطيع إنشاء طلب بحقول صالحة فقط، ولا يقرأ شيئاً. المدير (بريد محدد) يقرأ ويغيّر الحالة ويحذف.
- التفعيل: مفتاح Firebase (Web API Key) يوضع في إعدادات Ali_Pub، وتسجيل الدخول بالبريد وكلمة السر المنشأين في Authentication.
- القواعد تُلصق يدوياً في Firebase Console (لا تُنشر تلقائياً).

## روابط الإعلانات
- منتج واحد (الأفضل لمعاينة فيسبوك): `https://almoutamad-commande.web.app/p/ID/?utm_source=facebook&utm_campaign=NOM`
- كل القطع: `https://almoutamad-commande.web.app/?utm_source=facebook`
- إن كان في الموقع منتج واحد فقط فالرابط بلا `p` يفتحه مباشرة.

## سجل الطلبات في Google Sheets
انظر `apps-script/Code.gs`. بعد إنشاء التطبيق ضع رابطه (ينتهي بـ `/exec`) في `sheetUrl` داخل `config.js`.
