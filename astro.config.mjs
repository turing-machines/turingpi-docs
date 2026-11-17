// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightLlmsTxt from 'starlight-llms-txt';
import sidebar from './src/sidebar.json' with { type: 'json' };

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
			logo: { light: './src/assets/logo-light.svg', dark: './src/assets/logo-dark.svg' },
			favicon: '/favicon.png',
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/turing-machines' },
				{ icon: 'discord', label: 'Discord', href: 'https://discord.com/invite/uNbysyc' },
			],
			customCss: ['./src/styles/custom.css'],
			sidebar,
			// ReadMe served /llms.txt for AI assistants; keep that working.
			plugins: [starlightLlmsTxt({ projectName: 'Turing Pi' })],
			head: [
				{ tag: 'link', attrs: { rel: 'icon', href: '/favicon.png', type: 'image/png' } },
			],
		}),
	],
});
