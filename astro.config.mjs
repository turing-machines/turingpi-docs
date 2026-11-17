// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightLlmsTxt from 'starlight-llms-txt';
import sidebar from './src/sidebar.json' with { type: 'json' };

// Public repo with the page sources. Every page links to its file there ("Suggest an edit"):
// readers without write access get a fork + pull request automatically.
const REPO = 'https://github.com/turing-machines/turingpi-docs';

export default defineConfig({
	site: 'https://docs.turingpi.com',
	// Keep ReadMe's URL shape exactly: /docs/<slug>, no trailing slash.
	trailingSlash: 'never',
	build: { format: 'file' },
	integrations: [
		starlight({
			title: 'Turing Pi Docs',
			description:
				'Guides and documentation for Turing Pi 2, Turing RK1 and supported compute modules: hardware setup, BMC, flashing OS, Kubernetes and more.',
			// Logo only, like the turingpi.com header; the title stays for <title> and screen readers.
			logo: { light: './src/assets/logo-light.svg', dark: './src/assets/logo-dark.svg', replacesTitle: true },
			favicon: '/favicon.png',
			social: [
				{ icon: 'github', label: 'GitHub', href: REPO },
				{ icon: 'discord', label: 'Discord', href: 'https://discord.com/invite/uNbysyc' },
			],
			editLink: { baseUrl: `${REPO}/edit/main/` },
			customCss: ['@fontsource-variable/inter', './src/styles/custom.css'],
			// Header, footer and mobile menu carry the turingpi.com menu and footer links.
			components: {
				Header: './src/components/Header.astro',
				Footer: './src/components/Footer.astro',
				MobileMenuFooter: './src/components/MobileMenuFooter.astro',
			},
			expressiveCode: { styleOverrides: { borderRadius: '0.75rem' } },
			sidebar,
			// ReadMe served /llms.txt for AI assistants; keep that working.
			plugins: [starlightLlmsTxt({ projectName: 'Turing Pi' })],
			head: [
				{ tag: 'link', attrs: { rel: 'icon', href: '/favicon.png', type: 'image/png' } },
			],
		}),
	],
});
