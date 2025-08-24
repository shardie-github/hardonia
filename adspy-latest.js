import { google } from 'googleapis';

export default async () => {
  try {
    const SHEET_ID = process.env.SHEET_ID;
    const creds = JSON.parse(process.env.GOOGLE_CREDENTIALS || '{}');
    const auth = new google.auth.JWT(
      creds.client_email,
      null,
      creds.private_key,
      ['https://www.googleapis.com/auth/spreadsheets.readonly']
    );
    await auth.authorize();
    const sheets = google.sheets({ version: 'v4', auth });

    const tab = 'AdSpy_UGC';
    const resp = await sheets.spreadsheets.values.get({
      spreadsheetId: SHEET_ID,
      range: `${tab}!A1:H2000`
    });
    const rows = resp.data.values || [];
    const [header, ...body] = rows;
    const idx = header.indexOf('URL');
    const urls = body.map(r => r[idx]).filter(Boolean);
    return new Response(urls.join('\n'), {
      status: 200,
      headers: { 'Content-Type': 'text/plain; charset=utf-8' }
    });
  } catch (e) {
    return new Response('ERROR: ' + String(e), { status: 500 });
  }
};
