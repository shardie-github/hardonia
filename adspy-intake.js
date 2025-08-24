import { google } from 'googleapis';

export default async (req) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type'
  };
  if (req.method === 'OPTIONS') return new Response('', { status: 204, headers });
  if (req.method !== 'POST') return new Response(JSON.stringify({ error: 'POST only' }), { status: 405, headers });

  try {
    const { url, source = 'manual', note = '' } = await req.json();
    if (!url || !/tiktok\.com/.test(url))
      return new Response(JSON.stringify({ error: 'Invalid TikTok URL' }), { status: 400, headers });

    const SHEET_ID = process.env.SHEET_ID;
    const creds = JSON.parse(process.env.GOOGLE_CREDENTIALS || '{}');
    if (!SHEET_ID || !creds.client_email || !creds.private_key)
      return new Response(JSON.stringify({ error: 'Missing env (SHEET_ID/GOOGLE_CREDENTIALS)' }), { status: 500, headers });

    const auth = new google.auth.JWT(
      creds.client_email,
      null,
      creds.private_key,
      ['https://www.googleapis.com/auth/spreadsheets']
    );
    await auth.authorize();
    const sheets = google.sheets({ version: 'v4', auth });

    const tab = 'AdSpy_UGC';
    await sheets.spreadsheets.values.update({
      spreadsheetId: SHEET_ID,
      range: `${tab}!A1:H1`,
      valueInputOption: 'RAW',
      requestBody: { values: [['Timestamp','URL','Source','Note','Author','Likes','Views','Score']] }
    }).catch(() => {});

    const now = new Date().toISOString();
    await sheets.spreadsheets.values.append({
      spreadsheetId: SHEET_ID,
      range: `${tab}!A2`,
      valueInputOption: 'USER_ENTERED',
      requestBody: { values: [[now, url, source, note, '', '', '', '']] }
    });

    return new Response(JSON.stringify({ ok: true, added: url }), { status: 200, headers });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e) }), { status: 500, headers });
  }
};
