// Links shared with the main site (turingpi.com header and footer).
export const siteNav = [
	{ label: 'Shop', href: 'https://turingpi.com/shop/' },
	{ label: 'Blog', href: 'https://turingpi.com/blog/' },
	{ label: 'Docs', href: '/', current: true },
	{ label: 'Help', href: 'https://turingpi.com/help/' },
];

export const footerLinks = [
	{ label: 'Media kit', href: 'https://turingpi.com/media-kit/' },
	{ label: 'Privacy', href: 'https://turingpi.com/privacy-policy/' },
	{ label: 'Terms', href: 'https://turingpi.com/terms-of-use/' },
];

export const footerSocials = [
	{ icon: 'discord', label: 'Discord', href: 'https://discord.com/invite/uNbysyc' },
	{ icon: 'twitter', label: 'Twitter', href: 'https://twitter.com/turingpi' },
	{ icon: 'facebook', label: 'Facebook', href: 'https://facebook.com/turingpi' },
	{ icon: 'tiktok', label: 'TikTok', href: 'https://www.tiktok.com/@turingpi' },
] as const;
