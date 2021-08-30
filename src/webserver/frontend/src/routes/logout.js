export async function get() {
	return {
		status: 308,
		headers: {
			'set-cookie': [
				'jwt=deleted; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT',
				'opensoar_user=deleted; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT'
			],
			'location': '/'
		}
	};
}