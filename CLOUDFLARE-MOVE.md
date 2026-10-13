# Move honorbrook-insurance.com from Netlify to Cloudflare Pages

Repo is ready: site/_redirects and site/_headers replace netlify.toml's rules.
Nothing is live on Cloudflare until you do steps 1-4 (account actions only you can do).

1. Sign up free at dash.cloudflare.com.
2. Workers & Pages > Create > Pages > Connect to Git > pick luaysadqi1-web/honorbrook-marketing.
   Build command: (leave empty)   Build output directory: site   Production branch: main
3. Open the *.pages.dev preview URL it gives you and check: home, /about, /medicare-advantage,
   a blog post, a county page, /services/medicare.html (should 301 to /medicare-advantage).
4. Custom domains > add honorbrook-insurance.com and www.honorbrook-insurance.com.
   Cloudflare asks you to move the domain's nameservers to Cloudflare (free). Do this at the registrar.
   Keep Netlify serving until the pages.dev check in step 3 passes.
5. In Cloudflare (SSL/TLS > Edge Certificates): turn on "Always Use HTTPS".
   Rules > Redirect Rules: https://www.honorbrook-insurance.com/* -> https://honorbrook-insurance.com/${1} (301).
   (Host-based redirects cannot live in _redirects.)
6. After cutover, in Search Console resubmit sitemap.xml and sitemap-counties.xml.

Not carried over: the Netlify chat function (never had an API key, so the widget only shows its phone fallback).
