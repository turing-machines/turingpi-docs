// Check every internal link and #anchor in the built site (dist/), following public/_redirects.
// Usage: npm run build && npm run check-links
import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';

const DIST = new URL('../dist/', import.meta.url).pathname;
const redirects = new Map(
	readFileSync(join(DIST, '_redirects'), 'utf8')
		.split('\n')
		.filter((l) => l.trim() && !l.startsWith('#') && !l.includes('*'))
		.map((l) => l.trim().split(/\s+/).slice(0, 2)),
);

const walk = (dir) =>
	readdirSync(dir).flatMap((f) => {
		const p = join(dir, f);
		return statSync(p).isDirectory() ? walk(p) : [p];
	});

const pages = new Map(); // url path -> html
for (const file of walk(DIST).filter((f) => f.endsWith('.html'))) {
	let url = '/' + relative(DIST, file).replace(/\.html$/, '');
	url = url === '/index' ? '/' : url.replace(/\/index$/, '');
	pages.set(url, readFileSync(file, 'utf8'));
}
const ids = new Map([...pages].map(([u, html]) => [u, new Set([...html.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1]))]));

const resolve = (path) => {
	for (let i = 0; i < 5 && redirects.has(path); i++) path = redirects.get(path);
	return path;
};

let broken = 0;
for (const [from, html] of pages) {
	if (from === '/404') continue;
	for (const [, raw] of html.matchAll(/<a\s[^>]*href="([^"]+)"/g)) {
		const href = raw.replaceAll('&amp;', '&');
		if (!href.startsWith('/') && !href.startsWith('#')) continue;
		const [p, hash] = href.split('#');
		const path = resolve(decodeURI(p || from).replace(/\/$/, '') || '/');
		const isFile = existsSync(join(DIST, path)) && statSync(join(DIST, path)).isFile();
		if (!pages.has(path) && !isFile) {
			console.log(`${from}: missing page ${href}`);
			broken++;
		} else if (hash && pages.has(path) && !ids.get(path).has(decodeURIComponent(hash))) {
			console.log(`${from}: missing anchor ${href}`);
			broken++;
		}
	}
}
console.log(`${pages.size} pages checked, ${broken} broken internal links`);
process.exit(broken ? 1 : 0);
