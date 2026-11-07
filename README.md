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

## روابط الإعلانات
- منتج واحد: `https://almoutamad-commande.web.app/?p=ID&utm_source=facebook&utm_campaign=NOM`
- كل القطع: `https://almoutamad-commande.web.app/?utm_source=facebook`
- إن كان في الموقع منتج واحد فقط فالرابط بلا `p` يفتحه مباشرة.

## سجل الطلبات في Google Sheets
انظر `apps-script/Code.gs`. بعد إنشاء التطبيق ضع رابطه (ينتهي بـ `/exec`) في `sheetUrl` داخل `config.js`.
