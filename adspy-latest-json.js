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
    const items = body.map(r => Object.fromEntries(header.map((h,i)=>[h, r[i] || ''])));
    return new Response(JSON.stringify({ items }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e) }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};
