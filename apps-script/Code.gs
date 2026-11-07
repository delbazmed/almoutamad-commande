/**
 * Al Moutamad — سجل الطلبات في Google Sheets
 * يُلصق هذا الكود في: Sheet ← Extensions ← Apps Script
 * ثم Deploy ← New deployment ← Web app (Execute as: Me — Who has access: Anyone)
 */
const SHEET_NAME = 'Commandes';
const STATUSES = ['Nouveau', 'Confirmé', 'Livré', 'Annulé', 'Injoignable'];
const HEADERS = ['Date', 'N° commande', 'Statut', 'Produit', 'Réf.', 'Qualité', 'Quantité', 'Total (DA)',
  'Nom', 'Téléphone', 'Wilaya', 'Commune', 'Véhicule', 'Motorisation', 'Source'];

function doPost(e) {
  try {
    const d = JSON.parse(e.postData.contents);

    // رفض الروبوتات والبيانات غير المنطقية
    const tel = String(d.telephone || '').replace(/\D/g, '');
    const nom = clean_(d.nom);
    if (d.website || nom.length < 3 || !/^0[567]\d{8}$/.test(tel)) {
      return json_({ ok: false });
    }

    const lock = LockService.getScriptLock();
    lock.waitLock(10000);
    try {
      const sh = sheet_();
      const row = sh.getLastRow() + 1;
      sh.getRange(row, 10).setNumberFormat('@'); // يحفظ الصفر في بداية الهاتف
      sh.getRange(row, 1, 1, HEADERS.length).setValues([[
        new Date(),
        clean_(d.id),
        'Nouveau',
        clean_(d.produit),
        clean_(d.ref),
        clean_(d.qualite),
        Number(d.quantite) || '',
        Number(d.total) || '',
        nom,
        tel,
        clean_(d.wilaya),
        clean_(d.commune),
        clean_(d.vehicule),
        clean_(d.motorisation),
        clean_(d.source)
      ]]);
    } finally {
      lock.releaseLock();
    }
    return json_({ ok: true });
  } catch (err) {
    return json_({ ok: false, error: String(err) });
  }
}

function doGet() {
  return json_({ ok: true, service: 'Al Moutamad orders' });
}

function sheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]).setFontWeight('bold').setBackground('#0f2438').setFontColor('#ffffff');
    sh.setFrozenRows(1);
    sh.getRange(2, 1, 1000, 1).setNumberFormat('dd/MM/yyyy HH:mm');
    sh.getRange(2, 3, 1000, 1).setDataValidation(
      SpreadsheetApp.newDataValidation().requireValueInList(STATUSES, true).setAllowInvalid(false).build());
  }
  return sh;
}

// نص آمن: يقصّ الطول ويمنع تحويل النص إلى صيغة داخل الجدول
function clean_(v) {
  let s = String(v == null ? '' : v).trim().slice(0, 200);
  if (/^[=+\-@]/.test(s)) s = "'" + s;
  return s;
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
