import { defineRouteMiddleware } from '@astrojs/starlight/route-data';

// With build.format 'file' Starlight builds canonical / og:url from the output file
// (https://docs.turingpi.com/docs/foo.html). The live URL — and the one ReadMe used —
// is /docs/foo, so strip the .html to keep search engines on the same URLs.
const clean = (url: string) => url.replace(/\/index\.html$/, '/').replace(/\.html$/, '');

export const onRequest = defineRouteMiddleware((context) => {
	for (const tag of context.locals.starlightRoute.head) {
		const attrs = tag.attrs;
		if (!attrs) continue;
		if (attrs.rel === 'canonical' && typeof attrs.href === 'string') attrs.href = clean(attrs.href);
		if (attrs.property === 'og:url' && typeof attrs.content === 'string') attrs.content = clean(attrs.content);
	}
});
