import os
from typing_extensions import Any, Mapping, Literal
from dataclasses import dataclass, field
import json as _json
import time
from urllib.parse import urlencode
import base64
import hashlib
import hmac
import httpx
from .client import HttpClient, HttpMixin, BIT2ME_API_URL

def message_to_sign(nonce: str, url: str, body: str | None = None) -> str:
  """Build the string that is SHA-256-hashed then HMAC-SHA512-signed.

  Bit2Me expects ``nonce:path`` when there is no body, and ``nonce:path:body`` when
  there is a JSON body (compact, no spaces). Do not append ``:`` for an empty body.
  """
  payload = f'{nonce}:{url}'
  if body is not None and body != '':
    payload += ':' + body
  return payload

def sign_message(message: str, secret: str) -> str:
  message_bytes = message.encode('utf-8')
  secret_bytes = secret.encode('utf-8')
  sha256 = hashlib.sha256()
  sha256.update(message_bytes)
  hash_digest = sha256.digest()
  hmac_sha512 = hmac.new(secret_bytes, hash_digest, hashlib.sha512)
  hmac_digest = base64.b64encode(hmac_sha512.digest()).decode()
  return hmac_digest

def auth_headers(api_key: str, secret_key: str, *, nonce: str | None = None, path: str, body: str | None = None) -> dict[str, str]:
  nonce = nonce or str(int(time.time() * 1000))
  msg = message_to_sign(nonce, path, body)
  signature = sign_message(msg, secret_key)
  return {
    'x-api-key': api_key,
    'api-signature': signature,
    'x-nonce': nonce
  }


@dataclass
class AuthHttpClient(HttpClient):
  api_key: str
  api_secret: str

  async def authed_request(
    self, method: str, base_url: str, path: str,
    *,
    json: Any | None = None,
    params: Mapping | None = None,
    headers: Mapping[str, str] | None = None,
    cookies: httpx._types.CookieTypes | None = None,
    auth: httpx._types.AuthTypes | httpx._client.UseClientDefault | None = httpx.USE_CLIENT_DEFAULT,
    follow_redirects: bool | httpx._client.UseClientDefault = httpx.USE_CLIENT_DEFAULT,
    timeout: httpx._types.TimeoutTypes | httpx._client.UseClientDefault = httpx.USE_CLIENT_DEFAULT,
    extensions: httpx._types.RequestExtensions | None = None,
  ):
    # Use `is not None` so JSON false / 0 / [] / "" still serialize and sign correctly.
    body = _json.dumps(json, separators=(',', ':')) if json is not None else None
    if params:
      path += '?' + urlencode(params, doseq=True)
    headers = {
      **auth_headers(self.api_key, self.api_secret, path=path, body=body),
      **(headers or {})
    }
    url = base_url + path
    return await self.request(
      method, url, headers=headers, content=body,
      auth=auth, follow_redirects=follow_redirects,
      cookies=cookies, timeout=timeout, extensions=extensions,
    )
  
  
@dataclass
class AuthHttpMixin(HttpMixin):
  base_url: str = field(kw_only=True, default=BIT2ME_API_URL)
  http: AuthHttpClient # type: ignore

  @classmethod
  def new(cls, api_key: str | None = None, api_secret: str | None = None, *, base_url: str = BIT2ME_API_URL):
    if api_key is None:
      api_key = os.environ['BIT2ME_API_KEY']
    if api_secret is None:
      api_secret = os.environ['BIT2ME_SECRET_KEY']
    client = AuthHttpClient(api_key=api_key, api_secret=api_secret)
    return cls(base_url=base_url, http=client)
  
  async def __aenter__(self):
    await self.http.__aenter__()
    return self
  
  async def __aexit__(self, exc_type, exc_value, traceback):
    await self.http.__aexit__(exc_type, exc_value, traceback)

  async def authed_request(
    self, method: str, path: str,
    *,
    json: Any | None = None,
    params: Mapping | None = None,
    headers: Mapping[str, str] | None = None,
    cookies: httpx._types.CookieTypes | None = None,
    auth: httpx._types.AuthTypes | httpx._client.UseClientDefault | None = httpx.USE_CLIENT_DEFAULT,
    follow_redirects: bool | httpx._client.UseClientDefault = httpx.USE_CLIENT_DEFAULT,
    timeout: httpx._types.TimeoutTypes | httpx._client.UseClientDefault = httpx.USE_CLIENT_DEFAULT,
    extensions: httpx._types.RequestExtensions | None = None,
  ):
    return await self.http.authed_request(
      method, self.base_url, path, params=params, headers=headers, json=json,
      auth=auth, follow_redirects=follow_redirects,
      cookies=cookies, timeout=timeout, extensions=extensions, 
    )

  async def authed_totp_request(
    self, method: str, path: str,
    *,
    totp_code: str, totp_type: Literal['gauth', 'sms', 'email'],
    json: Any | None = None,
    params: Mapping | None = None,
    headers: Mapping[str, str] | None = None,
    cookies: httpx._types.CookieTypes | None = None,
    auth: httpx._types.AuthTypes | httpx._client.UseClientDefault | None = httpx.USE_CLIENT_DEFAULT,
    follow_redirects: bool | httpx._client.UseClientDefault = httpx.USE_CLIENT_DEFAULT,
    timeout: httpx._types.TimeoutTypes | httpx._client.UseClientDefault = httpx.USE_CLIENT_DEFAULT,
    extensions: httpx._types.RequestExtensions | None = None,
  ):
    headers = {
      **(headers or {}),
      'x-totp': totp_code,
      'x-totp-type': totp_type,
    }
    return await self.http.authed_request(
      method, self.base_url, path, params=params, headers=headers, json=json,
      auth=auth, follow_redirects=follow_redirects,
      cookies=cookies, timeout=timeout, extensions=extensions, 
    )
