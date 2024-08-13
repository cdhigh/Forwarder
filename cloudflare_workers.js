const ALLOW_KEYS = 'xzSlE';

export default {
  async fetch(request, env, ctx) {
    return await handleRequest(request);
  }
}

async function handleRequest(request) {
  const url = new URL(request.url);
  const params = new URLSearchParams(url.search);

  const u = params.get('u');  // 需要转发的url
  const k = params.get('k');  // AUTHKEY
  const timeout = parseInt(params.get('t') || '30') * 1000;  // 超时时间，默认30秒

  if (!k || k !== ALLOW_KEYS) {
    return new Response('Auth Key is invalid!', { status: 403 });
  }

  if (!u || !k) {
    return new Response('<html><head><title>Forwarder Url</title></head><body>Forwarder(1.2.4) : thisurl?k=AUTHKEY&t=timeout&u=url</body></html>', {
      headers: { 'Content-Type': 'text/html' },
    });
  }

  const referer = new URL(u).origin;

  try {
    // 设置超时的 Promise，用于处理超时情况
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    // 转发请求
    const response = await fetch(u, {
      method: 'GET',
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en,*',
        'Referer': referer
      },
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    // 提取并传递所有非 hop-by-hop 的 headers
    const newHeaders = new Headers(response.headers);
    ['connection', 'keep-alive', 'proxy-authenticate', 'proxy-authorization', 'te', 'trailer', 'transfer-encoding', 'upgrade'].forEach(header => {
      newHeaders.delete(header);
    });

    return new Response(await response.text(), {
      status: response.status,
      headers: newHeaders,
    });
  } catch (e) {
    console.error("Error: ", e);
    return new Response('Request failed!<br/>' + e, { status: 400 });
  }
}
